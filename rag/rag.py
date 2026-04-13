"""
rag服务
"""
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser

from file_history_store import FileChatMessageHistory
from vectore_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda


def get_history(session_id):
    return FileChatMessageHistory(session_id, "./chat_history")


def print_model(prompt):
    print("*" * 20)
    print(prompt)
    print("*" * 20)
    return prompt


class RagService(object):
    def __init__(self):
        self.vector_store = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model_name))

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "以我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料:{context}。"),
                ("system", "并且我提供用户的对话历史记录，如下："),
                MessagesPlaceholder("history"),
                ("user", "请回答用户提问：{input}")
            ]
        )

        self.model = ChatTongyi(model=config.chat_model_name)

        self.chain = self.__get_chain()

    def __get_chain(self):
        """
        获取问答链
        :return:
        """

        # 获取检索器
        retriever = self.vector_store.get_retriever()

        def format_document(doc: list[Document]):
            if not doc:
                return "无相关参考资料"

            formatted_str = ""
            for doc in doc:
                formatted_str += f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n"
            return formatted_str

        def format_for_prompt_template(value):
            # {input, context, history}
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["context"] = value["context"]
            new_value["history"] = value["input"]["history"]
            return new_value

        def format_for_retriever(value: dict) -> str:
            return value["input"]

        chain = ({"input": RunnablePassthrough(),
                  "context": RunnableLambda(format_for_retriever) | retriever | format_document
                  } | RunnableLambda(format_for_prompt_template)
                 | self.prompt_template
                 | print_model
                 | self.model
                 | StrOutputParser())

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        return conversation_chain
        # return chain


if __name__ == '__main__':
    # res = RagService().chain.invoke("我的身高185cm,体重180斤，尺码推荐")
    # print(res)

    # session id 配置
    session_config = {
        "configurable": {
            "session_id": "user_001",
        }
    }

    res = RagService().chain.invoke({"input": "棉裤如何保养？"}, session_config)
    print(res)

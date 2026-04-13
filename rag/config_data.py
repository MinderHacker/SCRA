
"""
配置文件
"""
md5_path="./md5.txt"

# aliyun
# DASHSCOPE_API_KEY=xxxx    #填写自己的api key

# Chroma
collection_name = "rag"
persist_directory = "./chroma_db"

# spliter
chunk_size = 1000
chunk_overlap = 1000
separators = ["\n\n", "\n", ".", "!", "?", "。", "！", "？", " ", ""]
max_split_char_number = 1000    # 文本分割的阈值

#
similarity_threshold = 1            # 检索返回匹配的文档数量

chat_model_name = "qwen3-max"
embedding_model_name = "text-embedding-v4"

session_config = {
        "configurable": {
            "session_id": "user_001",
        }
    }

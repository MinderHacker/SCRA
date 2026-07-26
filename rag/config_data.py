
"""
配置文件
"""
md5_path="./rag/md5.txt"

# aliyun
DASHSCOPE_API_KEY="..."    #填写自己的api key

# Chroma
collection_name = "rag"
# persist_directory = "./chroma_db"
# Milvus Standalone
milvus_uri = "http://192.168.101.128:19530"

# spliter
chunk_size = 500
chunk_overlap = 100
separators = ["\n\n", "\n", ".", "!", "?", "。", "！", "？", " ", ""]
max_split_char_number = 500 # 文本分割的阈值

#
similarity_threshold = 3            # 检索返回匹配的文档数量

chat_model_name = "qwen3-max"
embedding_model_name = "text-embedding-v4"

session_config = {
        "configurable": {
            "session_id": "user_001",
        }
    }

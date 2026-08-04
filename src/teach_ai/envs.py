
import os
import pathlib


from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 读取环境变量
DS_KEY = os.getenv("DS_KEY")
GLM_KEY = os.getenv("GLM_KEY")

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
print(f"BASE_DIR: {BASE_DIR}")

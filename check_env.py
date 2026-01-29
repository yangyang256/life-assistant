from dotenv import load_dotenv
import os

load_dotenv()

tokens_raw = os.getenv("ACCESS_TOKENS", "")
tokens = [t.strip() for t in tokens_raw.split(",") if t.strip()]

print("LECTURE_URL:", os.getenv("LECTURE_URL"))
print("PREFILED_ID:", os.getenv("PREFILED_ID"))
print("AUDIENCE_ID:", os.getenv("AUDIENCE_ID"))
print("GRAB_TIME:", os.getenv("GRAB_TIME"))
print("THREADS_PER_ACCOUNT:", os.getenv("THREADS_PER_ACCOUNT"))
print("MAX_RETRIES:", os.getenv("MAX_RETRIES"))
print("SLEEP_RETRY:", os.getenv("SLEEP_RETRY"))
print("Tokens count:", len(tokens))
print("First token preview:", (tokens[0][:6] + "******") if tokens else "NONE")
print("✅ .env 文件加载完成！")


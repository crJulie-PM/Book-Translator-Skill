import os
import time
import requests

# ========= 配置 =========
INPUT_FILE = "The Very Secret Society of Irre.txt"          # 你的英文原版书
OUTPUT_FILE = "The Very Secret Society of Irre2.txt"      # 输出中文文件名

# ---------- DeepSeek 配置 ----------
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")   # 从环境变量读取 Key（安全）
if not DEEPSEEK_API_KEY:
    raise ValueError("请在环境变量中设置 DEEPSEEK_API_KEY")

DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"            # 常用模型，也可用 deepseek-reasoner

# ---------- 其他参数 ----------
CHUNK_SIZE = 1500                           # 每块字数（可调）
CHUNK_MARK = "----CHUNK----"                # 分隔标记，用于断点续传
RETRY_SLEEP = 3                             # 出错重试等待秒数

# ==========================================

def count_done_chunks(path):
    """统计已经翻译了多少个块（用于断点续传）"""
    if not os.path.exists(path):
        return 0
    with open(path, "r", encoding="utf-8") as f:
        return f.read().count(CHUNK_MARK)

def split_text(text, chunk_size):
    """按段落切分文本，尽量保持语义完整"""
    text = text.replace("\r\n", "\n")
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""
    for p in paragraphs:
        if len(current) + len(p) < chunk_size:
            current += p + "\n\n"
        else:
            chunks.append(current)
            current = p + "\n\n"
    if current:
        chunks.append(current)
    return chunks

def deepseek_translate(text):
    """调用 DeepSeek API 翻译一段英文"""
    prompt = f"""请把下面英文翻译成自然通顺的简体中文。
要求：
1 只输出中文
2 保留段落
3 不要解释

{text}"""

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    r = requests.post(DEEPSEEK_URL, json=data, headers=headers)
    if r.status_code != 200:
        raise RuntimeError(f"API 错误 {r.status_code}: {r.text}")

    result = r.json()
    # DeepSeek 响应格式与 OpenAI 一致
    return result["choices"][0]["message"]["content"]

def main():
    # 检查输入文件
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"找不到输入文件: {INPUT_FILE}")

    # 读取原文
    with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    # 切块
    chunks = split_text(text, CHUNK_SIZE)
    done = count_done_chunks(OUTPUT_FILE)

    print("模型:", DEEPSEEK_MODEL)
    print("输入文件:", INPUT_FILE)
    print("输出文件:", OUTPUT_FILE)
    print("总块数:", len(chunks))
    print("已翻译:", done)

    # 逐块翻译并追加写入
    with open(OUTPUT_FILE, "a", encoding="utf-8") as out:
        for i in range(done, len(chunks)):
            while True:
                try:
                    print(f"正在翻译 {i+1}/{len(chunks)} ...")
                    zh = deepseek_translate(chunks[i])
                    out.write("\n" + CHUNK_MARK + "\n")
                    out.write(zh)
                    out.write("\n")
                    out.flush()
                    print(f"已保存第 {i+1} 块")
                    break
                except Exception as e:
                    print("出错:", e)
                    print(f"等待 {RETRY_SLEEP} 秒后重试...")
                    time.sleep(RETRY_SLEEP)

    print("全部翻译完成！")

if __name__ == "__main__":
    main()
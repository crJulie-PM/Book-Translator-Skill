# Book-Translator-Skill
一个基于 Python 和 DeepSeek API 的自动化脚本，能将英文电子书（.txt 格式）翻译成流畅、自然的中文。支持长文本分块、断点续传，方便处理大部头书籍或长篇网文小说。
## ✨ 主要特性
- **智能分块**：按段落和字数自动切分长文本，保留语义完整性。
- **断点续传**：翻译中断后再次运行，自动从上次中断的地方继续。
- **本地运行**：数据在本地处理，只需调用DeepSeek API，安全可控。
- **简单易用**：只需准备一个 `.txt` 文件，即可开始翻译。
- ## 🛠️ 安装与配置

### 前提条件
- Python 3.8 或更高版本
- 一个 [DeepSeek](https://platform.deepseek.com/) API Key

### 安装步骤
 **克隆仓库**
    ```bash
    git clone https://github.com/crJulie-PM/book-translator-skill.git
    cd book-translator-skill
    **安装依赖**
    pip install -r requirements.txt
    
#### 使用方法

1.  **准备文件**：将你的英文电子书转换为 `.txt` 格式，放入项目文件夹。
2.  **设置API Key**：在终端中设置环境变量（推荐，更安全）。
    ```bash
    # Windows (PowerShell)
    $env:DEEPSEEK_API_KEY="你的API密钥"

    # macOS / Linux
    export DEEPSEEK_API_KEY="你的API密钥"
3. **运行脚本**：
deepseek-translatebook.py
4.**获取结果**：翻译完成后，会在同目录下生成一个 _zh.txt 结尾的中文文件。

#### 5. 配置说明
```markdown
## ⚙️ 配置项

你可以在 `translator.py` 文件头部修改以下参数：

| 变量 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `INPUT_FILE` | 输入文件名 | `"as_man_thinketh.txt"` |
| `OUTPUT_FILE` | 输出文件名 | `"as_man_thinketh_zh.txt"` |
| `CHUNK_SIZE` | 每段翻译的最大字符数 | `1500` |
| `DEEPSEEK_MODEL` | 使用的DeepSeek模型 | `"deepseek-chat"` |

** ❓ 常见问题**
**Q: 如何将 EPUB/MOBI 格式转换为 TXT？**
A: 推荐使用免费工具 [Calibre](https://calibre-ebook.com/)。安装后，在终端执行：
```bash
ebook-convert 你的书.epub 你的书.txt

#### 许可证
```markdown
## 📄 许可证
本项目采用 [MIT License](LICENSE) 开源许可证。
## 文件准备清单
创建 .gitignore 文件：内容可参考：
# Python
__pycache__/
*.pyc
.env
venv/
env/

# 输出文件（可选，避免把翻译好的大文件也上传）
*_zh.txt
创建 requirements.txt 文件：在项目文件夹的终端中运行：
pip freeze > requirements.txt

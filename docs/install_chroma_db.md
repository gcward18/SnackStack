### 🛠️ Python Installation & Verification
Activate Virtual Environment (Recommended)

```bash
python -m venv .venv

source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

Use code with caution.Install the Package

```bash
pip install langchain-chroma
```

Verify the Installation

```python
import chromadb

print(chromadb.__version__)
```
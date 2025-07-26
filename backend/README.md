
# 🧠 MCP-Compliant Text Insight API

A lightweight FastAPI-based service providing **rule-based summarization and classification** of textual feedback, compliant with the **Model Context Protocol (MCP)**. Ideal for structured feedback processing in dashboards, CRMs, or analytics pipelines.

---

## 🚀 Features

- ✅ Rule-based **Summarization** of input text  
- ✅ Confidence-based **Classification** (e.g., Bug, Feature Request, Usability Issue)  
- ✅ Fully **MCP-compliant** input/output schema  
- ✅ Ready for **CORS-enabled frontend integration**  


---

## 📁 Project Structure

```
BACKEND/
├── __pycache__/
├── .venv/
├── .vscode/
├── data/
├── postman/
├── index.html
├── logic_handler.py
├── main.py
├── models.py
├── README.md
├── requirements.txt
└── schemas.py
```

---

## ⚙️ Installation

### 🔧 Prerequisites

- Python 3.11.8
- pip (Python package manager)

### 🐍 Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 📦 Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🧪 Run the API

```bash
uvicorn main:app --reload
```

- API runs at: `http://127.0.0.1:8000`


---

## 📨 API Usage

### 🔍 Endpoint: `/mcp/process`

- **Method:** `POST`
- **Content-Type:** `application/json`
- **Response Model:** `MCPOutput`

### ✅ Example Request

```json
{
  "model_context": {
    "task": "text_analysis",
    "intent": "summarization + classification",
    "user_role": "customer",
    "language": "en"
  },
  "input": {
    "text": "I love the new dark mode, but the search is extremely slow after the recent update."
  }
}
```

### ✅ Example Response

```json
{
  "output": {
    "summary": "User praises the dark mode for aesthetics and comfort.",
    "category": "Usability Issue",
    "confidence": 0.82
  },
  "mcp_response": {
    "task": "text_analysis",
    "intent": "summarization + classification",
    "output_type": "structured",
    "generated_by": "rule-engine-v1"
  }
}
```

---

## 🧠 Supported Intents

- `"summarization"`
- `"classification"`
- `"summarization + classification"`

> Unsupported intents will return an error message.

---

## 📄 MCP-Compliant Schema

This API follows a strict schema defined using [Pydantic](https://pydantic.dev).

### Input Fields

- `model_context`: Context metadata including task, intent, role, and language
- `input.text`: Raw user feedback to analyze

### Output Fields

- `summary`: Optional short summary of the input
- `category`: Optional classification label (e.g., Bug, Praise)
- `confidence`: Confidence score for classification
- `message`: Present only when the intent is unsupported

---

## 🧰 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [Uvicorn](https://www.uvicorn.org/) (ASGI server)

---



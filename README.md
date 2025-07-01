# 📚 Chat With Multiple PDF Documents using LangChain & Google Gemini Pro

A powerful AI chatbot that allows users to interact with **multiple PDF documents** by asking questions in natural language. This project utilizes **LangChain**, **FAISS**, and **Google Gemini Pro** to extract, index, and generate answers based on PDF content.

---

## 🚀 Features

- 📄 Upload and chat with multiple PDFs at once
- 🤖 Integrated with **Google Gemini Pro** (Generative AI)
- 🔍 Uses **FAISS** for fast vector similarity search
- 🧠 Semantic document understanding via embeddings
- 🧰 Lightweight frontend (Streamlit or CLI)
- 🔐 `.env` configuration for secure API keys

---

## 🧠 Technologies Used

- Python 3.10+
- [LangChain](https://python.langchain.com/)
- Google Generative AI (`gemini-pro`)
- FAISS for vector store
- PyMuPDF / PDFPlumber (PDF parsing)
- dotenv

---

## 📁 Project Structure

```

├── faiss-index/
│   ├── index.faiss
│   └── index.pkl
├── Notebook/
│   └── main.ipynb
├── System/
│   ├── helper.py
│   └── temp.py
├── frontend.py              # Main app runner
├── .env.example             # Template for environment variables
├── requirements.txt
├── LICENSE
└── README.md

````

---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/Chat-With-Multiple-PDF-Documents-With-Langchain-And-Google-Gemini-Pro.git
cd Chat-With-Multiple-PDF-Documents-With-Langchain-And-Google-Gemini-Pro

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
````

---

## 🔑 Setup API Keys

Rename `.env.example` to `.env` and add your credentials:

```
GOOGLE_API_KEY=your_google_api_key
```

> You can get your Gemini API key from [https://makersuite.google.com/app](https://makersuite.google.com/app)

---

## 🧪 How to Use

### Option 1: Notebook (for experiments)

```bash
jupyter notebook Notebook/main.ipynb
```

### Option 2: Run the App

```bash
python frontend.py
```

1. Load your PDFs.
2. Ask any question related to the content.
3. Get smart, contextual answers powered by Gemini.

---

## 💡 Example Questions

> "What does the document say about GDPR compliance?"
> "Summarize the key findings in Chapter 3."
> "What is the main argument of the second PDF?"

---

## ✅ To-Do

* [ ] Add PDF upload via UI
* [ ] Improve multi-doc context management
* [ ] Support long-form answers
* [ ] Export chat history

---

## 📄 License

Licensed under the [MIT License](LICENSE)

---

## 🙋‍♂️ Author

**Sayed Ali Hassan**
[GitHub](https://github.com/Sayedalihassaan)

---

## ⚠️ Disclaimer

This tool is intended for educational and research purposes only. Do not rely on it for legal or medical decisions without verification.

```

---

✅ **Next Steps**:
- Paste this into your `README.md` file.
- Replace `your-username` with your GitHub username if you're publishing the repo.

Let me know if you want:
- a custom logo/banner
- instructions for deploying on Streamlit Cloud or HuggingFace
- advanced usage for RAG or Gemini tuning
```

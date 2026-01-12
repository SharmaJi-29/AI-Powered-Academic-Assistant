from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from pypdf import PdfReader
import requests
import textwrap
import os


class SummarizerScreen(Screen):

    document_text = ""

    def on_pre_enter(self):
        self.ids.file_name_label.text = "No document selected"
        self.ids.summary.text = "Summary will appear here..."
        self.ids.summarize_btn.disabled = True
        self.ids.ask_btn.disabled = True

    # ===============================
    # LLM CALL (Ollama – Phi)
    # ===============================
    def llm_summarize(self, context):
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "phi",
                    "prompt": context,
                    "stream": False
                },
                timeout=120
            )
            return response.json().get("response", "No response from AI")
        except Exception as e:
            return f"AI Error: {e}"

    # ===============================
    # SIMPLE RAG
    # ===============================
    def rag_summarize(self, text):
        chunks = textwrap.wrap(text, 800)
        selected_chunks = chunks[:4]

        prompt = f"""
You are an academic summarization assistant.

Summarize the following content clearly and concisely.
Focus on key ideas, concepts, and conclusions.

Content:
{' '.join(selected_chunks)}

Provide a structured summary.
"""
        return self.llm_summarize(prompt)

    # ===============================
    # DOCUMENT PICKER (MODEL STYLE)
    # ===============================
    def open_document(self):
        from kivymd.uix.filemanager import MDFileManager

        self.file_manager = MDFileManager(
            select_path=self.select_path,
            exit_manager=self.exit_manager
        )
        self.file_manager.show(os.path.expanduser("~"))

    def exit_manager(self, *args):
        self.file_manager.close()

    def select_path(self, path):
        self.exit_manager()
        self.document_text = ""

        file_name = os.path.basename(path)
        self.ids.file_name_label.text = f"📄 {file_name}"

        if path.endswith(".pdf"):
            reader = PdfReader(path)
            self.document_text = " ".join(
                page.extract_text() or "" for page in reader.pages
            )

        elif path.endswith(".txt"):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                self.document_text = f.read()

        else:
            self.ids.summary.text = "❌ Only PDF or TXT allowed"
            return

        if not self.document_text.strip():
            self.ids.summary.text = "❌ No readable text found"
            return

        self.ids.summary.text = "📄 Document uploaded successfully. Click summarize."
        self.ids.summarize_btn.disabled = False

    # ===============================
    # SUMMARIZE DOCUMENT
    # ===============================
    def summarize_text(self):
        if not self.document_text.strip():
            self.ids.summary.text = "❗ Please upload a document first"
            return

        self.ids.summary.text = "⏳ Generating summary..."
        summary = self.rag_summarize(self.document_text)
        self.ids.summary.text = summary

        self.ids.ask_btn.disabled = False
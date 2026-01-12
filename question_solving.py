from kivy.uix.screenmanager import Screen
import requests
import pytesseract
from PIL import Image
from pypdf import PdfReader
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup


class VisualQnAScreen(Screen):

    def llama2_response(self, prompt):
        try:
            r = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "phi", "prompt": prompt, "stream": False},
                timeout=120
            )
            return r.json().get("response", "No response")
        except Exception as e:
            return f"AI Error: {e}"

    def search_query(self):
        q = self.ids.question.text.strip()
        if not q:
            self.ids.answer.text = "Please enter a question"
            return
        self.ids.answer.text = "Thinking..."
        self.ids.answer.text = self.llama2_response(q)

    def open_image(self):
        chooser = FileChooserIconView(filters=["*.png", "*.jpg", "*.jpeg"])
        popup = Popup(title="Select Image", content=chooser, size_hint=(0.9, 0.9))
        chooser.bind(on_submit=lambda x, y, z: self.process_image(y[0], popup))
        popup.open()

    def process_image(self, path, popup):
        popup.dismiss()
        text = pytesseract.image_to_string(Image.open(path))
        self.ids.answer.text = self.llama2_response(text)

    def open_document(self):
        chooser = FileChooserIconView(filters=["*.pdf", "*.txt"])
        popup = Popup(title="Select Document", content=chooser, size_hint=(0.9, 0.9))
        chooser.bind(on_submit=lambda x, y, z: self.process_document(y[0], popup))
        popup.open()

    def process_document(self, path, popup):
        popup.dismiss()
        text = ""
        if path.endswith(".pdf"):
            for p in PdfReader(path).pages:
                if p.extract_text():
                    text += p.extract_text()
        else:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        self.ids.answer.text = self.llama2_response(text[:3000])
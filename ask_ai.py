from kivy.uix.screenmanager import Screen
import requests


class AskAIScreen(Screen):

    def ask_ai(self):
        question = self.ids.question.text.strip()

        if not question:
            self.ids.answer.text = "❗ Please enter a question"
            return

        self.ids.answer.text = "⏳ Thinking..."

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "phi",
                    "prompt": f"""
You are an academic assistant.
Answer the following question clearly and accurately.

Question:
{question}
""",
                    "stream": False
                },
                timeout=120
            )

            self.ids.answer.text = response.json().get(
                "response", "No response from AI"
            )

        except Exception as e:
            self.ids.answer.text = f"AI Error: {e}"
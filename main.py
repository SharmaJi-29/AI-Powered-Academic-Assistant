from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from splash import SplashScreen
from login import LoginScreen
from register import RegisterScreen
from database import init_db
from kivy.core.window import Window
from question_solving import VisualQnAScreen
from summerizer import SummarizerScreen
from ask_ai import AskAIScreen
from studyplanner import StudyPlannerScreen


Window.size = (350, 600)

class HomeScreen(Screen):
    pass

class AcademicApp(MDApp):
    def build(self):
        init_db()
        self.theme_cls.theme_style = "Light"

        self.sm = ScreenManager()
        self.sm.add_widget(SplashScreen(name="splash"))
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(RegisterScreen(name="register"))
        self.sm.add_widget(HomeScreen(name="home"))
        self.sm.add_widget(VisualQnAScreen(name="question_solving"))
        self.sm.add_widget(SummarizerScreen(name="summarizer"))
        self.sm.add_widget(AskAIScreen(name="ask_ai"))
        self.sm.add_widget(StudyPlannerScreen(name="study_planner"))
    
        return self.sm
    
    def open_QnA(self):
        self.sm.current = "question_solving"

    def open_summarizer(self):
        self.sm.current = "summarizer"

    def open_ask_ai(self):
        self.sm.current = "ask_ai"

    def go_home(self):
        self.sm.current = "home"

    def go_back_to_summarizer(self):
        self.sm.current = "summarizer"

    def open_study_planner(self):
        self.sm.transition.direction = "left"
        self.sm.current = "study_planner"

    def go_home_from_planner(self):
        self.sm.transition.direction = "right"
        self.sm.current = "home"

if __name__ == "__main__":
    AcademicApp().run()
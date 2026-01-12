from kivymd.uix.screen import MDScreen
from kivy.clock import Clock

class SplashScreen(MDScreen):
    def on_enter(self):
        Clock.schedule_once(self.go_next, 3)  # After 3 sec, go to login

    def go_next(self, *args):
        self.manager.current = "login"
from kivymd.uix.screen import MDScreen
from kivymd.toast import toast
from database import validate_user

class LoginScreen(MDScreen):
    def do_login(self):
        email = self.ids.email.text
        password = self.ids.password.text

        if validate_user(email, password):
            toast("Login Successful ")
            self.manager.current = "home"
        else:
            toast("Invalid Credentials")
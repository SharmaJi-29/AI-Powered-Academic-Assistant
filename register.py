from kivymd.uix.screen import MDScreen
from kivymd.toast import toast
from database import register_user

class RegisterScreen(MDScreen):
    def do_register(self):
        username = self.ids.username.text
        email = self.ids.email.text
        password = self.ids.password.text

        if register_user(username, email, password):
            toast("Registered Successfully ")
            self.manager.current = "login"
        else:
            toast("User Already Exists ")
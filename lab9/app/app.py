from flask import Flask


class App:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(App, cls).__new__(cls)
            cls.instance.__app = Flask(__name__)
            cls.instance.__app.config.from_object('config')
        return cls.instance

    def getApp(self):
        return self.__app

    @staticmethod
    def getMenu():
        return {
            "/about": "About me",
            "/contacts": "My contacts",
            "/users": "Users",
            "/login": "SignIn",
            "/register": "SignUp",
            "/account": "Account",
            "/logout": "Logout"
        }

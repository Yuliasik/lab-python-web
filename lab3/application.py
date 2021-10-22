from flask import Flask


class Application:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Application, cls).__new__(cls)
            cls.instance.__app = Flask(__name__)
        return cls.instance

    def getApplication(self):
        return self.__app

    @staticmethod
    def getMenu():
        return {
            "/about": "About me",
            "/contacts": "My contacts"
        }

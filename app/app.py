
class App:
    @staticmethod
    def getMenu():
        return {
            "/about": "About me",
            "/contacts": "My contacts",
            "/posts": "All posts",
            "/posts/create": "New post",
            "/posts/categories": "Categories",
            "/forms/form": "FormCabinet",
            "/auth/users": "Users",
            "/auth/login": "SignIn",
            "/auth/register": "SignUp",
            "/auth/account": "Account",
            "/auth/logout": "Logout"
        }

import unittest

from flask_login import current_user
from flask_testing import TestCase

from app import db, create_app
from app.auth.models import User
import urllib


class BaseTest(TestCase):

    def create_app(self):
        self.baseURL = 'http://localhost:5000/'
        return create_app('test')

    def setUp(self):
        db.create_all()
        db.session.add(User("adminuser", "admin.user@in.com", "password"))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_is_server_up_and_running(self):
        response = urllib.request.urlopen(self.baseURL)
        self.assertEqual(response.code, 200)

    def test_setup(self):
        self.assertTrue(self.app is not None)
        self.assertTrue(self.client is not None)
        self.assertTrue(self._ctx is not None)


class FlaskTest(BaseTest):
    # Чи фласк запущено коректно
    def test_index(self):
        response = self.client.get('/auth/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Чи сторінка з акаунтом перекидає на логін
    def test_is_account_route_to_login(self):
        response = self.client.get('/auth/account', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    # Чи сторінка з логіном відкривається
    def test_is_login_page_opens(self):
        response = self.client.get('/auth/login')
        self.assertIn(b'Login', response.data)

    # Чи впускає програма в систему при правильних даних
    def test_is_register_then_login_correct(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=dict(username="test_user",
                          email="test.user123@gmail.com",
                          password="password1",
                          password_repeat="password1"),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn('registered!', response.data)

            response = self.client.post(
                '/auth/login',
                data=dict(email="test.user123@gmail.com", password="password1"),
                follow_redirects=True
            )
            self.assertTrue(current_user.is_active)
            self.assert_200(response)

    # Чи не впускає при неправильно введених даних
    def test_incorrect_login(self):
        response = self.client.post(
            '/auth/login',
            data=dict(email="not_test_user@gmail.com", password="not_password"),
            follow_redirects=True
        )
        self.assertIn(b'Invalid login!', response.data)

    # Чи вибиває помилка при повторній спробі увійти
    def test_login_twice(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=dict(username="test_user",
                          email="test.user123@gmail.com",
                          password="password1",
                          password_repeat="password1"),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn('registered!', response.data)

            response = self.client.post(
                '/auth/login',
                data=dict(email="test.user123@gmail.com", password="password1"),
                follow_redirects=True
            )
            self.assertTrue(current_user.is_active)
            self.assert_200(response)

            response = self.client.post(
                '/auth/login',
                data=dict(email="test.user123@gmail.com", password="password1"),
                follow_redirects=True
            )
            self.assertIn('You are already loggined in!', response.data)
            self.assert_200(response)


if __name__ == '__main__':
    unittest.main()

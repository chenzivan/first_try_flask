import re
import unittest
from app import create_app, db
from app.models import User, Role


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_register_and_login(self):
        #注册
        response = self.client.post(
            '/auth/register', data={
                'email': 'someone@example.com',
                'username': 'someone',
                'password': 'mycat',
                'password2': 'mycat'
            }
        )
        self.assertEqual(response.status_code, 302)

        #登录
        response = self.client.post('/auth/login',data={
            'email':'someone@example.com',
            'password':'mycat'
        },follow_redirects=True)
        #follow_redirect=True 自动发起重定向请求，返回的是重新请求的那个状态码
        self.assertEqual(response.status_code, 200)
        # self.assertTrue(re.search(b'hello,\s+someone',response.data))
        self.assertTrue(b'You have not confirmed your account yet.' in response.data)

        #确认账户
        user = User.query.filter_by(email='someone@example.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get('/auth/confirm/{}'.format(token),follow_redirects=True)

        user.confirm(token)

        self.assertEqual(response.status_code, 200)
        print(response.data)
        self.assertTrue(b'You have confirmed your account' in response.data)

        # 登出
        response = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('你已经成功登出了！'.encode() in response.data)
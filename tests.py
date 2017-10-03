import unittest
from app.users import views
from app import app
class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_user_signup(self):
        info = dict(first_name = 'James', last_name = 'Clark',\
                    email = 'jc@gmail.com', password = 'mandelson')
        response = self.app.post('/api/user/signup', data=info)
        self.assertIn(b'',response.data)
        self.assertEqual(response.status_code, 201)
        

    def test_user_login(self):
        pass

if __name__ == '__main__':
    unittest.main()

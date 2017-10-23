import unittest
import json
from app import app, db

class TestsUsers(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    #ensure new user can be created    
    def test_add_new_user(self):
        response = self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(first_name='James',
                                                        last_name='Clark',
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        self.assertIn(u'Successfully signed up',response.data)
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)

    #ensure user name is unique
    def test_add_unique_user(self):
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(first_name='James',
                                                        last_name='Clark',
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        response = self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(first_name='James',
                                                        last_name='Clark',
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        data = json.loads(response.data.decode())
        self.assertIn(u'User already taken',data['message'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)    

    #ensure users can be got
    def test_get_users(self):
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(first_name='James',
                                                        last_name='Clark',
                                                        email='jk@gmail.com',
                                                        password='amazon')))
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(first_name='Lames',
                                                        last_name='Klark',
                                                        email='jok@gmail.com',
                                                        password='amazon')))
        response = self.tester.get('/api/user',
                                  content_type='application/json')
        data = json.loads(response.data.decode())
        user1 = [user for user in data['users'] if user['first_name']=='Lames']
        user2 = [user for user in data['users'] if user['first_name']=='James']
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'Lames', user1[0]['first_name'])
        self.assertIn(u'Clark', user2[0]['last_name'])
        


    #ensure a user can be got
    def test_valid_get_user(self):
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(first_name='James',
                                                        last_name='Clark',
                                                        email='jk@gmail.com',
                                                        password='amazon')))
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(first_name='Lames',
                                                        last_name='Klark',
                                                        email='jok@gmail.com',
                                                        password='amazon')))
        response = self.tester.get('/api/user/jok@gmail.com',
                                   content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertIn(u'Klark', response.data)
        
        self.assertEqual(response.status_code, 200)

    #ensure a non-user cant be got
    def test_invalid_get_user(self):
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(first_name='James',
                                                        last_name='Clark',
                                                        email='jk@gmail.com',
                                                        password='amazon')))
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(first_name='Lames',
                                                        last_name='Klark',
                                                        email='jok@gmail.com',
                                                        password='amazon')))
        response = self.tester.get('/api/user/<email>',
                                   content_type='application/json',
                                   data=json.dumps(dict(email='jeek@gmail.com')))
        self.assertIn(u'No user found', response.data)
        
        self.assertEqual(response.status_code, 200)
    

    #ensure user does not login without credentials
    def test_no_credentials_login_user(self):
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(first_name='James',
                                                        last_name='Clark',
                                                        email='jh@gmail.com',
                                                        password='amazon')))#pragma:no cover
        response = self.tester.post('/login',
                                    content_type='text/html')#pragma:no cover
        
        self.assertIn(u'you need to authorize with email and password',response.data)#pragma:no cover
        self.assertEqual(response.status_code, 401)#pragma:no cover

    #ensure user does not login without credentials:correct email:
    def test_auth_login_user(self):
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(first_name='James',
                                                        last_name='Clark',
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        response = self.tester.post('/login',
                                    content_type='application/json',
                                   data=json.dumps(dict(email='jm@gmail.com',
                                                      password='amazon')))
        self.assertIn(u'you need to use a correct email',response.data)
        self.assertEqual(response.status_code, 401)
    #ensure user does not login with incorrect password
    def test_invalid_login_user(self):
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(first_name='James',
                                                        last_name='Clark',
                                                        email='jh@gmail.com',
                                                        password='amazon')))#pragma:no cover
        response = self.tester.post('/login',
                                    content_type='application/json',
                                   data=json.dumps(dict(email='jh@gmail.com',
                                                      password='blizzard')))#pragma:no cover
        #data = json.loads(response.data.decode())
        self.assertIn(u'you need to authorize with correct password',response.data)#pragma:no cover
        self.assertEqual(response.status_code, 401)#pragma:no cover
        
    #ensure user_token generated on login
    def test_token_login_user(self):
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(first_name='James',
                                                        last_name='Clark',
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        response = self.tester.post('/login',
                                    content_type='application/json',
                                   data=json.dumps(dict(email='jh@gmail.com',
                                                      password='amazon')))
        data = json.loads(response.data.decode())
        self.assertTrue(data['token'])
        self.assertEqual(response.status_code, 200)
        
class TestRecipes(unittest.TestCase):
    """To test the recipe blueprint routes"""
    
    def setUp(self):
        self.tester = app.test_client(self)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    #ensure recipe can be added by logged in user
    def test_add_recipe(self):
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(first_name='James',
                                                        last_name='Clark',
                                                        email='jh@gmail.com',
                                                        password='amazon')))#pragma:no cover
        user_login = self.tester.post('/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))
        result = json.loads(user_login.data.decode())['token']
        response = self.tester.post('/api/recipe',content_type='application/json',
                                   data =json.dumps( dict(name='Chicken stew',
                                                        description='boil in vegetables')),
                                    headers =dict(x_access_token=result))#pragma:no cover
        data = json.loads(response.data.decode())#pragma:no cover
        self.assertIn(u'Successfully added recipe',response.data)#pragma:no cover
        self.assertEqual(response.status_code, 200)#pragma:no cover

    #ensure recipe does not add with invalid token
    def test_invalid_token(self):
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(first_name='James',
                                                        last_name='Clark',
                                                        email='jh@gmail.com',
                                                        password='amazon')))#pragma:no cover
        user_login = self.tester.post('/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))
        result = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1MDg2MTg2NTQsInN1YiI6MSwiZXhwIjoxNTA4NjE4NjU5fQ.CJumlDfIRJ6_93qlWzocD-B2T_TGjQcNbQKTjCyTR1E"
        response = self.tester.post('/api/recipe',content_type='application/json',
                                   data =json.dumps( dict(name='Chicken stew',
                                                        description='boil in vegetables')),
                                    headers =dict(x_access_token=result))#pragma:no cover
        data = json.loads(response.data.decode())#pragma:no cover
        self.assertIn(u'"Token is invalid"',response.data)#pragma:no cover
        self.assertEqual(response.status_code, 401)#pragma:no cover

    #ensure recipe does not add with no token
    def test_no_token(self):
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(first_name='James',
                                                        last_name='Clark',
                                                        email='jh@gmail.com',
                                                        password='amazon')))#pragma:no cover
        user_login = self.tester.post('/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))

        response = self.tester.post('/api/recipe',content_type='application/json',
                                   data =json.dumps( dict(name='Chicken stew',
                                                        description='boil in vegetables')),
                                    headers=dict(x_access_token=None))#pragma:no cover
        data = json.loads(response.data.decode())#pragma:no cover
        self.assertIn(u'"Token is invalid"',response.data)#pragma:no cover
        self.assertEqual(response.status_code, 401)#pragma:no cover
        
    #ensure error is returned when recipe fails to add
    def test_add_recipe_error(self):
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(first_name='James',
                                                        last_name='Clark',
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login=self.tester.post('/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))
        result = json.loads(user_login.data.decode())['token']
        
        self.tester.post('/api/recipe',content_type='application/json',
                         data =json.dumps( dict(name='Chicken stew',
                                                description='boil in vegetables')),
                         headers =dict(x_access_token=result))
        response = self.tester.post('/api/recipe',content_type='application/json',
                                   data =json.dumps( dict(name='Chicken stew',
                                                        description='boil in vegetables')),
                                    headers =dict(x_access_token=result))
        data = json.loads(response.data.decode())
        self.assertIn(u'An error occured try again',response.data)
        self.assertEqual(response.status_code, 200)

        
    #ensure recipes can be viewed publicly
    def test_get_recipe_list(self):
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(first_name='James',
                                                        last_name='Clark',
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))
        result = json.loads(user_login.data.decode())['token']
        self.tester.post('/api/recipe',content_type='application/json',
                                   data =json.dumps( dict(name='Chicken stew',
                                                        description='boil in vegetables')),
                         headers =dict(x_access_token=result))
        self.tester.post('/api/recipe',content_type='application/json',
                                   data =json.dumps( dict(name='Chicken stew',
                                                        description='boil in salads')),
                         headers=dict(x_access_token=result))
        response = self.tester.get('/api/recipe',
                                  content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertIn(u'Chicken stew', response.data)
        self.assertEqual(response.status_code, 200)

    #ensure single recipe can be viewed
    def test_get_recipe_single(self):
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(first_name='James',
                                                        last_name='Clark',
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))
        result = json.loads(user_login.data.decode())['token']
        self.tester.post('/api/recipe',content_type='application/json',
                                   data =json.dumps( dict(name='Chicken stew',
                                                        description='boil in vegetables')),
                         headers =dict(x_access_token=result))
        self.tester.post('/api/recipe',content_type='application/json',
                                   data =json.dumps( dict(name='Beef stew',
                                                        description='boil in vegetables')),
                         headers =dict(x_access_token=result))
        self.tester.post('/api/recipe',content_type='application/json',
                                   data =json.dumps( dict(name='Beans stew',
                                                        description='boil in oil with salads')),
                         headers =dict(x_access_token=result))
        response = self.tester.get('/api/recipe/<name>',
                                   content_type='application/json',
                                   data = json.dumps(dict(name='Chicken stew')))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'boil in vegetables', response.data)

    #ensure error is returned if recipe does not exist
    def test_get_recipe(self):
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(first_name='James',
                                                        last_name='Clark',
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))
        result = json.loads(user_login.data.decode())['token']
        self.tester.post('/api/recipe',content_type='application/json',
                                   data =json.dumps( dict(name='Chicken stew',
                                                        description='boil in vegetables')),
                         headers =dict(x_access_token=result))
        self.tester.post('/api/recipe',content_type='application/json',
                                   data =json.dumps( dict(name='Beef stew',
                                                        description='boil in vegetables')),
                         headers =dict(x_access_token=result))

        response = self.tester.get('/api/recipe/<name>',
                                   content_type='application/json',
                                   data = json.dumps(dict(name='Chicken and fries')))
        data = json.loads(response.data.decode())        
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'recipe does not exist', response.data)
    
    #ensure recipe can be edited by logged in user
    def test_edit_recipe(self):
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(first_name='James',
                                                        last_name='Clark',
                                                        email='jh@gmail.com',
                                                        password='amazon')))#pragma:no cover
        user_login = self.tester.post('/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))
        result = json.loads(user_login.data.decode())['token']
        self.tester.post('/api/recipe',content_type='application/json',
                                   data =json.dumps( dict(name='Chicken stew',
                                                        description='boil in vegetables')),
                         headers =dict(x_access_token=result))
        self.tester.post('/api/recipe',content_type='application/json',
                                   data =json.dumps( dict(name='Beef stew',
                                                        description='boil in vegetables')),
                         headers =dict(x_access_token=result))
        response = self.tester.put('/api/recipe/<name>', content_type='application/json',
                                   data=json.dumps(dict(name='Beef stew',
                                                        new_name='Beef fries',
                                                        new_description='boil in vegetables')),
                                   headers=dict(x_access_token=result))#pragma:no cover
        data = json.loads(response.data.decode())#pragma:no cover
        self.assertEqual(response.status_code, 200)#pragma:no cover
        self.assertIn(u'Successfully edited', response.data)#pragma:no cover

    #ensure recipe can be edited by logged in user
    def test_fail_edit_recipe(self):
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(first_name='James',
                                                        last_name='Clark',
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))
        result = json.loads(user_login.data.decode())['token']
        self.tester.post('/api/recipe',content_type='application/json',
                                   data =json.dumps( dict(name='Chicken stew',
                                                        description='boil in vegetables')),
                         headers =dict(x_access_token=result))
        self.tester.post('/api/recipe',content_type='application/json',
                                   data =json.dumps( dict(name='Beef stew',
                                                        description='boil in vegetables')),
                         headers =dict(x_access_token=result))

        response = self.tester.put('/api/recipe/<name>', content_type='application/json',
                                   data=json.dumps(dict(name='Beef stews',
                                                        new_name='Beef fries',
                                                        new_description='boil in vegetables')),
                                   headers=dict(x_access_token=result))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertIn(u'"Recipe non exitent', response.data)
        
    #ensure  recipe can be deleted by logged in user
    def test_delete_recipe(self):
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(first_name='James',
                                                        last_name='Clark',
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))
        result = json.loads(user_login.data.decode())['token']
        self.tester.post('/api/recipe',content_type='application/json',
                                   data =json.dumps( dict(name='Chicken stew',
                                                        description='boil in vegetables')),
                         headers =dict(x_access_token=result))
        self.tester.post('/api/recipe',content_type='application/json',
                                   data =json.dumps( dict(name='Beef stew',
                                                        description='boil in vegetables')),
                         headers =dict(x_access_token=result))
        response = self.tester.delete('/api/recipe/<name>', content_type='application/json',
                                   data=json.dumps(dict(name='Beef stew')),
                                      headers=dict(x_access_token=result))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'successfully deleted', response.data)

    #ensure error message sent if recipe is non existent
    def test_delete_recipe_error(self):
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(first_name='James',
                                                        last_name='Clark',
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))
        result = json.loads(user_login.data.decode())['token']
        self.tester.post('/api/recipe',content_type='application/json',
                                   data =json.dumps( dict(name='Chicken stew',
                                                        description='boil in vegetables')),
                         headers =dict(x_access_token=result))
        self.tester.post('/api/recipe',content_type='application/json',
                                   data =json.dumps( dict(name='Beef stew',
                                                        description='boil in vegetables')),
                         headers =dict(x_access_token=result))
        response = self.tester.delete('/api/recipe/<name>', content_type='application/json',
                                   data=json.dumps(dict(name='Beef stews')),
                                      headers=dict(x_access_token=result))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'Recipe does not exist', response.data)


if __name__ == '__main__':
    unittest.main()

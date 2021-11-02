from django.http import request
import jwt, json

from django.test                    import TestCase, Client, client
from unittest.mock                  import MagicMock, patch

from users.models                   import User
from my_settings                    import SECRET_KEY


class UserTest(TestCase):
    def setUp(self):
        self. maxDiff = None
        user = User.objects.create(
            email = "dodam@wanted.com",
            password = "wanted1!!"
        )
  
    def tearDown(self):
        User.objects.all().delete()
        
    def test_join_success(self):
            client = Client()
            user = {
                'user' :'dd',
                'email' : 'dodam123@wanted.com',
                'password' : 'password1!',
                'phone_number' : '01023456787'
            }	
            response = client.post('/users/join', json.dumps(user), content_type='application/json')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), 
                {
                    "MESSAGE" : "SUCCESS"
                }
            )

    def test_duplicate_email(self):
            client = Client()
            user = {
                'email' : 'dodam@wanted.com',
                'password' : 'password1!'
            }
            response = client.post('/users/join', json.dumps(user), content_type='application/json')

            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(),
                {
                    "MESSAGE" : "EXIST_DATA"
                }
            )



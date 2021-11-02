import json, jwt

from django.test       import TestCase, Client
from django.test.utils import teardown_databases

from users.models      import User
from posts.models      import Post
from my_settings       import SECRET_KEY


class PostTest(TestCase):
    def setUp(self):
        self. maxDiff = None
        user = User.objects.create(
            email = "dodam@wanted.com",
            password = "wanted1!!"
        )

        post = Post.objects.bulk_create(
            [Post(
                user_id = user.id,
                title   = "게시판에 글을 쓰기",
                comment = "테스트 화이팅!"
            ),
                Post(
                    user_id = user.id,
                    title = "게시판에 글을 쓰자아",
                    comment = "테스트 화이팅!"
                ),

                Post(
                    user_id = user.id,
                    title = "10/27 지원마감",
                    comment = "테스트 화이팅!"
                ),
            ]
        )
           
    def tearDown(self):
        User.objects.all().delete()
        Post.objects.all().delete()
        
    def test_PostView_success(self):
        client = Client()
        response = client.get('/posts/2',content_type = 'application/json') 

        self.assertEqual(response.status_code,200)        
        
    def test_PostView_error(self):
        client = Client()
        response = client.get('/posts/', content_type= 'application/json')

        self.assertEqual(response.status_code,404)    
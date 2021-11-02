import json
import bcrypt

from django.http  import response
from users.models import User

from .models        import Category, Post, Comment, DetailComment
from django.test    import TestCase, Client

class Post_Test(TestCase):
    def setUp(self):
        Post.objects.create(
            id          = 1,
            user_id     = User.objects.get(id=1),
            category_id = Category.objects.get(id=1),
            title       = '프리온보딩1',
            content     = 'aimmo project'
        )
        Post.objects.create(
            [Post(
                id          = 1,
                user_id     = User.objects.get(id=1),
                category_id = Category.objects.get(id=1),
                title       = '프리온보딩1',
                content     = 'aimmo project'
            )]
        )
    def tearDown(self):
        Post.objects.all().delete()

    def test_postview_post_success(self):
        client = Client()

        post = {
            'tittle'  : '제목',
            'content' : '내용',
            'created_at' : Post.objects.get(id=1).created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

        response = client.post('/posts', json.dumps(post, content_type = 'application/json'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
            'message' : 'SUCCESS'
            }
        )

    def test_postview_post_jsondecode_error(self):
        client = Client()
            
        response = client.post('/post')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'meesage' : 'JSON_DECODE_EROOR'
            }
        )
    
    def test_postview_post_key_error_content(self):
        client = Client() 

        post = {
            'tittle' : '제목'
        }

        response = client.post('/posts', json.dumps(post), content_type= 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
         {
            'message' : 'KEY_ERROR'
         }
        )

    def test_postview_get_success(self):
        client = Client()

        result = [
            {
                'post_id'    : 1,
                'user'       : '김프로',
                'title'      : '타이틀1',
                "created_at" : Post.objects.get(id=1).created_at.strftime('%Y-%m-%d %H:%M:%S')
            },
            {
                'post_id'    : 2,
                'user'       : '김아마',
                'title'      : '타이틀2',
                "created_at" : Post.objects.get(id=1).created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        ]

        response = client.get('/posts')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result' : result})

    def test_postdetailview_get_success(self):
        client = Client()

        data = {
            'post_id' : 1,
            'user'    : '김프로',
            'title'   : '타이틀1',
            'content' : '냉무',
            'created_at' : Post.objects.get(id=1).created_at.striftime('%Y-%m-%d %H:%M:%S')
        }

        response = client.get('/posts/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'data' : data})

    def test_postdetailview_get_post_does_not_exist(self):
        client = Client()

        response = client.get('/posts/3')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()), {'message' : 'POST_NOT_FOUND'}

    def test_postdetailview_delete_success(self):
        client = Client()

        response = client.delete('/posts/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'SUCCESS'})

    def test_postdetailview_patch_success(self):
        client = Client()

        post = {
            'title'   : '타이틀 수정',
            'content' : '내용 수정'
        }

        response = client.patch('/posts/1', json.dumps(post), content_type = 'application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        {
            'message' : 'SUCCESS'
        }
        )
        
    def test_postdetailview_patch_post_jsondecode_error(self):
        client = Client

        response = client.patch('/posts/1')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'JSON_DECODE_ERROR'
            }
        )

class Comment_Test(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
            name     = '정지훈',
            email    = 'jung1@gmail.com',
            password = 'm111111!'
        )
        
        Post.objects.create(
            id          = 1,
            user_id     = User.objects.get(id=1),
            category_id = Category.objects.get(id=1),
            title       = '프리온보딩1',
            content     = 'aimmo project'
        )
        
        Comment.objects.create(
            id         = 1,
            user_id    = User.objects.get(id=1),
            post_id    = Post.objects.get(id=1),
            comment    = 'aimmo project'
        )        
        
    def tearDown(self):
        User.objects.all().delete()
        Comment.objects.all().delete()

    def test_commentview_post_success(self):
        client = Client()

        post = {
            'comment' : '내용',
        }

        response = client.post('/posts/1/comments', json.dumps(post, content_type = 'application/json'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
            'message' : 'SUCCESS'
            }
        )

    def test_commentview_post_jsondecode_error(self):
        client = Client()
            
        response = client.post('/posts/1/comments')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'meesage' : 'JSON_DECODE_EROOR'
            }
        )
    
    def test_commentview_post_key_error_content(self):
        client = Client() 

        post = {
            'comment' : '제목'
        }

        response = client.post('/posts/1/comments', json.dumps(post), content_type= 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
         {
            'message' : 'KEY_ERROR'
         }
        )

    def test_commentview_get_success(self):
        client = Client()

        comment_list = [
            {
                'user_name'  : '김프로',
                'comment'    : '타이틀1',
                "created_at" : Comment.objects.get(id=1).created_at.strftime('%Y-%m-%d %H:%M:%S')
            },
            {
                'user_name'  : '김아마',
                'comment'    : '타이틀2',
                "created_at" : Comment.objects.get(id=1).created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        ]

        response = client.get('/posts/1/comments')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'comment_list' : comment_list})

    def test_commentview_get_post_does_not_exist(self):
        client = Client()

        response = client.get('/posts/3/comments')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()), {'message' : 'INVALID_POST_ID'}

    def test_commentmodifylview_delete_success(self):
        client = Client()

        response = client.delete('/posts/comments/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'SUCCESS'})

    def test_commentmodifyview_patch_success(self):
        client = Client()

        post = {
            'comment'   : '내용 변경'
        }

        response = client.patch('/posts/comments/1', json.dumps(post), content_type = 'application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        {
            'message' : 'SUCCESS'
        }
        )
        
    def test_commentmodifyview_patch_post_jsondecode_error(self):
        client = Client

        response = client.patch('/posts/comments/1')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'JSON_DECODE_ERROR'
            }
        )

class DetailComment_Test(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
            name     = '정지훈',
            email    = 'jung1@gmail.com',
            password = 'm111111!'
        )
        
        Comment.objects.create(
            id             = 1,
            user_id        = User.objects.get(id=1),
            comment_id     = Comment.objects.get(id=1),
            detail_comment = 'aimmo project'
        )
        
        DetailComment.objects.create(
            [DetailComment(
                id             = 1,
                user_id        = User.objects.get(id=1),
                comment_id     = Comment.objects.get(id=1),
                detail_comment = 'aimmo project'
            )]
        )

    def tearDown(self):
        User.objects.all().delete()
        Comment.objects.all().delete()
        DetailComment.objects.all().delete()

    def test_detailcommentview_post_success(self):
        client = Client()

        post = {
            'detail_comment' : '내용',
        }

        response = client.post('/comments/1/detailcomments', json.dumps(post, content_type = 'application/json'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
            'message' : 'SUCCESS'
            }
        )

    def test_dtailcommentview_post_jsondecode_error(self):
        client = Client()
            
        response = client.post('/comments/1/detailcomments')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'meesage' : 'JSON_DECODE_EROOR'
            }
        )
    
    def test_detailcommentview_post_key_error_content(self):
        client = Client() 

        post = {
            'comment' : '제목'
        }

        response = client.post('/comments/1/detailcomments', json.dumps(post), content_type= 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
         {
            'message' : 'KEY_ERROR'
         }
        )

    def test_detailcommentview_get_success(self):
        client = Client()

        detail_comment_list = [
            {
                'user_name'      : '김프로',
                'detail_comment' : '디테일코멘트1',
                'created_at'     : DetailComment.objects.get(id=1).created_at.strftime('%Y-%m-%d %H:%M:%S')
            },
            {
                'user_name'      : '김아마',
                'detail_comment' : '디테일코멘트2',
                'created_at'     : DetailComment.objects.get(id=1).created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        ]

        response = client.get('/comments/1/detailcomments')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'detail_comment_list' : detail_comment_list})

    def test_detailcommentview_get_post_does_not_exist(self):
        client = Client()

        response = client.get('/comments/1/detailcomments')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()), {'message' : 'INVALID_POST_ID'}

    def test_detailcommentmodifylview_delete_success(self):
        client = Client()

        response = client.delete('/comments/detailcomments/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'SUCCESS'})

    def test_detailcommentmodifyview_patch_success(self):
        client = Client()

        post = {
            'comment'   : '내용 변경'
        }

        response = client.patch('/comments/detailcomments/1', json.dumps(post), content_type = 'application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        {
            'message' : 'SUCCESS'
        }
        )

    def test_detialcommentmodifyview_patch_post_jsondecode_error(self):
        client = Client

        response = client.patch('/comments/detailcomments/1')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'JSON_DECODE_ERROR'
            }
        )
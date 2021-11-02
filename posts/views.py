import json
from json.decoder import JSONDecodeError

from django.http  import JsonResponse
from django.views import View
from django.db    import transaction

from posts.models import Category, Post, Comment, DetailComment
from users.utils  import login_decorator

class PostView(View):
    @login_decorator
    def post(self, request):
        try:
            data     = json.loads(request.body)
            user     = request.user
            category = data['category_id']
            title    = data['title']
            content  = data['content']

            Post.objects.create(
                user_id     = user.id,
                category_id = category,
                title       = title,
                content     = content
            )
            return JsonResponse({'data': data}, status=201)

        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
    
    def get(self, request):
        try:
            limit  = int(request.GET.get('limit', 10))
            offset = int(request.GET.get('offset', 0))
            #TODO: 카테고리 필터링
            #TODO: 검색

            if limit > 10:
                return JsonResponse({'message':'TOO_MUCH_LIMIT'}, status=400)

            posts  = Post.objects.all()[offset:offset+limit]

            result = [{
                'post_id'    : post.id,
                'user'       : post.user.name,
                'title'      : post.title,
                "created_at" : post.created_at,
                "updated_at" : post.updated_at
                } for post in posts]
            return JsonResponse({'count': len(posts), 'data':result}, status=200)

        except ValueError:
            return JsonResponse({'message':'VALUE_ERROR'}, status=400)

class PostDetailView(View):
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            #TODO: 조회수 증가
            data = {
                    'post_id'    : post.id,
                    'user'       : post.user.name,
                    'title'      : post.title,
                    'content'    : post.content,
                    "created_at" : post.created_at,
                    "updated_at" : post.updated_at
                }
            return JsonResponse({'data': data}, status=200)

        except Post.DoesNotExist:
            return JsonResponse({'message' : 'POST_NOT_FOUND'}, status=404)

    @login_decorator
    @transaction.atomic
    def patch(self, request, post_id):
        try:
            data    = json.loads(request.body)
            user    = request.user
            title   = data['title']
            content = data['content']

            if not Post.objects.filter(id=post_id, user=user).exists():
                return JsonResponse({'message':'INVALID_POST_ID'}, status=404)

            post = Post.objects.get(id=post_id, user=user)

            post.content = content
            post.title   = title
            post.save()
            return JsonResponse({'message':'UPDATED'}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

    @login_decorator
    def delete(self, request, post_id):

        user = request.user

        if not Post.objects.filter(id=post_id, user=user).exists():
            return JsonResponse({'message':'INVALID_POST_ID'}, status=404)

        post = Post.objects.get(id=post_id, user=user)
            
        post.delete()
        return JsonResponse({'message': f'post_id {post_id} is DELETED'}, status=200)

class CommentView(View):
    @login_decorator
    def post(self, request, post_id):
        try:
            if not Post.objects.filter(id = post_id).exists() :
                return JsonResponse({'message' : 'INVALID_PRODUCT_ID'}, status = 404)

            data   = json.loads(request.body)
            user   = request.user

            Comment.objects.create(
                user_id = user.id,
                post_id = post_id,
                comment = data['comment']
                )

            return JsonResponse({'message':'SUCCESS'}, status = 201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)

        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status = 400)

    def get(self, request, post_id):
        try :
            if not Post.objects.filter(id = post_id).exists() :
                    return JsonResponse({'message' : 'INVALID_PRODUCT_ID'}, status = 404)

            limit   = int(request.GET.get('limit', 5))
            offset  = int(request.GET.get('offset', 0))

            comments = Comment.objects.filter(post_id=post_id).order_by('-created_at')
            
            if limit :
                limit    = offset + limit
                comments = comments[offset : limit]
            
            comment_list = [{
                'user_name'     : comment.user.name,
                'comment'       : comment.comment,
                'created_at'    : comment.created_at,
            } for comment in comments]
            
            return JsonResponse({'DATA' : comment_list}, status = 200)

        except Post.DoesNotExist :
            return JsonResponse({'message' : 'INVALID_POST_ID'}, status = 404)

        except Post.MultipleObjectsReturned :
            return JsonResponse({'message' : 'MULTIPLE_OBJECTS_ERROR'}, status = 400)

class CommentModifyView(View):
    @login_decorator
    def delete(self, request, comment_id):
        try:
            user = request.user
            if not Comment.objects.filter(id=comment_id).exists():
                return JsonResponse({'message' : 'INVALID_REVIEW_ID'}, status=404)
            
            comment = Comment.objects.get(id=comment_id)
            
            if user.id != comment.user.id :
                return JsonResponse({'message' : 'INVALID_USER'}, status = 401)
            
            comment.delete()
            
            return JsonResponse({'meassage' : 'SUCCESS'}, status = 201)

        except Comment.DoesNotExist :
            return JsonResponse({'message' : 'INVALID_REVIEW_ID'}, status = 404)

        except Comment.MultipleObjectsReturned :
            return JsonResponse({'message' : 'MULTIPLE_OBJECTS_ERROR'}, status = 400)

    @login_decorator
    def patch(self, request, comment_id):
        try :
            user = request.user
            data = json.loads(request.body)
            if not Comment.objects.filter(id=comment_id).exists():
                return JsonResponse({'message' : 'INVALID_COMMENT_ID'}, status = 404)
            
            comment = Comment.objects.get(id=comment_id)
            
            if user.id != comment.user.id:
                return JsonResponse({'message' : 'INVALID_USER'}, status = 401)
            
            comment.comment = data.get('comment', comment.comment)
            comment.save()
            
            return JsonResponse({'message' : 'SUCCESS'}, status = 201)

        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)

        except Comment.DoesNotExist :
            return JsonResponse({'message' : 'INVALID_COMMENT_ID'}, status = 404)

        except Comment.MultipleObjectsReturned :
            return JsonResponse({'message' : 'MULTIPLE_OBJECTS_ERROR'}, status = 400)

class DetailCommentView(View):
    @login_decorator
    def post(self, request, comment_id):
        try :
            if not Comment.objects.filter(id = comment_id).exists() :
                return JsonResponse({'messages' : 'INVALID_COMMENT_ID'}, status = 404)
        
            data = json.loads(request.body)
            user = request.user
        
            DetailComment.objects.create(
                user_id        = user.id,
                comment_id     = comment_id,
                detail_comment = data['detail_comment']
            )
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except Comment.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_COMMENT_ID'}, status = 404)

        except Comment.MultipleObjectsReturned :
            return JsonResponse({'message' : 'MULTIPLE_OBJECTS_ERROR'}, status = 400)

        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)
    
    def get(self, request, comment_id):
        
        if not Comment.objects.filter(id = comment_id).exists():
            return JsonResponse({'messages' : 'INVALID_COMMENT_ID'}, status = 404)
        
        detail_comments_list = [{
            'user_name'      : comment.user.name,
            'detail_comment' : comment.detail_comment,
            'created_at'     : comment.created_at,
        }for comment in DetailComment.objects.filter(comment_id = comment_id)]
        
        return JsonResponse({'detail_comments_list' : detail_comments_list }, status = 200)

class DetailCommentModifyView(View):
    @login_decorator
    def delete(self, request, detail_comment_id):
        try :
            user = request.user
            if not DetailComment.objects.filter(id = detail_comment_id).exists() :
                return JsonResponse({'message' : 'INVALID_DETAIL_COMMENT_ID'}, status = 404)
        
            detail_comment = DetailComment.objects.get(id = detail_comment_id)
            if user.id != detail_comment.user.id :
                return JsonResponse({'message' : 'UNAUTHORIZED'}, status = 401)
        
            detail_comment.delete()
        
            return JsonResponse ({'message' : 'SUCCESS'}, status = 200)

        except DetailComment.DoesNotExist :
            return JsonResponse({'message' : 'INVALID_DETAIL_COMMENT_ID'}, status = 404)

        except DetailComment.MultipleObjectsReturned :
            return JsonResponse({'message' : 'MULTIPLE_OBJECTS_ERROR'}, status = 400)

    @login_decorator
    def patch(self, request, detail_comment_id):
        try :
            user = request.user
            data = json.loads(request.body)
            
            if not DetailComment.objects.filter(id = detail_comment_id).exists() :
                return JsonResponse({'message' : 'INVALID_DETAIL_COMMENT_ID'}, status = 404)
            
            detail_comment = DetailComment.objects.get(id = detail_comment_id)
            
            if user.id != detail_comment.user.id :
                return JsonResponse({'message' : 'UNAUTHORIZED'}, status = 401)
        
            detail_comment.detail_comment = data.get('detail_comment', detail_comment.detail_comment)
            detail_comment.save()
        
            return JsonResponse({'message' : 'SUCCESS'}, status = 201)

        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)

        except DetailComment.DoesNotExist :
            return JsonResponse({'message' : 'INVALID_DETAIL_COMMENT_ID'}, status = 404)

        except DetailComment.MultipleObjectsReturned :
            return JsonResponse({'message' : 'MULTIPLE_OBJECTS_ERROR'}, status = 400)
from django.urls import path

from posts.views import (PostView,
    PostDetailView, 
    CommentView, 
    CommentModifyView, 
    DetailCommentView, 
    DetailCommentModifyView)

urlpatterns = [
    path('', PostView.as_view()),
    path('/<int:post_id>', PostDetailView.as_view()),
    path('/<int:post_id>/comments', CommentView.as_view()),
    path('/comments/<int:comment_id>', CommentModifyView.as_view()),
    path('/comments/<int:comment_id>/detailcomments', DetailCommentView.as_view()),
    path('/comments/detailcomments/<int:detail_comment_id>', DetailCommentModifyView.as_view())
]
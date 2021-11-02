from django.db    import models

from users.models import User

class Category(models.Model):
    name = models.CharField(max_length=30)

class Post(models.Model):
    title      = models.CharField(max_length=100)
    content    = models.TextField()
    category   = models.ForeignKey(Category, on_delete=models.CASCADE)
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=False)

    class Meta:
        db_table = 'posts'
        
class Comment(models.Model):
    comment    = models.CharField(max_length=500)
    post       = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=False)
    
    class Meta:
        db_table = 'comments'
    
class DetailComment(models.Model):
    detail_comment = models.CharField(max_length=500)
    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    comment        = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at     = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=False)
    
    class Meta:
        db_table = 'detail_comments'
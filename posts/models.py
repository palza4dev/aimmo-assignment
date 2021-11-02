from django.db    import models

from users.models import User

class Category(models.Model):
    name = models.CharField(max_length=30)

class Post(models.Model):
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    category = models.CharField(max_length=50)
    user     = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'posts'
        
class Comment(models.Model):
    comment         = models.CharField(max_length=500)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    post            = models.ForeignKey(Post, on_delete=models.CASCADE)
    #parents_comment = models.ForeignKey()
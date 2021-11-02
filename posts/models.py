from django.db    import models

class Post(models.Model):
    user            = models.ForeignKey('users.User', on_delete=models.CASCADE)
    title           = models.CharField(max_length=45)
    comment         = models.CharField(max_length=2000, null=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True, null=True)

    class Meta:
	    db_table = 'posts'
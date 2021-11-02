from django.db import models

class Comment(models.Model):
    user       = models.ForeignKey("user.User", on_delete=models.CASCADE)
    post       = models.ForeignKey("Posts", on_delete=models.CASCADE)
    content    = models.TextField()
    reply      = models.ForeignKey('self', on_delete = models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    solution   = models.BooleanField(default=False)
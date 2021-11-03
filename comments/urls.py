from django.urls import path
from .views import CommentView, ReplyView

urlpatterns = [ 
	path('/post/<int:post_id>/comment', CommentView.as_view(),ReplyView.as_view()) 
]
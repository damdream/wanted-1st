from django.urls import path
from .views import PostingView

urlpatterns = [ 
	path ('', PostingView.as_view()),
	path ('/<int:post_id>', PostingView.as_view()),
]
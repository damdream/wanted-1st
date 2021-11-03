import json
from django import views
from django.core           import paginator

from django.http           import JsonResponse, request
from django.views          import View

from users.models          import User
from posts.models          import Post
from .models               import Comment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from users.utils           import login_decorator

class CommentView(views):
    @login_decorator
    def post(self, request):
        try :
            data = json.loads(request.body)
        
            if not User.objects.filter(email=data["email"]).exists():
                return JsonResponse({"MESSAGE":"INVALID_USER"}, status=400)

            if not Post.objects.filter(id = data["post"]).exists():
                return JsonResponse({"MESSAGE":"NO_POST"}, status=400)

            if data["comment"] == "" :
                return JsonResponse({"MESSAGE":"NULL_COMMENTS"}, status = 400)

            Comment.objects.create( 
                user            = request.user,
                post            = request.post,
                content         = data["comment"],
            )

            return JsonResponse({"MESSAGE":"SUCCESS"}, status = 201)

        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status = 400)   


    def get(self, request, post_id):
        comments = Comment.objects.filter(post_id = post_id)
        comment_list = Comment.objects.all().order_by('id')
        paginator = Paginator(comment_list, 3)
        page      = int(request.GET.get('page',1))

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        results = []

        for comment in comments:
            results.append(
                {
                    "user"          : comment.user,
                    "comment"       : comment.comment,
                }
            )
        return JsonResponse ({"page" :page, "result": results}, status = 200)     

class ReplyView(views):
    @login_decorator
    def post(self, request, board_pk, reply_pk):
        try:
            data  = json.loads(request.body)
            user  = request.user
            post  = Post.objects.get(id=board_pk)

            if data['content']=="":
                return JsonResponse({'MESSAGE':'EMPTY_CONTENT'})
            else:
                Comment.objects.create(
                    user_id  = user.id,
                    post     = post,
                    content  = data['content'],
                    reply_id = reply_pk
                )

            return JsonResponse({'MESSAGE': 'SELF_COMMENT_CREATE'}, status=200)       

        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status = 400)   


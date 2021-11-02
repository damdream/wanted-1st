import json
from django.core import paginator

from django.http           import JsonResponse, request
from django.views          import View
from django.db.models      import Q
from users.models          import User
from posts.models          import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from users.utils           import login_decorator

class PostingView(View):
    @login_decorator    
    def post(self,request):
        try:
            data = json.loads(request.body)

            if data["title"] == "" :
                return JsonResponse({"MESSAGE":"NULL_POSTS"}, status = 400)

            Post.objects.create( 
                user            = request.user,
                title           = data["title"],
                comment         = data["comment"],
                category        = data["category"]
            )

            return JsonResponse({"MESSAGE":"SUCCESS"}, status = 201)

        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status = 400)    

    def get(self,request,post_id):
        post_list = Post.objects.all().order_by('id')
        paginator = Paginator(post_list, 3)
        page      = int(request.GET.get('page',1))

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        result = [
            {
                "user"            : post.user.id,
                "created_at"      : post.created_at,
                "title"           : post.title,
                "comment"         : post.comment,

            } for post in posts]

        return JsonResponse ({"page" :page,"result": result}, status = 200)

    @login_decorator
    def delete (self,request,post_id):

        if not Post.objects.filter(id=post_id, user = request.user).exists():
            return JsonResponse({"MESSAGE": "NO_REVIEWS"}, status = 400)

        Post.objects.filter(id=post_id).delete()

        return JsonResponse ({"MESSAGE" : "DELETE"}, status = 204)    

    @login_decorator
    def patch (self,request, post_id):
        try:
            data = json.loads(request.body)

            if not Post.objects.filter(id=post_id, user = request.user).exists():
              return JsonResponse({"MESSAGE": "NO_REVIEWS"}, status = 400)
    
            Post.objects.filter(id=post_id).update(title= data["title"], comment= data["comment"])
            return JsonResponse ({"MESSAGE" : "UPDATE"}, status = 200)

        except KeyError: 
            return JsonResponse ({"MESSAGE":"KEY_ERROR"},status = 400)
import sqlite3
import json, re, bcrypt, jwt

from django.views        import View
from django.http         import JsonResponse, request

from users.models        import User

from preonboarding.settings import SECRET_KEY  

email_ragular    = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
password_regular = re.compile('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,12}$')

class JoinView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
           
            if (not email_ragular.match(data["email"])) or (not password_regular.match(data["password"])):
                return JsonResponse ({"MESSAGE":"INVALID_FORMAT"}, status = 400)
                
            if (User.objects.filter(email=data["email"]).exists()) or (User.objects.filter(phone_number=data['phone_number']).exists()):
                return JsonResponse ({"MESSAGE": "EXIST_DATA"}, status = 400)
                
            bcrypt_password = bcrypt.hashpw(data["password"].encode("utf-8"),bcrypt.gensalt()). decode("utf-8")    
            
            user = User.objects.create(
                user         = data["user"],
                email        = data["email"],
                password     = bcrypt_password,
                phone_number = data["phone_number"],
            )
            
            return JsonResponse ({"MESSAGE":"SUCCESS"}, status = 200)
        
        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status = 400)

class LoginView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)

            if data["email"] == "" or data["password"] == "" :
                return JsonResponse ({"MESSAGE": "INVALID_REQUEST"},status = 400)    

            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse ({"MESSAGE":"USER_DOES_NOT_EXIST"}, status =401)
    
            user     = User.objects.get(email=data["email"])
            password = user.password.encode("utf-8")

            if not bcrypt.checkpw(data["password"].encode("utf-8"),password) :
                return JsonResponse ({"MESSAGE":"USER_DOES_NOT_EXIST"},status = 401)

            access_token = jwt.encode({"id": user.id}, SECRET_KEY, algorithm="HS256")
            return JsonResponse ({"access_token": access_token,"MESSAGE":"SUCCESS"}, status = 200)

        except KeyError:
            return JsonResponse ({"MESSAGE":"KEY_ERROR"},status = 400)    

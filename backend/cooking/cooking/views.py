# from django.views import View
# from django.http import JsonResponse

# class RedirectSocial(View):
    
#     def get(self, request, *args, **kwargs):
#         code, state = str(request.GET['code']), str(request.GET['state'])
#         # code = str(request.GET['code'])
#         # state = str(request.GET['state'])
#         json_obj = {'code': code, 'state': state}
#         print(json_obj)
#         return JsonResponse(json_obj)

"""
http://localhost:8000/http:/localhost:8080/google?state=2oKiQDXPWlCUPf1luxYji4AIn6s4UHpS&code=4%2F0AX4XfWiJ0eomdYK0W7fJTIZv9uSoXDpeC39IFNoN9qwNDZIW7D0B2NFMdMJTV_Q3MN9irg&scope=email%20profile%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile%20openid&authuser=0&prompt=consent

"""        
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.contrib import messages
from django.contrib.auth import logout


User = get_user_model()


class CheckIdBanned(MiddlewareMixin):
    def process_request(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # print('user is authenticated')
            if request.user.is_banned:
                print("this user is banned!!!!!")
                try:
                    messages.add_message(request, messages.WARNING, 'This account is baned')
                except messages.MessageFailure:
                    pass
                logout(request)
                return HttpResponseRedirect('/')

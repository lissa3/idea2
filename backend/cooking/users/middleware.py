from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.contrib import messages
from django.contrib.auth import logout
import logging
logger = logging.getLogger('user_issues')

User = get_user_model()


class CheckIdBanned(MiddlewareMixin):
    def process_request(self, request, *args, **kwargs):
        # print("inside middelware")
        if request.user.is_authenticated:
            print('user is authenticated')
            if request.user.is_banned:
                print("this user is banned")
                try:
                    messages.add_message(request, messages.WARNING, 'This account is baned')
                    logger.error(f"banned user access {request.user.id}")
                except messages.MessageFailure:
                    pass
                logout(request)
                logger.error(f"banned user is loged out {request.user.id}")
                return HttpResponseRedirect('/')

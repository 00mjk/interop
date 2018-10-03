"""Interoperability login view."""

import logging
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.generic import View

logger = logging.getLogger(__name__)


class Login(View):
    """Logs the user in with a POST request using the given parameters.

    This view performs the login process for the user. The POST paramters must
    include 'username' and 'password'. Users can programatically send a login
    request to this view which will return a cookie containing the session ID.
    Users then send this cookie with each request to make requests as an
    authenticated user.
    """

    def post(self, request):
        # Attempt authentication
        try:
            username = request.POST['username']
            password = request.POST['password']
        except KeyError:
            # Failed to get POST parameters, invalid request
            logger.warning(
                'Did not specify username & password in login request.')
            return HttpResponseBadRequest(
                'Login must be POST request with '
                '"username" and "password" parameters.')

        # Use credentials to authenticate
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Successful authentication with active user, login
            login(request, user)
            logger.info('User logged in: %s.' % user.username)
            return HttpResponse('Login Successful.')
        else:
            # Invalid user credentials, invalid request
            logger.warning('Invalid credentials in login request.')
            logger.debug(request)
            return HttpResponse('Invalid Credentials.', status=401)

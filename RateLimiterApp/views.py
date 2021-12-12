from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from RateLimiterApp.models import *
from RateLimiterApp.constants import *

from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required

from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Count
from django.conf import settings


import json
import os
import datetime
import requests

logger = logging.getLogger(__name__)


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return


class CreateUserAPI(APIView):

    def post(self, request, *args, **kwargs):

        response = {}
        response['status'] = 500
        try:

            data = request.data
            logger.info("CreateUserAPI: %s", str(data))

            username = data["username"]
            password = data["password"]

            CustomUser.objects.create(username=username, password=password)
            response['status'] = 200

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("CreateUserAPI: %s at %s", e, str(exc_tb.tb_lineno))

        return Response(data=response)


class DeleteUserAPI(APIView):

    def post(self, request, *args, **kwargs):

        response = {}
        response['status'] = 500
        try:

            data = request.data
            logger.info("DeleteUserAPI: %s", str(data))

            username = data["username"]

            custom_user_obj = CustomUser.objects.get(username=username)
            custom_user_obj.delete()

            response['status'] = 200

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("DeleteUserAPI: %s at %s", e, str(exc_tb.tb_lineno))

        return Response(data=response)


class ListUsersAPI(APIView):

    def post(self, request, *args, **kwargs):

        response = {}
        response['status'] = 500
        try:

            data = request.data
            logger.info("ListUsersAPI: %s", str(data))

            custom_user_objs = CustomUser.objects.all()

            user_list = []
            for custom_user_obj in custom_user_objs:
                temp_dict = {}
                temp_dict["username"] = custom_user_obj.username
                user_list.append(temp_dict)

            response["user_list"] = user_list
            response['status'] = 200

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("ListUsersAPI: %s at %s", e, str(exc_tb.tb_lineno))

        return Response(data=response)


class TestAPI(APIView):

    def get(self, request, *args, **kwargs):

        response = {}
        response['status'] = 500
        try:
            logger.info("TestAPI:")

            response['status'] = 200

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("TestAPI: %s at %s", e, str(exc_tb.tb_lineno))

        return Response(data=response)
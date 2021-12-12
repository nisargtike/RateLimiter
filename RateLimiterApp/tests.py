from django.test import TestCase
from RateLimiterApp.models import CustomUser
from rest_framework.test import APIClient
import json
import time

class RateLimiterTestCase(TestCase):

    def setUp(self):
        c1 = CustomUser.objects.create(username="nisarg123", password="nisarg123")
        c2 = CustomUser.objects.create(username="nisarg124", password="nisarg124")
        c3 = CustomUser.objects.create(username="nisarg125", password="nisarg125")
        c4 = CustomUser.objects.create(username="nisarg126", password="nisarg126")

    def login(self, username, password):
        client = APIClient()
        response = client.post('/token-auth/', {"username": username, "password": password}, format='json')
        content = json.loads(response.content)
        token = content["token"]
        return token

    def call_test_api(self, token):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="JWT " + token)
        response = client.get('/test/', {}, format='json')
        return response

    def test_successful_call(self):
        
        username1 = "nisarg123"
        password1 = "nisarg123"

        username2 = "nisarg124"
        password2 = "nisarg124"

        token1 = self.login(username1, password1)
        token2 = self.login(username2, password2)

        for i in range(8):
            response = self.call_test_api(token1)
            self.assertEqual(response.status_code, 200)

        for i in range(8):
            response = self.call_test_api(token2)
            self.assertEqual(response.status_code, 200)


    def test_failure_call1(self):
        
        username1 = "nisarg125"
        password1 = "nisarg125"

        token1 = self.login(username1, password1)

        failure_flag = False
        for i in range(12):
            response = self.call_test_api(token1)
            if response.status_code==403:
                failure_flag = True
        
        self.assertEqual(failure_flag, True)


    def test_failure_call2(self):
        
        username1 = "nisarg126"
        password1 = "nisarg126"

        token1 = self.login(username1, password1)

        failure_flag1 = False
        for i in range(9):
            response = self.call_test_api(token1)
            if response.status_code==403:
                failure_flag1 = True
        
        time.sleep(2)

        failure_flag2 = False
        for i in range(9):
            response = self.call_test_api(token1)
            if response.status_code==403:
                failure_flag2 = True

        time.sleep(2)

        failure_flag3 = False
        for i in range(9):
            response = self.call_test_api(token1)
            if response.status_code==403:
                failure_flag3 = True

        self.assertEqual(failure_flag1, False)
        self.assertEqual(failure_flag2, False)
        self.assertEqual(failure_flag3, True)
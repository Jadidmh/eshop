from rest_framework.test import APITestCase
from django.urls import reverse
from .models import User
from model_mommy import mommy
from django.contrib.auth.hashers import check_password

# Create your tests here.

class TestClientRegister(APITestCase):

    def setUp(self):
        pass

    def test_client_register(self):
        url = reverse('clientRegister')
        data = {
            "phone": "09338804396",
            "email": "iraj@gmail.com",
            "username": "Iraj",
            "password1": "m13801121",
            "password2": "m13801121"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)

    def test_client_register_password_hash(self):
        url = reverse('clientRegister')
        data = {
            "phone": "09338804396",
            "email": "iraj@gmail.com",
            "username": "Iraj",
            "password1": "m13801121",
            "password2": "m13801121"
        }
        self.client.post(url, data=data)
        client = User.objects.get(phone="09338804396")
        self.assertTrue(check_password("m13801121", client.password))

    def test_client_register_wrong_password(self):
        url = reverse('clientRegister')
        data = {
            "phone": "09338804396",
            "email": "iraj@gmail.com",
            "username": "Iraj",
            "password1": "m13801121",
            "password2": "13801121"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_client_register_is_client(self):
        url = reverse('clientRegister')
        data = {
            "phone": "09338804396",
            "email": "iraj@gmail.com",
            "username": "Iraj",
            "password1": "m13801121",
            "password2": "m13801121"
        }
        self.client.post(url, data=data)
        client = User.objects.get(phone="09338804396")
        self.assertTrue(client.is_client)


class TestClientLogin(APITestCase):

    def setUp(self):
        self.user = mommy.make(User, phone='09305006849', password='m13801121')

    def test_client_login_error(self):
        url = reverse('clientLogin')
        data = {
            "phone": "09305006849",
            "password": "m13801122"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 401)


class TestClientProfile(APITestCase):

    def setUp(self):
        self.user = mommy.make(User, phone='09305006849')

    def test_client_profile_show(self):
        url = reverse('clientProfile')
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_client_profile_unauthorized(self):
        url = reverse('clientProfile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_client_profile_edit_error(self):
        url = reverse('clientProfile')
        self.client.force_authenticate(self.user)
        data = {
            "phone": "09305006848",
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_client_profile_edit(self):
        url = reverse('clientProfile')
        self.client.force_authenticate(self.user)
        data = {
            "phone": "09338804396",
            "email": "iraj@gmail.com",
            "username": "Iraj",
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, 200)
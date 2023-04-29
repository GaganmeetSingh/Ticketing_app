from django.test import TestCase, Client
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.test import APIRequestFactory
from .models import *
from .serializers import *
from rest_framework_simplejwt.tokens import AccessToken
from django.urls import reverse


class CityTestCase(APITestCase):
    def setup(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = AccessToken.for_user(self.user)
        self.city = City.objects.create(city_name="abc", state='Punjab', latitide=1.234, longitude=2.345)
    

    def test_get_city(self):
        response = self.client.get('city/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_city(self):
        data = {'city_name': 'test2', 'state': 'Punjab', 'latitude': 2.345, 'longitude':3.456}
        response = self.client.post('city/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
class BusServiceTestCase(APITestCase):
    def setup(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()   
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = AccessToken.for_user(self.user)
        data = {'source':1, 'destination':2, 'total_seats':50, 'depature_time': '18:30', 'travel_time':'06:00'} 
        self.bus_service = self.client.post('bus-service/', data, format='json')
        
    def test_get_bus_service(self):
        response = self.client.get('bus-service/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_bus_service(self):
        data = {'source':2, 'destination':3, 'total_seats':50, 'depature_time': '18:30', 'travel_time':'06:00'} 
        response = self.client.post('bus-service/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
class BookingTestCase(APITestCase):
    def setup(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()   
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = AccessToken.for_user(self.user)
        data = {'passenger_name':'ABC', 'bus_service':2, 'travel_date': '2023-05-02'} 
        self.bus_service = self.client.post('booking/', data, format='json')
        
    def test_get_bus_service(self):
        response = self.client.get('booking/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_bus_service(self):
        data = {'passenger_name':'ABCD', 'bus_service':1, 'travel_date': '2023-05-02'} 
        response = self.client.post('booking/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
 
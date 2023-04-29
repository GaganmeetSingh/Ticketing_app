from django.shortcuts import render
from ticketing_app.models import *
from ticketing_app.serializers import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models.functions import TruncMonth
from django.db.models import Count, Sum
from rest_framework.response import Response


# Create your views here.
"""This API is used to create a User.
Django's User model is used here.
Returns: 
    User object in json format.
"""
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny, )
    
"""This API is used to create a new city for POST request 
which will act as source or destination of BusService and
also lists all the cities added so far for GET request.
Returns:
    City object in json format for create.
    List of Cities for list.
"""
class CityListCreateView(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (IsAuthenticated, )
    
"""This API is used to create a Bus Service with specific 
source and destination for POST request and also returns list
of all bus services for GET request.
Returns: 
    Bus Service object for create.
    List of all Bus Services for list.
"""
class BusServiceListCreateView(generics.ListCreateAPIView):
    queryset = BusService.objects.all()
    permission_classes = (IsAuthenticated, )
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BusServiceCreateSerializer 
        else:
            return BusServiceListSerializer 

"""This API is used to create a Booking with specific 
bus service and passenger details for POST request and
also returns list of all bookings for GET request.
Returns: 
    Booking object for create.
    List of all Bookings for list.
"""
class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    permission_classes = (IsAuthenticated, )
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookingCreateSerializer 
        else:
            return BookingListSerializer

"""This API is used to cancel a Booking with specific 
id passed in the url.
Returns: 
    id of the Booking that has been cancelled.
"""        
class BookingCancelView(generics.RetrieveUpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingRetrieveSerializer
    permission_classes = (IsAuthenticated, )
    
"""This API has no access restriction and can be used by
anyone to get the booking detials with booking id as a parameter.
Returns:
    Booking object.
"""
class BookingRetrieveView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingListSerializer
    permission_classes = (AllowAny, )

"""This API returns count of all Bookings grouped monthly
and source location based.
Returns:
    List of dict objects with parameter as count, month and location id.
"""
class BookingCountSummaryView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        count = Booking.objects.filter(is_cancelled=False).annotate(
            month=TruncMonth('travel_date')
        ).values('month', 'bus_service__source__city_name').annotate(count=Count('id')).order_by('bus_service__source', 'month')
        
        results = []
        for c in count:
            results.append(
                {
                'month':c['month'],
                'source_loc': c['bus_service__source__city_name'],
                'count': c['count']
                }
            )
            
        return Response(results)

"""This API returns Booking amount of all Bookings grouped monthly
and source location based.
Returns:
    List of dict objects with parameter as amount, month and location id.
"""
class BookingAmountSummaryView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        amount = Booking.objects.filter(is_cancelled=False).annotate(
            month=TruncMonth('travel_date')
        ).values('month', 'bus_service__source__city_name').annotate(total_amount=Sum('booking_amount')).order_by('bus_service__source', 'month')
        
        results = []
        for a in amount:
            results.append(
                {
                'month':a['month'],
                'source_loc': a['bus_service__source__city_name'],
                'amount': a['total_amount']
                }
            )
            
        return Response(results)
    

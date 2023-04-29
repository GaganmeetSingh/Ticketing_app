from django.urls import path
from ticketing_app import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # to register a user
    path('register/', views.UserRegisterView.as_view(), name='signup_user'),
    # to create access token 
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # to refresh access token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # to create city and meta api for city
    path('city/', views.CityListCreateView.as_view(), name='create_list_city'),
    # to create bus service and meta api for bus service
    path('bus-service/', views.BusServiceListCreateView.as_view(), name='create_list_bus_service'),
    # to create booking and meta api for booking
    path('booking/', views.BookingListCreateView.as_view(), name='create_list_booking'),
    # to cancel a booking
    path('booking-cancel/<int:pk>/', views.BookingCancelView.as_view(), name='cancel_booking'),
    # to get a booking object by id
    path('booking/<int:pk>/', views.BookingRetrieveView.as_view(), name='retrieve_booking'),
    # to get booking count data based on location and date range
    path('booking-count-summary/', views.BookingCountSummaryView.as_view(), name='count_summary_booking'),
    # to get amount of booking data grouped based on locationa and date range
    path('booking-amount-summary/', views.BookingAmountSummaryView.as_view(), name='amount_summary_booking'),
    
]
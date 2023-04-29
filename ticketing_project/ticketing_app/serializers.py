from ticketing_app.models import *
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
import datetime
import qrcode
from django.core.files.base import ContentFile
from io import BytesIO
# from django.contrib.gis.geos import Point

class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    
    password2 = serializers.CharField(required=True, write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True, 'required':True, 'validators':[validate_password]},
            'username': {'required':True}
        }
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"Error": "Password does not match"})
        return attrs
    
    def create(self, validated_data):
        manager = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email']
        )

        manager.set_password(validated_data['password'])
        manager.save()
        
        return manager


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city_name', 'state', 'latitude', 'longitude']
        
        extra_kwargs = {
            'city_name': {'required': True},
            'state': {'required': True},
            'latitude': {'required': True},
            'longitude': {'required': True}
        }
        

class BusServiceCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BusService
        fields = ['id', 'source', 'destination', 'total_seats', 'departure_time', 'travel_time']
        extra_kwargs = {
            'source': {'required': True},
            'destination': {'required': True},
            'total_seats': {'required': True},
            'departure_time': {'required': True},
            'travel_time': {'required': True}
        }
    
    def calculate_price(self, source, dest):
        dist = ((source.latitude - dest.latitude)**2 + (source.longitude - dest.longitude)**2)**0.5
        return int(20 + dist * 0.5)
        
    def create(self, validated_data):
        bus_service = BusService.objects.create(
            source = validated_data['source'],
            destination = validated_data['destination'],
            total_seats = validated_data['total_seats'],
            departure_time = validated_data['departure_time'],
            travel_time = validated_data['travel_time'],
            price = self.calculate_price(validated_data['source'], validated_data['destination']),
            is_active = True
        )
        
        bus_service.save()
        return bus_service
    
class BusServiceListSerializer(serializers.ModelSerializer):
    source = CitySerializer()
    destination = CitySerializer()
    
    class Meta:
        model = BusService
        fields = '__all__'
    
    
class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'passenger_name', 'bus_service', 'travel_date']
        extra_kwargs = {
            'passenger_name': {'required': True},
            'bus_service': {'required': True},
            'travel_date': {'required': True}
        }
    
    def validate(self, attrs):
        if not ((attrs['travel_date'] == datetime.datetime.now().date() and datetime.datetime.now().time() < attrs['bus_service'].departure_time()) or attrs['travel_date'] > datetime.datetime.now().date()):
            raise serializers.ValidationError('Ticket booking ended')
        return attrs
            
    def get_avl_seat(self, bus_service, travel_date):
        seat_num = None
        booked_seats = Booking.objects.filter(travel_date=travel_date, bus_service=bus_service, is_cancelled = False).values_list('seat_number', flat=True)
        
        for i in range(1,bus_service.total_seats +1):
            if i not in booked_seats:
                seat_num = i
                break
        return seat_num
    
    def gen_qrcode(self, booking):
        qr_image = qrcode.make(f"ID: {booking.id}\nName: {booking.passenger_name}\nPNR: {booking.pnr}\TravelDate: {booking.travel_date}\nDestination: {booking.bus_service.destination}\nAmount Paid: {booking.booking_amount}")
        byte_stream = BytesIO()
        qr_image.save(byte_stream, format='PNG')
        qr_image_bytes = byte_stream.getvalue()
        return qr_image_bytes
        
    def create(self, validated_data):  
        validated_data['manager'] = self.context['request'].user
        validated_data['booking_amount'] = validated_data['bus_service'].price
        validated_data['seat_number'] = self.get_avl_seat(validated_data['bus_service'], validated_data['travel_date'])
        
        if validated_data['seat_number'] == None:
            return {'message': 'Seat not available'}
        
        booking = super().create(validated_data)
        booking.qr_code = self.gen_qrcode(booking)
        booking.save()
        return booking
        
    
class BookingListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Booking
        fields = '__all__'
        
        
class BookingRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id']
        
    def update(self, instance, validated_data):
        if instance.is_cancelled == True:
            raise serializers.ValidationError('Booking already cancelled')
        
        instance.is_cancelled = True
        instance.cancelled_at = datetime.datetime.now()
        instance.save()
        return instance
    
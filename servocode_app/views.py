from .models import Location
from .serializers import LocationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

class LocationList(APIView):
    def get(self,request,format=None):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True, context={"request":request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LocationView(APIView):
    def get_object(self,pk):
        try:
            return Location.objects.get(pk=pk)
        except Location.DoesNotExist:
            raise Http404

    def get(self,request,id,format=None):
        location = self.get_object(id)
        serializer = LocationSerializer(location,context={"request":request})
        return Response(serializer.data)

    def delete(self,request,id,format=None):
        location = self.get_object(id)
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self,request,id,format=None):
        location = self.get_object(id)
        serializer = LocationSerializer(location,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self,request,id,format=None):
        pass

class ClosestLocation(APIView):
    def get_closest_location(self,latitude,longitude):
        geolocator = Nominatim()
        location = (latitude,longitude)

        locations = Location.objects.all()
        closest_object = locations[0] #object from db
        closest = (closest_object.latitude, closest_object.longitude)
        closest_id = closest_object.id
        closest_distance = geodesic(location,closest)

        for loc in locations:
            if closest_distance > geodesic(location, (loc.latitude,loc.longitude)):
                closest_distance = geodesic(location,(loc.latitude,loc.longitude))
                closest_id = loc.id

        return Location.objects.get(id=closest_id)

    def get(self, request, latitude, longitude, format=None):
        try:
            latitude = float(latitude)
            longitude = float(longitude)

            if (-90) < latitude < 90 and (-180) < longitude < 180:
                #ok
                location = self.get_closest_location(latitude=latitude, longitude=longitude)

                serializer = LocationSerializer(location, context={"request": request})
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

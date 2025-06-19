from django.shortcuts import render

# Create your views here.


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Run
from .serializers import RunSerializer


@api_view(['GET'])
def my_function_based_view(request):
    return Response({
        'company_name': 'Бегуны 30+',
        'slogan': 'Не бегаем в любую погоду! От -30 до +30!',
        'contacts': 'Город Москва, Олимпийская деревня'
    })


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer

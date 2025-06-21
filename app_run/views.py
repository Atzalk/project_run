from django.shortcuts import render

# Create your views here.


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Run
from .serializers import RunSerializer, UserSerializer, RunUserSerializer
from django.contrib.auth.models import User


@api_view(['GET'])
def my_function_based_view(request):
    return Response({
        'company_name': 'Бегуны 30+',
        'slogan': 'Не бегаем в любую погоду! От -30 до +30!',
        'contacts': 'Город Москва, Олимпийская деревня'
    })


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.select_related('athlete').all()
    serializer_class = RunUserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        qs = self.queryset
        type = self.request.query_params.get('type', None)
        if type == 'coach':
            qs = qs.filter(is_staff=True, is_superuser=False)
        if type == 'athlete':
            qs = qs.filter(is_staff=False, is_superuser=False)
        return qs.filter(is_superuser=False)


class RunUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Run.objects.select_related('athlete').all()
    serializer_class = RunUserSerializer

from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .models import Run
from .serializers import RunSerializer, UserSerializer, RunUserSerializer
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend


class RunsPagination(PageNumberPagination):
    page_size_query_param = 'size'


class UsersPagination(PageNumberPagination):
    page_size_query_param = 'size'


@api_view(['GET'])
def my_function_based_view(request):
    return Response({
        'company_name': 'Бегуны 30+',
        'slogan': 'Не бегаем в любую погоду! От -30 до +30!',
        'contacts': 'Город Москва, Олимпийская деревня'
    })


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.select_related('athlete').all()
    serializer_class = RunSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'athlete']
    ordering_fields = ['created_at']


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    pagination_class = UsersPagination
    filterset_fields = ['first_name', 'last_name']
    ordering_fields = ['date_joined']

    def get_queryset(self):
        qs = self.queryset
        type = self.request.query_params.get('type', None)
        if type == 'coach':
            qs = qs.filter(is_staff=True, is_superuser=False)
        if type == 'athlete':
            qs = qs.filter(is_staff=False, is_superuser=False)
        return qs.filter(is_superuser=False)


class RunUserViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.select_related('athlete').all()
    serializer_class = RunUserSerializer
    pagination_class = RunsPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'athlete']
    ordering_fields = ['created_at']


class RunStartViewSet(APIView):
    def post(self, request, id=None):
        data_run = get_object_or_404(Run, id=id)
        if data_run.status == 'in_progress' or data_run.status == 'finished':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data_run.status = 'in_progress'
        data_run.save()
        serializer = RunSerializer(data_run)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RunStopViewSet(APIView):
    def post(self, request, id=None):
        data_run = get_object_or_404(Run, id=id)
        if data_run.status == 'init' or data_run.status == 'finished':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data_run.status = 'finished'
        data_run.save()
        serializer = RunSerializer(data_run)

        return Response(serializer.data, status=status.HTTP_200_OK)

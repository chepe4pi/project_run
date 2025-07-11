from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from rest_framework import status
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from app_run.models import Run
from app_run.serializers import RunSerializer, UserSerializer

@api_view(['GET'])
def company_details(request):
    details = {
        'company_name': settings.COMPANY_NAME,
        'slogan': settings.SLOGAN,
        'contacts': settings.CONTACTS
    }
    return Response(details)


class RunViewSet(ModelViewSet):
    queryset = Run.objects.select_related('athlete').all()
    serializer_class = RunSerializer
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name']


class UserViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for retrieving user information.
    
    This viewset provides 'list' and 'retrieve' actions for User objects,
    excluding superusers. It supports filtering by user type ('coach' or 'athlete')
    via query parameters.
    """
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_superuser=False)
    lookup_field = 'is_staff'
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name']
    
    def get_queryset(self) -> 'QuerySet[User]':
        """
        Filter the queryset based on the 'type' query parameter.
        
        Returns:
            QuerySet[User]: Filtered queryset of User objects.
                - If type='coach': returns staff users
                - If type='athlete': returns non-staff users
                - Otherwise: returns all non-superuser users
        """
        user_type = self.request.query_params.get('type')
        
        # Use a dictionary mapping for cleaner, more maintainable code
        type_filters = {
            'coach': {'is_staff': True},
            'athlete': {'is_staff': False}
        }
        
        if user_type in type_filters:
            return self.queryset.filter(**type_filters[user_type])
        
        return self.queryset


class RunStartAPIView(APIView):
    def put(self, request, pk, format=None):
        run = get_object_or_404(Run, pk=pk)
        if run.status not in [Run.RunStatus.IN_PROGRESS, Run.RunStatus.FINISHED]:
            serializer = RunSerializer(run, data={'status': Run.RunStatus.IN_PROGRESS}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Run already started'}, status=status.HTTP_400_BAD_REQUEST)


class RunStopAPIView(APIView):
    def put(self, request, pk, format=None):
        run = get_object_or_404(Run, pk=pk)
        if run.status == Run.RunStatus.IN_PROGRESS:
            serializer = RunSerializer(run, data={'status': Run.RunStatus.FINISHED}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Run not started'}, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from .models import Events, Member, AttendanceRecord
from .serializers import EventsSerializer
import logging

logger = logging.getLogger(__name__)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
def event_crud(request, pk=None):
    user = request.user
    logger.warning(f"User: {user}, Username: {getattr(user, 'username', None)}, Role: {getattr(user, 'role', None)}, is_officer: {getattr(user, 'is_officer', None)}, is_admin: {getattr(user, 'is_admin', None)}")
    if request.method == 'GET':
        # Allow both admin and officer to view events
        if not (hasattr(user, 'is_admin') and user.is_admin()) and not (hasattr(user, 'is_officer') and user.is_officer()):
            return Response({'detail': 'Forbidden'}, status=403)
        events = Events.objects.all()
        serializer = EventsSerializer(events, many=True)
        return Response(serializer.data)
    else:
        # Only allow admin for POST, PUT, DELETE
        if not (hasattr(user, 'is_admin') and user.is_admin()):
            return Response({'detail': 'Forbidden'}, status=403)
        if request.method == 'POST':
            serializer = EventsSerializer(data=request.data)
            if serializer.is_valid():
                event = serializer.save()
                # Register all members for this event
                for member in Member.objects.all():
                    AttendanceRecord.create_attendance_records(event, member)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'PUT':
            try:
                event = Events.objects.get(pk=pk)
            except Events.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = EventsSerializer(event, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            try:
                event = Events.objects.get(pk=pk)
            except Events.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            event.delete()
            return Response(status=status.HTTP_204_NO_CONTENT) 
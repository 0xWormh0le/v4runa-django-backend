from rest_framework import generics
from .serializers import IotSensorDataRecordSerializer
from rest_framework.response import Response
from rest_framework import status

class SensorDataView(generics.CreateAPIView):
    """
    Add sensor data from Particle Web Hook.
    """

    serializer_class = IotSensorDataRecordSerializer

    def create(self, request):
        serializer = IotSensorDataRecordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except Exception as e:
            return Response(
                { 'result': 'failed', 'message': str(e) },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response({ 'result': 'ok' }, status=status.HTTP_200_OK)


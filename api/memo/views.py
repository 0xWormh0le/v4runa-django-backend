from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.models import Memo

class MemoView(APIView):
    def post(self, request):
        domain = request.user.email.split('@')[1]
        memo = Memo.objects.filter(email_domain=domain).first()

        if memo is None:
            memo = Memo(memo=request.data.get('value'), email_domain=domain)
        else:
            memo.memo = request.data.get('value')

        try:
            memo.save()
        except Exception as e:
            return Response(
                { 'result': 'failed', 'message': str(e) },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({ 'result': 'ok' }, status=status.HTTP_200_OK)

    def get(self, request):
        domain = request.user.email.split('@')[1]
        memo = Memo.objects.filter(email_domain=domain).first()
        return Response(
            { 'value': None if memo is None else memo.memo },
            status=status.HTTP_200_OK
        )

        



from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import UserProductLikeManager
from .serializers import UserLikeDislikeSerializer


class UserLikeProductAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = UserLikeDislikeSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        is_liked_already = UserProductLikeManager.objects.filter(
            user=user, content_type=data.validated_data['content_type'], object_id=data.validated_data['object_id']
        ).first().exists()

        if is_liked_already:
            UserProductLikeManager.objects.filter(
                user=user, content_type=data.validated_data['content_type'], object_id=data.validated_data['object_id']
            ).first().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            UserProductLikeManager.objects.create(
                user=user, content_type=data.validated_data['content_type'], object_id=data.validated_data['object_id']
            )
            return Response(status=status.HTTP_201_CREATED)


__all__ = ['UserLikeProductAPIView']

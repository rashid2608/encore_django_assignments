from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
import logging
logger = logging.getLogger(__name__)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })





class VerifyToken(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        token_key = request.data.get('token')
        logger.info(f"Received token verification request for token: {token_key[:5]}...")

        if not token_key:
            logger.warning("No token provided in request")
            return Response({"error": "No token provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = Token.objects.select_related('user').get(key=token_key)
            user = token.user
            logger.info(f"Token verified for user: {user.username}")
            return Response({
                'valid': True,
                'user_id': user.pk,
                'username': user.username,
                'email': user.email
            })
        except Token.DoesNotExist:
            logger.warning(f"Invalid token: {token_key[:5]}...")
            return Response({
                'valid': False,
                'error': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error during token verification: {str(e)}")
            return Response({
                'valid': False,
                'error': 'An error occurred during verification'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


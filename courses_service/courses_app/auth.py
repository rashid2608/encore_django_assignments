# courses_service/courses_app/auth.py

import requests
import logging
from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

class CustomTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        logger.info("Attempting to authenticate request")
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            logger.warning("No Authorization header found")
            return None

        try:
            token = auth_header.split()[1]
            logger.info(f"Token extracted: {token[:5]}...")  # Log first 5 chars for security
        except IndexError:
            logger.error("Invalid token header format")
            raise exceptions.AuthenticationFailed('Invalid token header')

        # Make a request to your auth service to validate the token
        try:
            response = requests.post('http://localhost:8000//verify-token/', data={'token': token})
            logger.info(f"Auth service response status: {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Error contacting auth service: {str(e)}")
            raise exceptions.AuthenticationFailed('Error verifying token')
        
        if response.status_code == 200:
            user_data = response.json()
            logger.info(f"Token verified for user: {user_data.get('username')}")
            try:
                user = User.objects.get(username=user_data['username'])
                logger.info(f"User found in database: {user.username}")
            except User.DoesNotExist:
                logger.warning(f"User {user_data['username']} not found, creating new user")
                user = User.objects.create_user(username=user_data['username'])
            
            return (user, token)
        
        logger.error("Invalid token")
        raise exceptions.AuthenticationFailed('Invalid token')
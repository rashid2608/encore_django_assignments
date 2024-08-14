# courses_app/tests/test_auth.py

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.exceptions import AuthenticationFailed
from unittest.mock import patch, MagicMock
from courses_app.auth import CustomTokenAuthentication

@pytest.fixture
def auth_class():
    return CustomTokenAuthentication()

@pytest.fixture
def mock_request():
    factory = APIRequestFactory()
    request = factory.get('/')
    request.META['HTTP_AUTHORIZATION'] = 'Token valid_token_123'
    return request

@pytest.mark.django_db
@patch('courses_app.auth.requests.post')
def test_custom_token_authentication_success(mock_post, auth_class, mock_request):
    # Mock the response from the auth service
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'username': 'testuser', 'valid': True}
    mock_post.return_value = mock_response

    # Perform authentication
    user, token = auth_class.authenticate(mock_request)

    # Assertions
    assert isinstance(user, User)
    assert user.username == 'testuser'
    assert token == 'valid_token_123'
    mock_post.assert_called_once_with(
        'http://localhost:8000/verify-token/',
        data={'token': 'valid_token_123'}
    )

@pytest.mark.django_db
@patch('courses_app.auth.requests.post')
def test_custom_token_authentication_invalid_token(mock_post, auth_class, mock_request):
    # Mock the response from the auth service for an invalid token
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_post.return_value = mock_response

    # Attempt authentication with invalid token
    with pytest.raises(AuthenticationFailed):
        auth_class.authenticate(mock_request)

@pytest.mark.django_db
def test_custom_token_authentication_no_auth_header(auth_class):
    # Create a request without an authorization header
    factory = APIRequestFactory()
    request = factory.get('/')

    # Attempt authentication without auth header
    result = auth_class.authenticate(request)
    assert result is None

@pytest.mark.django_db
@patch('courses_app.auth.requests.post')
def test_custom_token_authentication_create_new_user(mock_post, auth_class, mock_request):
    # Mock the response from the auth service
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'username': 'newuser', 'valid': True}
    mock_post.return_value = mock_response

    # Ensure the user doesn't exist before the test
    User.objects.filter(username='newuser').delete()

    # Perform authentication
    user, token = auth_class.authenticate(mock_request)

    # Assertions
    assert isinstance(user, User)
    assert user.username == 'newuser'
    assert User.objects.filter(username='newuser').exists()
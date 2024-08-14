from django.test import TestCase
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpass123')

@pytest.mark.django_db
def test_token_auth(api_client, user):
    response = api_client.post('/api-token-auth/', {'username': 'testuser', 'password': 'testpass123'})
    assert response.status_code == 200
    assert 'token' in response.data

@pytest.mark.django_db
def test_verify_token(api_client, user):
    token = Token.objects.create(user=user)
    response = api_client.post('/verify-token/', {'token': token.key})
    assert response.status_code == 200
    assert response.data['valid'] == True
    assert response.data['username'] == 'testuser'

@pytest.mark.django_db
def test_verify_invalid_token(api_client):
    response = api_client.post('/verify-token/', {'token': 'invalid_token'})
    assert response.status_code == 400
    assert response.data['valid'] == False

@pytest.mark.django_db
def test_verify_token_missing_token(api_client):
    response = api_client.post('/verify-token/', {})
    assert response.status_code == 400
    assert 'token' in response.data['error']

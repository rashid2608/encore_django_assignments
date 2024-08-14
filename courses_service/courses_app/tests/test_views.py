# courses_service/courses_app/tests/test_views.py

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from courses_app.auth import CustomTokenAuthentication

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_user():
    user = User.objects.create_user(username='testuser', password='testpass')
    token = Token.objects.create(user=user)
    return user, token

@pytest.fixture
def authenticated_client(api_client, authenticated_user):
    user, token = authenticated_user
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return api_client

@pytest.fixture
def mock_auth(monkeypatch, authenticated_user):
    user, token = authenticated_user
    def mock_authenticate(*args, **kwargs):
        return (user, token)
    monkeypatch.setattr(CustomTokenAuthentication, 'authenticate', mock_authenticate)


@pytest.fixture
def mock_courses_api(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse({
            'results': [
                {'name': 'Course 1', 'org': 'Org 1'},
                {'name': 'Course 2', 'org': 'Org 2'}
            ]
        }, 200)

    monkeypatch.setattr('requests.get', mock_get)

@pytest.mark.django_db
def test_courses_list(authenticated_client, mock_auth, mock_courses_api):
    response = authenticated_client.get('/courses/')
    assert response.status_code == 200
    assert len(response.data['results']) == 2

@pytest.mark.django_db
def test_courses_list_unauthenticated(api_client):
    response = api_client.get('/courses/')
    assert response.status_code == 403

@pytest.mark.django_db
def test_courses_list_with_fields(authenticated_client, mock_auth, monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse({
            'results': [
                {'name': 'Course 1', 'org': 'Org 1', 'description': 'Desc 1'},
                {'name': 'Course 2', 'org': 'Org 2', 'description': 'Desc 2'}
            ]
        }, 200)

    monkeypatch.setattr('requests.get', mock_get)

    response = authenticated_client.get('/courses/?fields=name,org')
    assert response.status_code == 200
    assert 'name' in response.data['results'][0]
    assert 'org' in response.data['results'][0]
    assert 'description' not in response.data['results'][0]

@pytest.mark.django_db
def test_courses_list_pagination(authenticated_client, mock_auth, monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse({
            'results': [{'name': f'Course {i}', 'org': f'Org {i}'} for i in range(1, 6)],
            'next': 'http://testserver/courses/?page=2',
            'previous': None
        }, 200)

    monkeypatch.setattr('requests.get', mock_get)

    response = authenticated_client.get('/courses/?page=1&page_size=5')
    assert response.status_code == 200
    assert len(response.data['results']) == 5
    assert response.data['next'] is not None
    assert response.data['previous'] is None
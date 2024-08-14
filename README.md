# Encore Django Assignments

This project demonstrates a simple microservices architecture using Django and Django Rest Framework. It consists of two separate services:

1. Authentication Service
2. Courses Service

## Prerequisites

Before you begin, ensure you have the following installed on your system:
- Python 3.8 or higher
- pip (Python package manager)
- Git
- Docker
- Docker Compose

You can check if these are installed by running the following commands:
```
python --version
pip --version
git --version
docker --version
docker-compose --version
```

## Project Structure

```
encore_django_assignments/
│
├── auth_service/
│   ├── auth_project/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   ├── auth_app/
│   │   ├── views.py
│   │   ├── tests/
│   │   │   └── test_views.py
│   │   └── ...
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── pytest.ini
│
├── courses_service/
│   ├── courses_project/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   ├── courses_app/
│   │   ├── views.py
│   │   ├── auth.py
│   │   ├── tests/
│   │   │   ├── test_views.py
│   │   │   └── test_auth.py
│   │   └── ...
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── pytest.ini
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Setup

### Using Docker Compose (Recommended)

1. Clone the repository:
   ```
   git clone https://github.com/rashid2608/encore_django_assignments.git
   cd encore_django_assignments
   ```

2. Build and run the services:
   ```
   docker-compose up --build -d
   ```

3. Create a superuser for the Auth Service:
   ```
   docker-compose exec auth-service python manage.py createsuperuser
   ```

The services will be available at:
- Auth Service: http://localhost:8000
- Courses Service: http://localhost:8001

### Manual Setup (Alternative)

1. Clone the repository:
   ```
   git clone https://github.com/rashid2608/encore_django_assignments.git
   cd encore_django_assignments
   ```

2. Set up the Auth Service:
   ```
   cd auth_service
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver 8000
   ```

3. Set up the Courses Service:
   ```
   cd ../courses_service
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver 8001
   ```

## Usage

1. Obtain a token from the Auth Service:
   ```
   curl -X POST http://localhost:8000/api-token-auth/ -H "Content-Type: application/json" -d '{"username": "your_username", "password": "your_password"}'
   ```

2. Use the token to access the Courses Service:
   ```
   curl -H "Authorization: Token Your_token_here" "http://localhost:8001/courses/?page=1&page_size=5&fields=name,org"
   ```

## Running Tests and Coverage

To run the tests and generate coverage reports:

1. For the Auth Service:
   ```
   cd auth_service
   coverage run -m pytest
   coverage report
   coverage html
   ```

2. For the Courses Service:
   ```
   cd courses_service
   coverage run -m pytest
   coverage report
   coverage html
   ```

The HTML coverage reports will be generated in the `htmlcov` directory of each service. Open `htmlcov/index.html` in a web browser to view the detailed coverage report.

You can combine these commands:
```
coverage run -m pytest && coverage report && coverage html
```

To check the report in a browser, run:
- macOS: `open htmlcov/index.html`
- Linux: `xdg-open htmlcov/index.html`
- Windows: `start htmlcov/index.html`

## Test Structure

- Auth Service tests are located in `auth_service/auth_app/tests/`
- Courses Service tests are located in `courses_service/courses_app/tests/`

The tests cover various aspects of the services, including:
- API endpoints functionality
- Authentication and authorization
- Inter-service communication
- Edge cases and error handling

## Learning Points

- Microservices Architecture
- Token-based Authentication
- Custom Authentication in Django Rest Framework
- Inter-service Communication
- API Design and Implementation
- Docker and Docker Compose for containerization
- Unit Testing in Django
- Test Coverage Analysis

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. When contributing, please:
- Write tests for new features or bug fixes
- Ensure all tests pass and maintain or improve coverage
- Follow the existing code style and project structure
- Use Conventional Commits for commit messages (https://www.conventionalcommits.org/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
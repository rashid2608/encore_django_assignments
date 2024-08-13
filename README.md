# Encore Django Assignments

This project demonstrates a simple microservices architecture using Django and Django Rest Framework. It consists of two separate services:

1. Authentication Service
2. Courses Service

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
│   │   └── ...
│   ├── manage.py
│   └── requirements.txt
│
├── courses_service/
│   ├── courses_project/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   ├── courses_app/
│   │   ├── views.py
│   │   ├── auth.py
│   │   └── ...
│   ├── manage.py
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

## Setup

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
   curl -H "Authorization: Token your_token_here" http://localhost:8001/courses/?page=1&page_size=5&fields=name,org
   ```

## Learning Points

- Microservices Architecture
- Token-based Authentication
- Custom Authentication in Django Rest Framework
- Inter-service Communication
- API Design and Implementation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
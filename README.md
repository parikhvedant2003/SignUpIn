# SignUpIn

**SignUpIn** is a Django-based project that implements user authentication functionalities, including user registration, login, logout, and JWT-based authentication. This project is designed to be simple yet secure, allowing users to sign up, authenticate, and maintain session security.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Error Handling](#error-handling)
- [License](#license)

---

## Features

- **User Registration**: Allows new users to register with unique usernames and emails.
- **User Login**: Secure login with JWT-based token authentication.
- **Protected Endpoints**: Secures specific routes, allowing access only to authenticated users.
- **Token-Based Authentication**: JWT tokens are used to validate user sessions and manage expiration.

## Prerequisites

- Python 3.7 or higher
- Django 3.2 or higher
- Django REST framework
- `djangorestframework-simplejwt` for JWT handling

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/parikhvedant2003/SignUpIn.git
   cd SignUpIn
   ```

2. **Create and Activate a Virtual Environment**:
   - **Step 2.1**: Set up the virtual environment in the project folder.
     ```bash
     python -m venv venv
     ```
   - **Step 2.2**: Activate the virtual environment.
     ```bash
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
     ```

3. **Install Project Dependencies**:
   - **Step 3.1**: Install basic dependencies for setting up the project.
     ```bash
     pip install -r requirements.txt
     ```
   - **Step 3.2**: Install the dependencies of the project using the poetry.
     ```bash
     poetry install
     ```

4. **Set Up and Configure the Database**:
   - **Step 4.1**: Configure any necessary settings in `settings.py`, such as the database path or JWT settings.
   - **Step 4.2**: Run migrations to set up the database structure.
     ```bash
     python manage.py migrate
     ```

5. **Create a Superuser (Optional)**:
   To access the Django admin panel, create a superuser account.
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Server**:
   ```bash
   python manage.py runserver
   ```

## Usage

- **Sign Up**: Register a new user using the signup API.
- **Sign In**: Obtain an access token via the signin API.
- **Access Protected Endpoints**: Access authorized resources using the token.

Use tools like **Postman** to interact with API endpoints and test the authentication flow.

## Project Structure

```
SignUpIn/
├── SignUpIn/
│   ├── settings.py         # Project settings, including JWT config
│   ├── urls.py             # Project URLs
│   └── wsgi.py             # WSGI config for deployment
├── SignUpSignIn/
│   ├── models.py           # CustomUser model definition
│   ├── views.py            # Business logic for signup, signin, logout
│   ├── serializers.py      # Serializers for handling JSON data
│   └── urls.py             # API endpoint URLs
├── requirements.txt
├── poetry.lock
├── pyproject.toml
├── manage.py
```

## Configuration

1. **JWT Secret Key**: Ensure your `settings.py` contains a `JWT_SECRET_KEY`.
2. **Token Lifetime**:
   Update `SIMPLE_JWT` in `settings.py` to configure token expiration.
   
   ```python
   SIMPLE_JWT = {
       'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
       'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
   }
   ```

## API Endpoints

| Method | Endpoint            | Description                         |
|--------|---------------------|-------------------------------------|
| GET    | `/accounts/`        | Protected resource (requires token) |
| POST   | `/accounts/signup/` | Registers a new user                |
| POST   | `/accounts/signin/` | Signs in and returns JWT token      |
| POST   | `/accounts/logout/` | Logs out, clearing session          |

## Error Handling

The application provides informative error messages for common issues:
- **400 Bad Request**: Returned for invalid input or missing fields.
- **401 Unauthorized**: Returned when authentication fails or token is invalid.
- **405 Method Not Allowed**: Returned when an unsupported HTTP method is used.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

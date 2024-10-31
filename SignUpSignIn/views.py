import jwt
import re
from datetime import datetime
from django.contrib.auth import authenticate, logout, get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

User = get_user_model()


# Utility function to generate JWT token
def generate_jwt_token(user):
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
        'iat': datetime.now()
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token


# Utility function to verify JWT token
def verify_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user = User.objects.get(id=payload['user_id'])
        return user
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
        return None


@api_view(['GET'])
def index(request):
    # Check for access_token in cookies
    token = request.COOKIES.get('access_token')
    if not token or not verify_jwt_token(token):
        return Response({"error": "Authentication required"}, status=401)

    # Example of a protected view
    return Response({"message": "Welcome, authenticated user!"}, status=200)


@api_view(['POST'])
def signup(request):
    profile_picture = request.FILES.get('profile_picture')
    username = request.data.get("username")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    email = request.data.get("email")
    password = request.data.get("password")
    confirm_password = request.data.get("confirm_password")

    # 1. Required Fields Validation
    if not all([username, first_name, last_name, email, password, confirm_password]):
        return Response({"error": "All fields are required."}, status=400)

    # 2. Password Validation
    if password != confirm_password:
        return Response({"error": "Passwords do not match."}, status=400)
    if len(password) < 8:
        return Response({"error": "Password must be at least 8 characters long."}, status=400)

    # 3. Username Validation
    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists."}, status=400)
    if len(username) < 3 or len(username) > 20:
        return Response({"error": "Username must be between 3 and 20 characters."}, status=400)
    if not re.match(r'^\w+$', username):
        return Response({"error": "Username can only contain letters, numbers, and underscores."}, status=400)

    # 4. Email Validation
    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already exists."}, status=400)
    try:
        validate_email(email)
    except ValidationError:
        return Response({"error": "Invalid email format."}, status=400)

    # 5. Profile Picture Validation (optional)
    if profile_picture:
        if not profile_picture.content_type in ["image/jpeg", "image/png"]:
            return Response({"error": "Profile picture must be a JPEG or PNG image."}, status=400)
        if profile_picture.size > 5 * 1024 * 1024:  # 5 MB limit
            return Response({"error": "Profile picture file size should not exceed 5 MB."}, status=400)

    # 6. Optional Fields Validation
    if first_name and len(first_name) > 30:
        return Response({"error": "First name should not exceed 30 characters."}, status=400)
    if last_name and len(last_name) > 30:
        return Response({"error": "Last name should not exceed 30 characters."}, status=400)

    # 7. User Agreement or Terms of Service (optional)
    # You may add a checkbox for terms acceptance and validate here.

    # If all validations pass, create the user
    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email
    )
    if profile_picture:
        user.profile_picture = profile_picture
    user.save()

    # Return success response
    return Response({
        "message": "User registered successfully. Please log in to continue.",
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "email": email
    }, status=201)


@api_view(['POST'])
def signin(request):
    username = request.data.get("username").strip()
    password = request.data.get("password").strip()

    if not User.objects.filter(username=username).exists():
        return Response({"error": "Username doesn't exist, do SignUp."}, status=400)

    user = authenticate(request, username=username, password=password)
    if user is not None:
        # Check if the token already exists in the cookies
        token = request.COOKIES.get('access_token')

        # Verify the token if it exists
        if token and verify_jwt_token(token):
            return Response({"message": "User is already authenticated."}, status=200)

        # Generate a new JWT token since it doesn't exist or is invalid
        token = generate_jwt_token(user)

        response = Response({
            "username": username,
            "message": "User authenticated successfully."
        }, status=200)

        # Set the access token as an HTTP-only cookie
        response.set_cookie(
            key='access_token',
            value=token,
            httponly=True,
            expires=datetime.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        )
        return response
    else:
        return Response({"error": "Authentication failed."}, status=401)


@api_view(['POST'])
def handle_logout(request):
    # Clear the access token cookie
    response = Response({"message": "Logged out successfully"}, status=200)
    response.delete_cookie('access_token')
    logout(request)
    return response

# GuardiaPass
#### Video Demo: <URL HERE>
#### Description:
GuardiaPass is a secure password management tool designed to help users store and organize their credentials safely. This project focuses on implementing robust encryption methods and user-friendly interfaces to make password management both secure and convenient.

Key Features:
* Secure password storage using industry-standard encryption
* Easy-to-use interface for managing multiple accounts
* Password generation capabilities

This project was developed as part of a security-focused final project for CS50.

Project Files Description

- `app.py`: Core application factory that sets up the Flask environment. It initializes crucial components like Flask-Login for user authentication, registers all blueprints (auth, main, and API routes), configures the secret key for session management, and sets up the user loader function for maintaining user sessions.

- `run.py`: Application entry point that handles the server initialization. It includes custom error handlers for 404 and 500 errors, configures the development/production environment settings, and manages the application lifecycle. This file is responsible for starting the Flask development server with the appropriate configuration.

- `config/config.py`: Configuration management system that defines different environment settings:
  - Development configuration with debug mode and local settings
  - Production configuration with secure cookie settings and enhanced security measures
  - Testing configuration for running unit tests with an in-memory database
  - Security parameters: PBKDF2 iterations (100,000), salt length (16 bytes), minimum password length (12)

- `models/`: Core data structure and database interaction layer
  - `__init__.py`: Database initialization module that sets up SQLAlchemy and creates necessary database tables
  - `password.py`: Password model that handles the encryption, storage, and retrieval of user passwords using Fernet encryption
  - `user.py`: Comprehensive user model implementing Flask-Login's UserMixin. Manages user authentication with password hashing (scrypt), session handling, and master key management for password encryption/decryption

- `routes/`: Application routing and business logic layer
  - `api.py`: RESTful API endpoints that handle password operations:
    - Password generation with customizable parameters
    - CRUD operations with input validation
    - Password strength checking
    - Secure password retrieval with proper authentication
  - `auth.py`: Authentication system that manages:
    - User registration with password strength validation
    - Secure login with session management (30-minute lifetime)
    - Logout functionality
    - Password strength checking endpoints
  - `main.py`: Basic view routes:
    - Landing page with authentication check
    - Dashboard view for password listing
    - Password management interface
    - User profile with password statistics

- `templates/`: Frontend interface templates using Jinja2
  - `base.html`: Master template with common elements like navigation, footer, and security headers (CSP, HSTS)
  - `dashboard.html`: Main user interface displaying stored passwords with search and filter options
  - `index.html`: Landing page with feature showcase and security information
  - `login.html`: Authentication form with CSRF protection
  - `manage.html`: Password management interface with encryption status
  - `register.html`: User registration form with password strength indicators

- `utils/`: Helper modules for security and functionality
  - `encryptor.py`: Encryption utility that implements:
    - Fernet encryption (AES-128-CBC) with HMAC authentication
    - Key derivation via PBKDF2-HMAC-SHA256 (100k iterations)
    - Random salt generation (16 bytes)
    - Secure key encoding (URL-safe Base64)
  - `password_generator.py`: Advanced password generation tool featuring:
    - Customizable password length and complexity
    - Special character inclusion
    - Entropy calculation
    - Password strength validation

- `passwords.db`: SQLite database file storing encrypted user data and passwords using secure schemas. It's created and managed automatically by SQLAlchemy, in the start up of the application.

- `requirements.txt`: Project dependencies including:
  - Flask framework and extensions (Flask-Login)
  - Cryptography libraries (cryptography)
  - Database ORM (SQLAlchemy)
  - Security packages
  - Development tools

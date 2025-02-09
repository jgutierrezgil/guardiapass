# GuardiaPass - Secure Password Management System

#### Video Demo: <URL HERE>

## Project Overview
GuardiaPass is a comprehensive password management solution that prioritizes both security and user experience. Built with modern web technologies and implementing industry-standard encryption methods, it provides a secure vault for storing and managing sensitive credentials while maintaining an intuitive and user-friendly interface.

## Core Features
- **Advanced Encryption**: Implements AES-128-CBC with HMAC authentication for secure password storage
- **Intuitive Dashboard**: Real-time statistics and password health monitoring
- **Password Generator**: Customizable password creation with entropy analysis
- **Security Analysis**: Continuous password strength assessment and recommendations
- **User Profiles**: Personalized security settings and preferences
- **Responsive Design**: Modern interface built with Bootstrap 5.3.0

## Detailed File Structure and Functionality

### Core Application Files

#### `app.py` - Application Factory
The cornerstone of GuardiaPass, this file implements the Factory pattern to create Flask application instances. Key responsibilities:
- Initializes Flask-Login for secure user authentication
- Configures session management with secure defaults
- Registers blueprints for modular functionality
- Sets up user loading mechanisms
- Configures security headers and CSRF protection
- Initializes database connections

#### `run.py` - Application Entry Point
Manages the application's lifecycle and server configuration:
- Implements custom error handlers (404, 403, 500)
- Configures environment-specific settings
- Sets up logging with rotation
- Manages debug/production modes
- Handles graceful shutdown
- Provides CLI interface for management commands

### Configuration Management

#### `config/config.py` - Configuration Handler
Implements a comprehensive configuration system:
- Defines separate environments (development, testing, production)
- Manages security parameters:
  * PBKDF2 iterations (100,000)
  * Salt length (16 bytes)
  * Session timeout settings
  * Cookie security options
- Configures database connections
- Sets logging levels and formats
- Manages environment variables

### Data Models

#### `models/password.py` - Password Management
Implements the core password functionality:
- Secure password storage using Fernet encryption
- Password metadata management
- Creation and modification timestamps
- URL and username storage
- Password strength calculation
- History tracking
- Category management
- Search functionality

#### `models/user.py` - User Management
Handles user-related operations:
- User authentication with scrypt hashing
- Session management
- Master key generation and storage
- Password reset functionality
- Profile management
- Security preferences
- Activity logging

#### `models/__init__.py` - Database Initialization
Manages database setup and configuration:
- SQLAlchemy initialization
- Model registration
- Migration management
- Index creation
- Foreign key constraints
- Connection pooling

### Route Handlers

#### `routes/api.py` - RESTful API
Provides programmatic access to GuardiaPass features:
- Password CRUD operations
- Batch operations support
- Password generation endpoints
- Strength analysis API
- Search functionality
- Export capabilities
- Rate limiting
- Input validation
- Error handling

#### `routes/auth.py` - Authentication System
Manages user authentication and security:
- User registration with validation
- Secure login implementation
- Password reset workflow
- Session management
- Security question handling
- Two-factor authentication support
- Brute force protection
- Account recovery

#### `routes/main.py` - Core Routes
Handles primary application views:
- Dashboard rendering
- Password management interface
- Profile settings
- Statistics generation
- Search functionality
- Category management
- Export/Import features
- Settings management

### Template System

#### `templates/base.html` - Base Template
Provides the foundation for all pages:
- Responsive navigation
- Security headers
- Asset management
- Error handling
- Notification system
- Modal components
- Form validation
- CSRF protection

#### `templates/dashboard.html` - Main Interface
Implements the primary user interface:
- Password list with filtering
- Security statistics
- Quick actions
- Search interface
- Category management
- Password health indicators
- Recent activity log

#### `templates/profile.html` - User Profile
Manages user-specific features:
- Security preferences
- Master password management
- Two-factor settings
- Activity history
- Export options
- Account deletion
- Password statistics

#### `templates/manage.html` - Password Management
Provides password manipulation interface:
- Password creation/editing
- Strength indicators
- Category assignment
- History viewing
- Sharing options
- Bulk operations
- Search functionality

### Security Utilities

#### `utils/encryptor.py` - Encryption System
Implements cryptographic operations:
- AES-128-CBC encryption
- HMAC authentication
- Key derivation (PBKDF2)
- Salt generation
- Key rotation
- Secure deletion
- Format preservation
- Error handling

#### `utils/password_generator.py` - Password Generation
Provides password creation functionality:
- Configurable complexity
- Entropy calculation
- Character set management
- Pattern prevention
- Length validation
- Strength assessment
- Format validation

### Database

#### `passwords.db` - SQLite Database
Manages persistent storage:
- Encrypted password storage
- User data management
- Session tracking
- Activity logging
- Backup support
- Index optimization
- Referential integrity

### Additional Components

#### `scripts/` - Utility Scripts
Contains maintenance and management scripts:
- Database migrations
- Key rotation
- Backup management
- Test data generation
- Health checks
- Performance monitoring
- Cleanup routines

#### `requirements.txt` - Dependencies
Lists project dependencies:
- Flask framework (core and extensions)
- Cryptography libraries
- Database ORM (SQLAlchemy)
- Security packages
- Testing frameworks
- Development tools
- Documentation generators

## Security Implementation

GuardiaPass implements multiple security layers:
1. **Encryption**: AES-128-CBC with HMAC
2. **Authentication**: Scrypt password hashing
3. **Session Security**: Secure cookies and timeout
4. **Input Validation**: Both client and server-side
5. **CSRF Protection**: All forms and API endpoints
6. **XSS Prevention**: Content Security Policy
7. **Error Handling**: Custom error pages
8. **Logging**: Detailed security event tracking
9. **Rate Limiting**: Brute force prevention
10. **Secure Headers**: HSTS, XFO, etc.

## Development and Testing

The project includes comprehensive testing:
- Unit tests for all components
- Integration testing
- Security vulnerability scanning
- Performance benchmarking
- Load testing
- UI/UX testing
- Cross-browser compatibility

## Deployment

Deployment considerations include:
- Environment configuration
- Database setup
- Backup procedures
- Monitoring setup
- Security hardening
- Performance optimization
- SSL/TLS configuration
- Load balancing

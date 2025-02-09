# GuardiaPass - Secure Password Management System

#### Video Demo: <URL HERE>

#### Description
GuardiaPass is a comprehensive password management solution that prioritizes both security and user experience. Built with modern web technologies and implementing industry-standard encryption methods, it provides a secure vault for storing and managing sensitive credentials while maintaining an intuitive and user-friendly interface.

## Core Features
- **Advanced Encryption**: Implements AES-128-CBC with HMAC authentication for secure password storage
- **Intuitive Dashboard**: Real-time statistics and password health monitoring
- **Password Generator**: Customizable password creation with entropy analysis
- **Security Analysis**: Continuous password strength assessment and recommendations
- **User Profiles**: Personalized security settings and preferences
- **Responsive Design**: Modern interface built with Bootstrap 5.3.0

## Detailed File Structure and Functionality

Below is a detailed description of the most relevant files and directories:

---

## 1. App.py
This file is the main entry point of the application.

- **create_app():** Responsible for setting up the Flask application, including:
  - Defining the secret key (SECRET_KEY) required for secure session management.
  - Configuring the Flask-Login LoginManager, specifying the login view (login_view) and the function to load the user into the session (user_loader).
  - Registering the blueprints (auth, main, and api), which are independent modules responsible for handling different sets of routes.
  - Initializing the database with `init_db()`.
  - Running the application in development mode (debug=True) if the file is executed directly (`if __name__ == '__main__': ...`).

This modular structure makes the code more maintainable, allowing each group of routes or functionality to be split into distinct blueprints. Additionally, having a `create_app()` function simplifies integration with testing tools, as you can create an application for tests with the same configuration.

---

## 2. routes/api.py
This file defines the `api` blueprint, which groups all the API endpoints related to the CRUD operations for passwords and password generation:

- **GET /passwords:** Returns all the passwords of an authenticated user.  
- **POST /passwords:** Creates a new password in the database.  
- **GET /passwords/<int:password_id>:** Retrieves details of a specific password.  
- **PUT /passwords/<int:password_id>:** Updates a password’s data.  
- **DELETE /passwords/<int:password_id>:** Deletes a password.  
- **POST /passwords/generate:** Generates a new password based on configurable criteria (length, use of uppercase, digits, special characters, etc.).  
- **POST /passwords/check-strength:** Checks the strength of a password, returning relevant information such as length and complexity.

The `@login_required` decorator is used on each route to ensure that only authenticated users can access these functionalities. Standard errors (404 and 500) are also centrally handled within this module, returning JSON-format responses to keep the API consistent.

---

## 3. routes/auth.py
This file contains the `auth` blueprint, in charge of managing everything related to user authentication and registration:

- **GET/POST /login:** Allows a user to log in with their username and password. It uses Flask-Login’s `login_user()` function to establish the session.
- **GET/POST /register:** Enables creating a new user account. It checks whether the username already exists, confirms that the passwords match, and verifies password strength using the `PasswordGenerator` class.
- **GET /logout:** Logs out the user, clearing session information (including `master_key`).
- **POST /check-password-strength:** An endpoint that returns the strength of a given password, useful for dynamic validation.

Having a separate blueprint for authentication logic helps maintain order and readability, making it easy to maintain or modify these routes without affecting the primary API layer.

---

## 4. routes/main.py
This file defines the `main` blueprint, which manages the main views of the application (the pages the user sees when browsing the web):

- **GET /**: Home page. If the user is already authenticated, they are redirected to the dashboard so they are not forced to log in again.
- **GET /dashboard:** Main view that shows a summary of saved passwords. It lists all the user’s credentials.
- **GET /manage:** Page for advanced password management (a broader interface for creating or editing).
- **GET /profile:** Displays user statistics, such as the number of unique domains, how many old passwords exist, a record of recent activities, and a breakdown of password strength (how many are weak, moderately strong, or strong).

Additionally, functions are added to the Jinja2 context (for example, `now=lambda: datetime.now(timezone.utc)`) so they can be used in the templates, facilitating the inclusion of date and time data in the views.

---

## 5. models/user.py
Defines the `User` model using SQLAlchemy. It includes:

- Attributes such as `username`, `password_hash`, `master_key`, and a relationship with the `Password` model.
- Static methods for creating a new user (`create`) and for retrieving a user by ID or username.
- The functionality of `set_password` and `check_password` using Werkzeug for password hashing, enhancing credential security.
- Integration with Flask-Login via the `UserMixin` class, providing methods and attributes to handle sessions in Flask.
- Methods like `get_passwords`, `add_password`, `update_password`, and `delete_password` to interact with the user's passwords, internally encrypting and decrypting credentials using the `master_key`.

The primary design decision here was to centralize per-user encryption logic in one place, simplifying maintenance and ensuring each user has a unique master key.

---

## 6. models/password.py
Models the table that stores passwords:

- Includes fields such as `name`, `url`, `username`, `encrypted_password`, and `comments`.
- The `create` method encrypts the received password before saving it to the database, using a `PasswordEncryptor` with the `master_key`.
- Exposes methods to retrieve all passwords for a user, update, and delete them.
- `to_dict` lets you convert information into a dictionary, which may or may not include the decrypted password, as needed.

Here, the decision was made to store only the encrypted password in the database for greater security. The decrypted password is never stored in plain text, and decryption is only performed when explicitly requested using the `master_key`.

---

## 7. models/__init__.py
This file initializes the SQLAlchemy `db` object and provides the `init_app` function that:

- Binds the database instance (`db`) to the Flask application.
- Imports the `User` and `Password` models to avoid circular reference issues.
- Creates the tables in the database with `db.create_all()` within the application context.

This configuration ensures the database is properly initialized every time the application starts up. You can switch to a different database (for example, PostgreSQL or MySQL) by modifying the connection string in the Flask configuration, without needing to change most of the application code.

---

## 8. Notable Design Decisions
- **Use of Blueprints:** The project was split into multiple blueprints (`auth`, `main`, and `api`) for modularity. This fosters scalability and readability, as each set of routes belongs to a coherent scope.
- **Flask-Login:** Chosen to handle session and authentication easily and seamlessly with Flask. This library provides ready-to-use functionalities, such as protecting routes with decorators and managing session cookies securely.
- **Encryption with Master Key:** Each user has a master key, rather than using a single global key. This offers a higher level of security, as accessing one user’s data does not automatically compromise everyone else’s passwords.
- **Separation of Responsibilities:**
  - The models (`user.py` and `password.py`) handle database logic and encryption.
  - The files in `routes` focus on routing and business logic, communicating with the models.
  - `App.py` handles the initial creation and configuration of the application.
- **Password Validation:** The `PasswordGenerator` class is implemented to validate and measure password strength, encouraging users to adopt more secure credentials. Additionally, there is an endpoint to generate complex and secure passwords.
- **Extensibility:** Thanks to the defined structure, adding new features (for example, exporting passwords to a CSV or integrating two-factor authentication) is relatively straightforward, without having to overhaul the entire project.

---

## 9. run.py
This file works as an alternate (or main, depending on configuration) entry point to run the application in a production or development environment with specific configurations. Unlike `App.py`, it places special emphasis on environment-based settings, log management, and centralized error handling:

### Loading Environment Variables
It uses the `python-dotenv` library (`load_dotenv()`) to load environment variables defined in a `.env` file. This facilitates separating configuration from the code, allowing sensitive data or deployment parameters (e.g., `SECRET_KEY`, `DATABASE_URL`, or `FLASK_ENV`) to remain hidden in the repository.

### create_app(config_name='default')
- Creates the Flask application and configures it with the appropriate configuration class (`app.config.from_object(config[config_name])`), imported from `config/config.py`.
- Initializes the `LoginManager` to handle user authentication, defining the login view (`login_view = 'auth.login'`) and status messages for the user.
- When `app.debug` is disabled, it sets up a logging system with `RotatingFileHandler` to store logs in a file (by default, `logs/guardiapass.log`). This is useful in production to diagnose problems and maintain an event history.
- Registers the main application blueprints:
  - `auth` for authentication (prefixed with `/auth`)
  - `main` for generic views and the dashboard
  - `api` for handling passwords and the password generator functionalities (prefixed with `/api`)
- Calls `init_app(app)` to initialize the database, consistent with the rest of the project.

### register_error_handlers(app)
This function registers several custom error handlers (404, 500, 403, and 405). For each error, a specific message is logged (info or error level) and the user is redirected to the corresponding template in `errors/<code>.html`. This approach:

- Centralizes the logic for handling common HTTP errors.
- Allows displaying user-friendly or more detailed messages and templates.

### Main Block (`if __name__ == '__main__': ...`)
- Instantiates the application with the configuration obtained from the `FLASK_ENV` environment variable, or `'default'` if it is not set.
- Determines the application’s port (`PORT`) from environment variables, providing flexibility in deployment across various environments.
- Finally, launches the application via `app.run(...)`.

---

## 10. config.py
This file centralizes all of the application’s configuration, making it easy to adjust for different environments (development, production, or testing). Environment variables are used with `python-dotenv` to separate sensitive settings from the codebase, easing security and deployment management.

### Class Config
Defines default values for:
- **SECRET_KEY:** Used by Flask to protect sessions and cookies. In production, it is recommended to set this to a long and secure string (usually in an environment variable).
- **SQLALCHEMY_DATABASE_URI:** Database path. By default, it’s set to use a local SQLite file (`passwords.db`).
- **SQLALCHEMY_TRACK_MODIFICATIONS:** Disables object modification tracking to save resources.
- Security and password-related parameters (`PBKDF2_ITERATIONS`, `SALT_LENGTH`, etc.), defining the robustness of password encryption.
- **PERMANENT_SESSION_LIFETIME** and **SESSION_COOKIE_HTTPONLY:** Define Flask session settings, such as lifetime and cookie security.

### Specialized Classes
- **DevelopmentConfig:** Inherits from `Config` and enables DEBUG mode to speed up development. It also disables `SESSION_COOKIE_SECURE`, allowing HTTP instead of HTTPS.
- **ProductionConfig:** Disables debug mode and forces the use of secure cookies (`SESSION_COOKIE_SECURE = True`), assuming HTTPS will be used in production to protect traffic.
- **TestingConfig:** Defines a configuration for unit tests. For example, it uses an in-memory database (`SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'`), facilitating isolated test execution without impacting real data.

### config Dictionary
Consolidates the different configuration classes to select the desired environment type. Typically, you aim at 'default' (or 'development') if no specific environment is provided.

---

## 11. utils/encryptor.py
This file defines the `PasswordEncryptor` class, which securely encrypts and decrypts passwords. It uses the `cryptography` library (specifically, `Fernet`), which offers high-level symmetric encryption. Key functionalities include:

### Initialization
- The `__init__` constructor optionally receives a key. If not provided, a new one is generated using `Fernet.generate_key()`.
- It stores and exposes the key in the `key` property, allowing reuse to decrypt data later.

### Encryption and Decryption
- **encrypt(password):** Converts the password to bytes (`.encode()`) and then calls `self.fernet.encrypt(...)`. The result is returned as a base64-encoded string.
- **decrypt(encrypted_password):** Performs the inverse process (`self.fernet.decrypt(...)`) and then decodes the result.
  
### Master Key
- **generate_key_from_master(master_password, salt=None):** Derives an encryption key from a master password using PBKDF2HMAC with SHA256.
- If no salt is provided, a random one is generated (`os.urandom(16)`).
- Returns the key in a Fernet-safe format (`base64.urlsafe_b64encode`) along with the generated salt.
- This strategy ensures that two users with the same master password do not produce the same key unless they also share the same salt.

### Key Verification
- **verify_key(key):** Checks if a key is valid for Fernet by attempting to instantiate `Fernet(key)` and returns `True` or `False` accordingly.

This simple, modular approach centralizes encryption logic in a single class, making it easy to maintain and update (e.g., increasing PBKDF2 iterations or changing the hashing algorithm in the future).

---

## 12. utils/password_generator.py
This class, `PasswordGenerator`, provides advanced methods for generating and validating passwords:

### Password Generation
- **generate_password(...):** Receives several parameters (length, use of uppercase, digits, special characters, extended characters, etc.) to customize the password.
- Ensures that the length is within a safe range (12 to 60 characters by default) and builds a character set (`charset`) based on selected options.
- Uses the `secrets` library to choose cryptographically secure random characters to form the final password.
- Guarantees the generated password contains at least one character of each chosen type (if digits are selected, at least one digit, etc.).

### Strength Measurement
- **measure_strength(password):** Evaluates the password according to factors like length, presence of uppercase letters, digits, special characters, extended characters, and repetitive patterns.
- Assigns a score based on these criteria and determines a strength level (Very Strong, Strong, Moderate, or Weak).
- Returns a dictionary that includes the score, the classification (`strength`), and a list of comments (`feedback`).

### Password Validation
- **validate_password(password):** Checks if the password meets minimum requirements (length, variety of characters, etc.).
- Returns a tuple `(bool, list)`, where `bool` indicates whether the password is valid and `list` contains messages related to errors or non-compliance.

Using this class encourages the creation and use of robust passwords by offering an easy way to generate random passwords and immediate feedback on security level for credentials entered by the user.

---

## 13. templates/base.html
This file serves as a base layout template for all views in the application. It uses Jinja2 (Flask’s template engine) to define blocks that each specialized page can extend and customize.

### HTML Structure and Resources
- Starts with `<!DOCTYPE html>` and `<html lang="es">`.
- Includes essential metadata and a `<title>` tag wrapped in a `{% block title %}` so that each page can override the title.
- Imports Bootstrap 5 from a CDN for styling and Font Awesome for icons.
- Also loads essential JS files from Bootstrap, Popper.js, and SweetAlert for interactive notifications.

### Custom Styles
- A set of CSS variables (e.g., `--primary-color`, `--accent-color`, etc.) is defined to facilitate changing the color palette of the application.
- Styles for the navigation bar (`.navbar`), footer, cards (`.card`), tables, and transitions (e.g., `fade-in`) are added.
- Content blocks have a light background (`var(--light-bg)`) with a responsive layout to ensure correct display on various screen sizes.

### Navigation Bar
- A top `navbar` containing links to different sections of the application (Dashboard, Management, Profile, etc.).
- Through `{% if session.get('_user_id') %}`, the template checks if the user is authenticated to display the corresponding options (or login/register links otherwise).
- The application logo/title links to the main view (`main.index`) and is accompanied by a Font Awesome icon (`fa-shield-alt`).

### Flash Messages
- Just below the navigation bar, a container is defined to handle flash messages (notifications) such as confirmations or errors.
- Uses `get_flashed_messages(with_categories=true)` to iterate over categorized messages (success, error, etc.) and display them in a Bootstrap alert component.

### Content Blocks
- **`{% block content %}`**: Located in a `<main>` with top and bottom margins. Each application view inserts its HTML content into this block.
- **`{% block extra_css %}`**: Allows injecting additional CSS into the `<head>` if needed for specific views.
- **`{% block scripts %}`**: Placed at the end of the `<body>`, where scripts or JavaScript logic for each child template can be added.

### Footer
- At the end of the page, a `<footer>` with a dark background (primary color) and light text is included. It shows copyright information and a reference to the project.

### Custom Scripts
- Defines two JavaScript functions for handling notifications (`showNotification`) and action confirmations (`confirmAction`), implemented with SweetAlert:
  - **showNotification(title, message, type):** Displays a floating toast notification in the top-right corner.
  - **confirmAction(title, text, callback):** Launches a modal prompting the user to confirm or cancel the action; if confirmed, the `callback()` function is executed.

---

## 14. templates/index.html
This file serves as the application’s home or landing page. Unlike most views, it does not directly extend `base.html` but includes many of the styles and navigation elements found in that base template.

### Header and Styles
- Uses Bootstrap 5 and Font Awesome from CDNs for styling and icons.
- Defines inline styles similar to those in `base.html` (`:root`, color variables, `.navbar`, etc.). This ensures aesthetic coherence with the rest of the application, though in a more consolidated project you might reuse `base.html` via `{% extends %}`.

### Navigation Bar
- Displays a `navbar` with the application’s logo (a shield icon and the name “GuardiaPass”).
- Shows different links depending on whether there is an authenticated user, checking `session.get('_user_id')`.
- Buttons for “Management” or “Dashboard” if the user is logged in, and “Log In” or “Register” otherwise.

### Flash Messages
- Iterates over flash messages and displays them in a Bootstrap `.alert` container for temporary notifications or errors.

### Main Content
- Occupies the page’s `<main>` and includes a welcome message and some personal info as an introduction: project name, student name, GitHub link, and ePortfolio.
- It’s an ideal place to describe the application’s purpose and highlight that it is a CS50 final project.

### Footer
- A `<footer>` with a dark background and light text (defined through the CSS variables).
- Mentions copyright and references the final project.

In summary, `index.html` acts as an intro page that quickly introduces the tool and provides information about its author.

---

## 15. templates/dashboard.html
This view extends the base template (`base.html`) using `{% extends "base.html" %}`, seamlessly integrating with its structure and styles. Its main goal is to display and manage passwords and provide access to the password generator.

### Password Generation
- On the left side (`col-md-6`), there is a form to set password parameters (length, use of uppercase, digits, special chars, etc.).
- Submitting the form sends an AJAX request to `/api/passwords/generate`, and the generated password is displayed along with its strength level (a badge indicating feedback).
- Includes a button to copy the password to the clipboard (`copyPassword()`).

### NIST Information
- On the right side (`col-md-6`), information about the National Institute of Standards and Technology (NIST) is provided, along with relevant publication links.
- A brief note explains how to find NIST key generation guidelines, such as NIST SP 800-133.

### List of Saved Passwords
- Below, a section labeled “My Passwords” (`<table class="table">`) is displayed.
- Dynamically filled with data from the `/api/passwords` route. For each password, columns like “Name,” “URL,” “User,” “Password,” and “Comments” are shown.
- The password is initially masked (********), and a toggle button lets the user show/hide it.

### Additional Scripts
In the **`{% block scripts %}`**:
- JavaScript to:
  - Generate a new password via AJAX and handle the response.
  - Fetch the list of passwords from the backend (`fetchPasswords()`) and render it in the table.
  - Toggle each password’s visibility in the table with a Font Awesome icon (`fa-eye` / `fa-eye-slash`).
  - Copy the password to the clipboard (`copyPassword()`).

This dashboard provides users with a comprehensive environment to manage their credentials. It integrates with the Flask `/api` for creating, reading, and exploring passwords and features a dynamic generator that encourages the use of secure passwords according to recognized standards (NIST).

---

## 16. templates/login.html
This template is based on the base template (`base.html`) and shows a login form. Key details:

### Login Form
- Fields: “Username” (`username`) and “Master Password” (`password`).
- Action: Submits data via `method="POST"` to the endpoint defined in `auth.login`.
- The password can be shown/hidden via a button that triggers a JavaScript function toggling the input field’s `type` between `password` and `text`.
- A note indicates that the master password cannot be edited once created. If forgotten, users should contact the administrator.

### Design and Styles
- Inherits the general styles from `base.html`, including the navbar, footer, and color variables.
- The form’s main structure (card with classes `card`, `card-header`, `card-body`) uses Bootstrap, ensuring a clean and responsive interface.

### Additional Links
- At the end of the form, there is an option to “Register” if the user does not have an account, linking to `auth.register`.

---

## 17. templates/register.html
Similarly extends `base.html` and shows a registration form for users. Main functionalities:

### Registration Form
- Fields: “Username” (`username`), “Master Password” (`master_password`), and “Confirm Password” (`confirm_password`).
- **Validations:**
  - Displays a strength indicator for the master password. When the user types into `master_password`, a JS function (`measurePasswordStrength`) calculates a score based on length and character diversity.
  - A progress bar (`progress-bar`) changes color depending on the score.
  - Before submitting, checks that `master_password` and `confirm_password` match. If not, submission is stopped and an error notification (`showNotification`) is displayed.

### Strength Indicator
- Implemented using a progress bar (`<div id="passwordStrength">`) that updates in real time.
- The score increases based on simple rules (length, uppercase, lowercase, digits, special characters).
- If the score is low, the bar is red (`bg-danger`), yellow (`bg-warning`) for intermediate values, or green (`bg-success`) for a stronger password.

### Notes and Warnings
- Emphasizes that the master password cannot be changed later.
- Suggests users contact the administrator if they forget it, as there is no built-in recovery functionality in this version.

### Additional Links
- If the user already has an account, they can return to the “Log In” form via the link to `auth.login`.

---

## 18. templates/manage.html
This template also extends `base.html` and provides a more complete environment for creating, viewing, updating, and deleting the user’s stored passwords. It is divided into two main sections:

### Add Password Form
- Includes fields such as “Name,” “URL,” “Username,” and “Password.”
- In the password section, there are two buttons:
  - Show/Hide the password (using an eye icon).
  - Generate a random password, which displays a mini generator with length and special character options, etc.
- After filling out and submitting the form with `id="addPasswordForm"`, an AJAX call to the `/api/passwords` route (POST method) is made to store the new password.

### Password List
- Displayed in a table with columns for “Name,” “URL,” “Username,” “Password” (masked as ********), “Comments,” and “Actions.”
- Action buttons include:
  - **Edit:** When clicked, the row becomes editable in place; text fields appear and “Save” or “Cancel” buttons replace the original view.
  - **Delete:** Triggers a confirmation modal (`#deleteModal`), and if the user confirms, a DELETE request is sent to `/api/passwords/<id>`.
- Additional JS functions assist with:
  - Toggling password visibility (`togglePasswordBtn`).
  - Generating and assigning random passwords to fields quickly (`generateAndSetPassword`).
  - Loading and rendering the password list (`loadPasswords`) from the API every time a change occurs (create, edit, delete), ensuring the table is always up-to-date with the database.

---

## 19. templates/profile.html
Also extends `base.html` and offers a detailed view of user profile data, where metrics and statistics about passwords are grouped:

### General Statistics
- **Total Passwords** (`passwords|length`).
- **Unique Domains** (`unique_domains`).
- **Last Update** (`last_update`).
- **Old Passwords** (over 90 days without updates).

### Password Strength
- Displays a progress bar with three segments (weak, medium, strong) in red, yellow, and green, respectively.
- Each segment shows the number of credentials falling into each category. An alert is also shown if the user has weak passwords.

### Recent Activity
- Lists the last five passwords created (or similar actions) with their date, site, and action performed (“Created,” for example).
- If there is no activity, a message “No recent activity” is displayed.

### Old Passwords
- A separate table groups credentials older than 90 days.
- Includes buttons to “Generate” a new password and “Update” the existing one, integrated with the API so the user can quickly renew outdated passwords.

### Adherence to Naming Conventions

Throughout the development of this project, we have made a conscious effort to follow established naming conventions in both Python and JavaScript. This includes:

1. **Python**  
   - **Module Names**: Lowercase with underscores (e.g., `password_generator.py`, `encryptor.py`).  
   - **Class Names**: Follows the [PEP 8](https://peps.python.org/pep-0008/) recommendation for [CapWords](https://peps.python.org/pep-0008/#class-names), such as `PasswordGenerator` and `PasswordEncryptor`.  
   - **Function and Variable Names**: Typically lowercase, with words separated by underscores (e.g., `create_app()`, `init_db()`).  
   - **Constants**: Uppercase and underscored, for example, in the `config.py` file (`PBKDF2_ITERATIONS = 100000`).

2. **JavaScript**  
   - **Variables and Functions**: CamelCase for function and method names (e.g., `generatePassword()`, `copyPassword()`), while local variables also generally follow CamelCase (e.g., `generatedPassword`).  
   - **Event Handlers**: Named in a self-describing way that clarifies their purpose (e.g., `addEventListener('click', function() {...})`).  
   - **Constants**: Often declared with capitalized names and underscores (though usage may vary depending on context), to indicate that they remain unchanged.

### Architecture and Patterns Summary

**Design Patterns Implemented**
- **Factory Method**: In `create_app()` (within both `app.py` and `run.py`), which creates configurable Flask instances.
- **Repository Pattern**: Basic implementation in the `User` and `Password` models, relying on static methods for data access.
- **Strategy Pattern**: Used by `PasswordGenerator` and the encryptor class (`PasswordEncryptor`), providing interchangeable algorithms.

*(Note: Although `Singleton` usage was considered via `current_app.config`, it was not explicitly implemented; I have done what I could within the project's scope.)*

---

**SOLID Principles**
- **Single Responsibility**: 
  - Achieved by splitting core entities into separate models (`User` vs. `Password`).
  - Some overlap remains where routes also handle business logic, but efforts have been made to keep them organized.
- **Open/Closed**: 
  - Extensible configurations for different environments (`DevelopmentConfig`, `ProductionConfig`).
  - Static methods in models are functional but could be refined further for easier extension.
- **Liskov Substitution**: 
  - Not heavily relevant due to limited inheritance.
- **Interface Segregation** and **Dependency Inversion**: 
  - I have aimed to keep dependencies manageable, though some direct coupling (e.g., SQLAlchemy in models) persists.
  - I have done our best given the current scope and project requirements.

---

**Clean Architecture**
- I have partially applied its principles, such as separating models (entities) and routes (use cases). 
- However, frameworks like Flask/SQLAlchemy remain intertwined in the codebase. 
- Overall compliance is modest, but we have implemented much of what was feasible within the academic scope of this project.

# Improvement Opportunities

1. **Service Layer**:
   - Create `services/auth_service.py` and `services/password_service.py`
   - Extract business logic from routes

2. **DTOs**:
   - Implement `PasswordCreateDTO`, `UserUpdateDTO` for centralized validation

3. **Unit of Work Pattern**:
   - Replace static methods in models with repositories

4. **Dependency Inversion**:
   - Define interfaces for critical services (e.g., `IPasswordEncryptor`)
   - Implement dependency injection

5. **Presentation Layer**:
   - Separate HTTP handlers (Flask) from response logic

### Conclusion

Throughout this document, we have delved deep into the various facets and components of our project, highlighting both its strengths and the areas that offer opportunities for growth and improvement. Much like the universe, our project is a system in constant expansion, filled with infinite possibilities and mysteries waiting to be discovered.

Each line of code, each designed architecture, and every decision made represents another step on our journey towards excellence. In crafting this project, we have striven to maximize the knowledge and skills acquired from CS50, leveraging its principles to build a robust and scalable foundation. However, as with any great adventure, there will always be room for innovation and refinement. After all, even the universe, with its countless galaxies and stars, continues to evolve and surprise us with new discoveries.

So, as we continue navigating this vast ocean of bits and bytes, let's remember to keep an open mind and a curious spirit. Because, at the end of the day, while our challenges may seem as vast as the cosmos, so too are our capabilities to overcome them, especially with the solid grounding provided by CS50.

Thank you for joining us on this journey! Now, with a cup of coffee in hand and a smile on our faces, let's keep coding towards the future!

See you in "CS50's Introduction to Cybersecurity"!
# Language-Agnostic Education Platform

Transform education into a language-agnostic experience where learning potential, not language proficiency, determines academic success, making quality education accessible to students worldwide regardless of their native language.

## Product Vision

This platform enables international university students with varying language proficiencies to access quality education without language barriers. It supports professors teaching diverse classrooms and helps university administrators focus on international recruitment and educational equity.

## Target Audience

- **International university students** with varying language proficiencies
- **Professors** teaching diverse classrooms
- **University administrators** focused on international recruitment and educational equity

## Core Features

- Student management (CRUD operations)
- Course management (CRUD operations)
- Enrollment tracking
- Language proficiency tracking
- Multi-language support foundation

## Technology Stack

- **Backend Framework**: FastAPI (Python)
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Architecture**: Modular Monolith

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd /path/to/project
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```

5. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` file and update the configuration values as needed.

## Running the Application

### Development Mode

Run the application with auto-reload enabled:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### API Documentation

Once the application is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Students

- `POST /api/v1/students` - Create a new student
- `GET /api/v1/students` - Get all students (with pagination)
- `GET /api/v1/students/{student_id}` - Get a specific student
- `PUT /api/v1/students/{student_id}` - Update a student
- `DELETE /api/v1/students/{student_id}` - Delete a student

### Courses

- `POST /api/v1/courses` - Create a new course
- `GET /api/v1/courses` - Get all courses (with pagination)
- `GET /api/v1/courses/{course_id}` - Get a specific course
- `PUT /api/v1/courses/{course_id}` - Update a course
- `DELETE /api/v1/courses/{course_id}` - Delete a course

### Health Check

- `GET /health` - Check application health status

## Database

The application uses SQLite by default for development. The database file will be created automatically at `./education_platform.db` when you first run the application.

### Database Models

- **Student**: Stores student information including name, email, native language, and proficiency level
- **Course**: Stores course information including title, description, original language, and instructor
- **Enrollment**: Tracks student enrollments in courses with status and grades

## Environment Variables

Key environment variables (see `.env.example` for full list):

- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Secret key for security features
- `CORS_ORIGINS`: Allowed CORS origins
- `DEBUG`: Enable/disable debug mode

## Project Structure

```
.
├── backend/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database setup
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── requirements.txt     # Python dependencies
│   └── routers/
│       ├── __init__.py
│       ├── students.py      # Student endpoints
│       └── courses.py       # Course endpoints
├── .env.example             # Environment variables template
└── README.md                # This file
```

## Architecture

The application follows a **Modular Monolith** architecture with clear separation of concerns:

- **Routers**: Handle HTTP requests and responses
- **Models**: Define database schema using SQLAlchemy
- **Schemas**: Validate request/response data using Pydantic
- **Database**: Manage database connections and sessions
- **Config**: Centralize application configuration

## Development Guidelines

- Follow PEP 8 style guide for Python code
- Use type hints for better code clarity
- Add logging for important operations
- Validate all user inputs using Pydantic schemas
- Handle errors gracefully with appropriate HTTP status codes
- Keep functions focused and single-purpose

## Security Features

- Input validation using Pydantic
- SQL injection prevention through SQLAlchemy ORM
- CORS configuration for API security
- Environment-based configuration (no hardcoded secrets)

## Future Enhancements

- Authentication and authorization (JWT)
- Real-time translation services integration
- Advanced analytics and reporting
- Mobile application support
- Notification system
- File upload for course materials

## Support

For issues, questions, or contributions, please refer to the project documentation or contact the development team.

## License

[Specify your license here]

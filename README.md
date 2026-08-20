# Educational Platform API

A personalized learning platform API designed for K-12 schools, higher education institutions, teachers, and students. This platform provides adaptive, technology-enhanced learning environments accessible to all institutions regardless of resources.

## Product Vision

Every student receives world-class, personalized education tailored to their unique needs, preparing them for future challenges through adaptive, technology-enhanced learning environments accessible to all institutions regardless of resources.

## Target Audience

- **K-12 Schools**: Primary and secondary educational institutions
- **Higher Education**: Colleges and universities
- **Teachers**: Educators seeking to enhance instruction
- **Students**: Learners requiring personalized education
- **Administrators**: Educational resource and outcome managers

## Core Features

- **Student Management**: Complete CRUD operations for student profiles
- **Course Management**: Create and manage educational courses
- **Personalized Learning**: Track student learning styles and preferences
- **Progress Tracking**: Monitor student enrollment and course progress

## Technology Stack

- **Framework**: FastAPI 0.104.1
- **Database**: SQLAlchemy 2.0.23 with SQLite
- **Validation**: Pydantic 2.5.0
- **Server**: Uvicorn 0.24.0
- **Architecture**: Modular Monolith

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. **Clone the repository** (or navigate to the project directory)

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Linux/Mac:
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
   Edit `.env` file with your configuration settings.

## Running the Application

### Development Mode

Start the FastAPI development server:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive API Documentation**: http://localhost:8000/docs
- **Alternative API Documentation**: http://localhost:8000/redoc

### Production Mode

For production deployment:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Health Check
- `GET /` - Root endpoint
- `GET /health` - Health check endpoint

### Students
- `POST /api/v1/students/` - Create a new student
- `GET /api/v1/students/` - Get all students (with pagination)
- `GET /api/v1/students/{student_id}` - Get a specific student
- `PUT /api/v1/students/{student_id}` - Update a student
- `DELETE /api/v1/students/{student_id}` - Delete a student

### Courses
- `POST /api/v1/courses/` - Create a new course
- `GET /api/v1/courses/` - Get all courses (with pagination)
- `GET /api/v1/courses/{course_id}` - Get a specific course
- `PUT /api/v1/courses/{course_id}` - Update a course
- `DELETE /api/v1/courses/{course_id}` - Delete a course

## Project Structure

```
.
├── backend/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database setup and session management
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic schemas for validation
│   ├── requirements.txt     # Python dependencies
│   └── routers/
│       ├── __init__.py
│       ├── students.py      # Student endpoints
│       └── courses.py       # Course endpoints
├── .env.example             # Environment variables template
└── README.md                # This file
```

## Database Models

### Student
- Personal information (name, email)
- Grade level and learning style preferences
- Enrollment tracking

### Course
- Course details (title, description, subject)
- Difficulty level classification
- Enrollment relationships

### Enrollment
- Links students to courses
- Tracks progress and status
- Enrollment date tracking

## Environment Variables

Key environment variables (see `.env.example`):

- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Secret key for security features
- `ALLOWED_ORIGINS`: CORS allowed origins
- `HOST`: Server host address
- `PORT`: Server port number

## Development

### Adding New Features

1. Create new models in `backend/models.py`
2. Define schemas in `backend/schemas.py`
3. Create router files in `backend/routers/`
4. Register routers in `backend/main.py`

### Database Migrations

The application automatically creates database tables on startup. For production environments, consider using Alembic for database migrations.

## Security Features

- Input validation using Pydantic
- SQL injection prevention through SQLAlchemy ORM
- CORS configuration for cross-origin requests
- Environment-based configuration
- Proper error handling and logging

## Logging

The application includes comprehensive logging:
- Application startup/shutdown events
- CRUD operation tracking
- Error logging with stack traces
- Request/response logging

## Support

For issues, questions, or contributions, please refer to the project documentation or contact the development team.

## License

[Add your license information here]

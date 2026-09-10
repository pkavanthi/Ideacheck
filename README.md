# Movement Health Platform API

A comprehensive movement health platform where proper exercise form becomes as accessible as workout videos themselves. This API provides the backend infrastructure for exercise tracking, form assessment, and movement optimization.

## Product Vision

Create a comprehensive movement health platform where proper exercise form becomes as accessible as workout videos themselves, evolving into AR-integrated coaching with wearable sensor integration and community-driven movement optimization.

## Target Audience

- Home fitness enthusiasts
- Rehabilitation patients
- Virtual fitness instructors
- Physiotherapists
- Anyone seeking to improve exercise form and prevent injuries without expensive personal training or in-person sessions

## Core Features

- **User Management**: Create and manage user profiles
- **Exercise Library**: CRUD operations for exercises with categorization
- **Form Assessment**: Track and assess exercise form quality with scoring and feedback
- **Movement Tracking**: Monitor progress over time with detailed assessments

## Technology Stack

- **Framework**: FastAPI 0.104.1
- **Database**: SQLAlchemy 2.0.23 (SQLite for development, PostgreSQL/MySQL for production)
- **Authentication**: JWT with python-jose
- **Password Hashing**: Passlib with bcrypt
- **Validation**: Pydantic 2.5.0
- **Server**: Uvicorn

## Architecture

Modular Monolith architecture with clear separation of concerns:
- `backend/main.py` - Application entry point
- `backend/models.py` - Database models
- `backend/schemas.py` - Pydantic schemas for validation
- `backend/routers/` - API route handlers
- `backend/config.py` - Configuration management
- `backend/database.py` - Database connection
- `backend/utils/` - Utility functions (security, etc.)

## Prerequisites

- Python 3.9 or higher
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
Edit `.env` and update the configuration values, especially:
- `SECRET_KEY`: Use a strong random string for production
- `DATABASE_URL`: Configure your database connection

## Running the Application

### Development Mode

Run the application with auto-reload enabled:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive API docs (Swagger): http://localhost:8000/docs
- Alternative API docs (ReDoc): http://localhost:8000/redoc

### Production Mode

For production, run without the `--reload` flag:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Health Check
- `GET /` - Root endpoint
- `GET /health` - Health check endpoint

### Users
- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/` - Get all users (with pagination)
- `GET /api/v1/users/{user_id}` - Get a specific user
- `PUT /api/v1/users/{user_id}` - Update a user
- `DELETE /api/v1/users/{user_id}` - Delete a user

### Exercises
- `POST /api/v1/exercises/?user_id={user_id}` - Create a new exercise
- `GET /api/v1/exercises/` - Get all exercises (with filters)
- `GET /api/v1/exercises/{exercise_id}` - Get a specific exercise
- `PUT /api/v1/exercises/{exercise_id}` - Update an exercise
- `DELETE /api/v1/exercises/{exercise_id}` - Delete an exercise

### Form Assessments
- `POST /api/v1/exercises/{exercise_id}/assessments?user_id={user_id}` - Create form assessment
- `GET /api/v1/exercises/{exercise_id}/assessments` - Get all assessments for an exercise
- `GET /api/v1/exercises/assessments/{assessment_id}` - Get a specific assessment
- `PUT /api/v1/exercises/assessments/{assessment_id}` - Update an assessment
- `DELETE /api/v1/exercises/assessments/{assessment_id}` - Delete an assessment

## Database

The application uses SQLAlchemy ORM with support for multiple databases:

### SQLite (Default - Development)
No additional setup required. Database file will be created automatically.

### PostgreSQL (Production)
1. Install PostgreSQL
2. Create a database:
   ```sql
   CREATE DATABASE movement_health;
   ```
3. Update `DATABASE_URL` in `.env`:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/movement_health
   ```

### MySQL (Production)
1. Install MySQL
2. Create a database:
   ```sql
   CREATE DATABASE movement_health;
   ```
3. Update `DATABASE_URL` in `.env`:
   ```
   DATABASE_URL=mysql+pymysql://user:password@localhost:3306/movement_health
   ```

## Database Models

### User
- User authentication and profile management
- Fields: id, email, username, hashed_password, full_name, is_active, timestamps

### Exercise
- Exercise definitions and categorization
- Fields: id, user_id, name, description, category, difficulty_level, target_muscles, equipment_needed, timestamps

### FormAssessment
- Exercise form quality tracking
- Fields: id, user_id, exercise_id, assessment_date, form_score, feedback, key_points, video_url, notes, created_at

## Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication (ready for implementation)
- CORS middleware configured
- Input validation using Pydantic
- SQL injection prevention through ORM

## Development

### Project Structure
```
.
├── backend/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration
│   ├── database.py          # Database setup
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py         # User endpoints
│   │   └── exercises.py     # Exercise & assessment endpoints
│   └── utils/
│       ├── __init__.py
│       └── security.py      # Security utilities
├── .env.example             # Environment variables template
├── README.md                # This file
└── requirements.txt         # Python dependencies
```

### Adding New Features

1. Create new models in `backend/models.py`
2. Create corresponding schemas in `backend/schemas.py`
3. Create router in `backend/routers/`
4. Register router in `backend/main.py`

## Error Handling

The API returns standard HTTP status codes:
- `200 OK` - Successful GET/PUT requests
- `201 Created` - Successful POST requests
- `204 No Content` - Successful DELETE requests
- `400 Bad Request` - Invalid input
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server errors

## Logging

Application logs are configured with timestamps and log levels. Check console output for:
- Application startup/shutdown
- Database operations
- API requests
- Errors and warnings

## Future Enhancements

- AR-integrated coaching
- Wearable sensor integration
- Community-driven movement optimization
- Video analysis for form assessment
- Real-time feedback system
- Social features and community sharing

## License

Proprietary - All rights reserved

## Support

For issues and questions, please contact the development team.

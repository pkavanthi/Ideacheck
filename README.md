# Smart Fitness Studio API

A REST API for movement quality tracking and exercise form analysis, transforming every home into a smart fitness studio where professional coaching is accessible to everyone.

## Product Vision

To create a world where movement quality matches movement quantity, making exercise not just harder but smarter and safer through accessible professional coaching at home.

## Target Audience

- Home fitness enthusiasts
- Physical therapy patients
- Fitness professionals
- Anyone seeking to improve exercise form and prevent injuries during solo workouts

## Core Features

- **User Management**: Create and manage user profiles
- **Exercise Library**: CRUD operations for exercises with detailed form tips and categorization
- **Workout Tracking**: Plan, track, and complete workout sessions with exercise combinations

## Technology Stack

- **Backend Framework**: FastAPI (Python)
- **Database**: SQLAlchemy ORM with SQLite (development) / PostgreSQL (production)
- **Authentication**: JWT tokens with bcrypt password hashing
- **Architecture**: Modular Monolith with clear separation of concerns

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
cd /app/user_workspace/team_058/49e53f53-3a11-4cc6-8580-0895a5571676
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and update SECRET_KEY with a strong random string
```

## Running Locally

1. Activate the virtual environment (if not already activated):
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Start the development server:
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

3. Access the API:
- API Base URL: http://localhost:8000
- Interactive API Documentation (Swagger UI): http://localhost:8000/docs
- Alternative API Documentation (ReDoc): http://localhost:8000/redoc

## API Endpoints

### Health Check
- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint

### Users
- `POST /api/v1/users` - Create a new user
- `GET /api/v1/users` - Get all users (with pagination)
- `GET /api/v1/users/{user_id}` - Get a specific user
- `PUT /api/v1/users/{user_id}` - Update a user
- `DELETE /api/v1/users/{user_id}` - Delete a user

### Exercises
- `POST /api/v1/exercises` - Create a new exercise
- `GET /api/v1/exercises` - Get all exercises (with filtering by category/difficulty)
- `GET /api/v1/exercises/{exercise_id}` - Get a specific exercise
- `PUT /api/v1/exercises/{exercise_id}` - Update an exercise
- `DELETE /api/v1/exercises/{exercise_id}` - Delete an exercise

### Workouts
- `POST /api/v1/workouts` - Create a new workout
- `GET /api/v1/workouts` - Get all workouts (with filtering by status/user)
- `GET /api/v1/workouts/{workout_id}` - Get a specific workout
- `PUT /api/v1/workouts/{workout_id}` - Update a workout
- `DELETE /api/v1/workouts/{workout_id}` - Delete a workout
- `POST /api/v1/workouts/{workout_id}/exercises` - Add an exercise to a workout

## Database Schema

### Users
- User authentication and profile management
- Relationships: One-to-many with Workouts and Exercises

### Exercises
- Exercise library with form tips and categorization
- Fields: name, description, category, difficulty_level, target_muscles, equipment_needed, form_tips

### Workouts
- Workout session tracking
- Fields: title, description, duration, calories_burned, status, scheduled_date, completed_date
- Status options: planned, in_progress, completed

### WorkoutExercises
- Junction table linking workouts and exercises
- Additional fields: sets, reps, weight, duration, rest_seconds, form_score, order

## Configuration

Key configuration options in `.env`:

- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Secret key for JWT token generation (must be changed in production)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiration time
- `ALLOWED_ORIGINS`: CORS allowed origins

## Architecture Overview

The application follows a **Modular Monolith** architecture:

```
backend/
├── main.py              # Application entry point and FastAPI setup
├── config.py            # Configuration management
├── database.py          # Database connection and session management
├── models.py            # SQLAlchemy database models
├── auth.py              # Authentication utilities (password hashing, JWT)
└── routers/             # API route handlers
    ├── users.py         # User management endpoints
    ├── exercises.py     # Exercise CRUD endpoints
    └── workouts.py      # Workout management endpoints
```

## Security Features

- Password hashing using bcrypt
- JWT token-based authentication
- CORS configuration for cross-origin requests
- Input validation using Pydantic models
- SQL injection prevention through SQLAlchemy ORM

## Development

### Code Structure
- **Models**: Database models defined in `backend/models.py`
- **Routers**: API endpoints organized by resource in `backend/routers/`
- **Configuration**: Centralized in `backend/config.py` using Pydantic settings
- **Database**: Session management in `backend/database.py`

### Adding New Features
1. Define database models in `models.py`
2. Create Pydantic schemas in the relevant router file
3. Implement CRUD operations in router files
4. Update database schema (migrations recommended for production)

## Production Deployment

For production deployment:

1. Change `DATABASE_URL` to PostgreSQL connection string
2. Generate a strong `SECRET_KEY` (use `openssl rand -hex 32`)
3. Set `DEBUG=False`
4. Use a production ASGI server (uvicorn with workers or gunicorn)
5. Set up proper CORS origins
6. Implement database migrations using Alembic
7. Add monitoring and logging
8. Set up SSL/TLS certificates

## License

This project is part of a fitness technology initiative to make professional coaching accessible to everyone.

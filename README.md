# AI Fitness Coach API

Transform global fitness culture from quantity-focused to quality-focused training by making professional movement coaching universally accessible through AI technology.

## Product Vision

Professional movement coaching for home fitness enthusiasts, physical therapy patients, remote fitness professionals, and workplace wellness programs.

## Target Audience

- Home fitness enthusiasts aged 25-55
- Physical therapy patients requiring guided exercise
- Remote fitness professionals monitoring clients
- Workplace wellness programs focused on ergonomics

## Core Features

- User management with fitness profiles
- Exercise library with detailed instructions
- Workout planning and tracking
- CRUD operations for users, exercises, and workouts

## Technology Stack

- **Backend Framework**: FastAPI (Python)
- **Database**: SQLite (SQLAlchemy ORM)
- **Authentication**: JWT with bcrypt password hashing
- **Architecture**: Modular Monolith

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
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
# Edit .env and set your SECRET_KEY
```

## Running Locally

1. Activate virtual environment (if not already activated):
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Start the development server:
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

3. Access the API:
- API: http://localhost:8000
- Interactive API docs: http://localhost:8000/docs
- Alternative API docs: http://localhost:8000/redoc

## API Endpoints

### Users
- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/` - Get all users
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user (soft delete)

### Exercises
- `POST /api/v1/exercises/` - Create a new exercise
- `GET /api/v1/exercises/` - Get all exercises (with filters)
- `GET /api/v1/exercises/{exercise_id}` - Get exercise by ID
- `PUT /api/v1/exercises/{exercise_id}` - Update exercise
- `DELETE /api/v1/exercises/{exercise_id}` - Delete exercise (soft delete)

### Workouts
- `POST /api/v1/workouts/` - Create a new workout
- `GET /api/v1/workouts/` - Get all workouts (with filters)
- `GET /api/v1/workouts/{workout_id}` - Get workout by ID
- `PUT /api/v1/workouts/{workout_id}` - Update workout
- `DELETE /api/v1/workouts/{workout_id}` - Delete workout

## Environment Variables

Required environment variables (see `.env.example`):

- `SECRET_KEY` - Secret key for JWT token generation (REQUIRED)
- `DATABASE_URL` - Database connection string (default: SQLite)
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time (default: 30)
- `ALLOWED_ORIGINS` - CORS allowed origins

## Database Schema

### Users
- User profiles with fitness levels
- Password hashing with bcrypt
- Soft delete support

### Exercises
- Exercise library with categories
- Difficulty levels and muscle groups
- Equipment requirements
- Video instructions support

### Workouts
- User-specific workout plans
- Exercise associations with sets/reps
- Completion tracking
- Scheduled and completed dates

## Architecture

**Modular Monolith** with clear separation:
- `backend/main.py` - Application entry point
- `backend/config.py` - Configuration management
- `backend/database.py` - Database setup
- `backend/models.py` - SQLAlchemy models
- `backend/routers/` - API route handlers

## Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- Input validation with Pydantic
- SQL injection prevention via SQLAlchemy ORM
- CORS configuration
- Environment-based secrets management

## Development

The application uses:
- FastAPI for high-performance async API
- SQLAlchemy for database ORM
- Pydantic for data validation
- Passlib for secure password hashing

## Success Metrics

- User registration and profile management
- Exercise library creation and management
- Workout planning and tracking
- Quality-focused movement coaching accessibility

## License

[Your License Here]

## Support

For issues and questions, please open an issue in the repository.

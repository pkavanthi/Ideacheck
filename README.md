# EduTranslate - Educational Platform with Language Translation

Transform education into a borderless, inclusive experience where language becomes an asset rather than a barrier, enabling world-class instruction to reach every student regardless of linguistic background.

## Product Vision

EduTranslate is designed for international university students with varying language proficiencies, professors teaching diverse classrooms, and university administrators seeking to enhance global competitiveness and student success.

## Core Features

- **Course Management**: Create, read, update, and delete courses with multilingual support
- **Course Materials**: Manage educational materials (lectures, assignments, readings) for each course
- **Translation System**: Translate courses and materials into multiple languages to support diverse student populations

## Technology Stack

- **Backend Framework**: FastAPI (Python)
- **Database**: SQLAlchemy ORM with SQLite (easily switchable to PostgreSQL/MySQL)
- **API Style**: RESTful API
- **Architecture**: Modular Monolith with clear separation of concerns

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## Installation

1. **Clone or navigate to the project directory**

2. **Create a virtual environment**
```bash
python -m venv venv
```

3. **Activate the virtual environment**

On Linux/Mac:
```bash
source venv/bin/activate
```

On Windows:
```bash
venv\Scripts\activate
```

4. **Install dependencies**
```bash
pip install -r backend/requirements.txt
```

5. **Set up environment variables**
```bash
cp .env.example .env
```

Edit `.env` file and update the configuration values as needed, especially:
- `SECRET_KEY`: Use a strong random string for production
- `DATABASE_URL`: Update if using PostgreSQL or MySQL instead of SQLite

## Running the Application

1. **Initialize the database** (first time only)
```bash
python -c "from backend.database import init_db; init_db()"
```

2. **Start the development server**
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

3. **Access the API documentation**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Courses

- `POST /api/v1/courses` - Create a new course
- `GET /api/v1/courses` - List all courses (supports filtering by language)
- `GET /api/v1/courses/{course_id}` - Get a specific course
- `PUT /api/v1/courses/{course_id}` - Update a course
- `DELETE /api/v1/courses/{course_id}` - Delete a course

### Course Materials

- `POST /api/v1/courses/{course_id}/materials` - Create course material
- `GET /api/v1/courses/{course_id}/materials` - List materials for a course

### Translations

- `POST /api/v1/translations/courses/{course_id}` - Create course translation
- `GET /api/v1/translations/courses/{course_id}` - List all translations for a course
- `GET /api/v1/translations/courses/{course_id}/{language}` - Get specific translation
- `DELETE /api/v1/translations/courses/{course_id}/{language}` - Delete translation
- `POST /api/v1/translations/materials/{material_id}` - Create material translation
- `GET /api/v1/translations/materials/{material_id}` - List material translations

## Project Structure

```
.
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection and session management
│   ├── models.py            # SQLAlchemy database models
│   └── routers/             # API route handlers
│       ├── __init__.py
│       ├── courses.py       # Course and material endpoints
│       └── translations.py  # Translation endpoints
├── .env.example             # Environment variables template
├── README.md                # This file
└── requirements.txt         # Python dependencies
```

## Database Schema

### Tables

1. **courses**: Main course information
   - id, title, description, language, instructor_name, created_at, updated_at, is_active

2. **course_translations**: Translated course content
   - id, course_id, target_language, translated_title, translated_description, created_at

3. **course_materials**: Educational materials for courses
   - id, course_id, title, content, material_type, language, created_at, updated_at

4. **material_translations**: Translated material content
   - id, material_id, target_language, translated_title, translated_content, created_at

## Example Usage

### Create a Course
```bash
curl -X POST "http://localhost:8000/api/v1/courses" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Introduction to Computer Science",
    "description": "Learn the fundamentals of programming",
    "language": "en",
    "instructor_name": "Dr. Smith"
  }'
```

### Create a Translation
```bash
curl -X POST "http://localhost:8000/api/v1/translations/courses/1" \
  -H "Content-Type: application/json" \
  -d '{
    "target_language": "es",
    "translated_title": "Introducción a las Ciencias de la Computación",
    "translated_description": "Aprende los fundamentos de la programación"
  }'
```

## Development

### Code Quality
- Follow PEP 8 style guidelines
- Use type hints for better code clarity
- Add docstrings to functions and classes

### Adding New Features
1. Create new models in `backend/models.py` if needed
2. Add new routes in `backend/routers/`
3. Update this README with new endpoints

## Production Deployment

For production deployment:

1. **Use a production-grade database** (PostgreSQL recommended)
   - Update `DATABASE_URL` in `.env`

2. **Set strong security values**
   - Generate a strong `SECRET_KEY`
   - Set `DEBUG=False`

3. **Use a production ASGI server**
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

4. **Consider using Docker** for containerized deployment

5. **Set up proper CORS origins** for your frontend domain

## Target Audience

- **International Students**: Access course content in their preferred language
- **Professors**: Reach diverse classrooms with multilingual content
- **University Administrators**: Enhance global competitiveness and student success

## License

This project is part of an educational platform initiative.

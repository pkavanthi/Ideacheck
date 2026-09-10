# Universal Learning Platform

A universal learning platform where language is never a barrier to education, enabling every student worldwide to access quality instruction in their native language.

## Product Vision

To create a universal learning platform where language is never a barrier to education, enabling every student worldwide to access quality instruction in their native language and fostering truly inclusive, equitable educational environments.

## Target Audience

- **International university students** with varying language proficiencies
- **Professors** teaching diverse classrooms
- **Educational administrators** seeking to improve institutional accessibility and reduce dropout rates among non-native speakers

## Core Features

- **Student Management**: Create, read, update, and delete student profiles with language preferences
- **Course Management**: Manage courses with multilingual support
- **Content Translation**: Translate course content into multiple languages
- **Enrollment System**: Enroll students in courses and track their progress

## Technology Stack

- **Backend Framework**: FastAPI (Python)
- **Database**: SQLite (easily upgradeable to PostgreSQL)
- **ORM**: SQLAlchemy
- **Data Validation**: Pydantic
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
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
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

1. **Start the development server**:
   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the application**:
   - API: http://localhost:8000
   - Interactive API Documentation (Swagger UI): http://localhost:8000/docs
   - Alternative API Documentation (ReDoc): http://localhost:8000/redoc

## API Endpoints

### Students
- `POST /api/v1/students/` - Create a new student
- `GET /api/v1/students/` - Get all students
- `GET /api/v1/students/{student_id}` - Get a specific student
- `PUT /api/v1/students/{student_id}` - Update a student
- `DELETE /api/v1/students/{student_id}` - Delete a student

### Courses
- `POST /api/v1/courses/` - Create a new course
- `GET /api/v1/courses/` - Get all courses
- `GET /api/v1/courses/{course_id}` - Get a specific course
- `PUT /api/v1/courses/{course_id}` - Update a course
- `DELETE /api/v1/courses/{course_id}` - Delete a course
- `POST /api/v1/courses/{course_id}/enroll` - Enroll a student in a course
- `POST /api/v1/courses/{course_id}/content` - Create course content
- `GET /api/v1/courses/{course_id}/content` - Get all content for a course

### Translations
- `POST /api/v1/translations/translate` - Translate text (placeholder implementation)
- `POST /api/v1/translations/content` - Create a content translation
- `GET /api/v1/translations/content/{content_id}` - Get all translations for content
- `GET /api/v1/translations/content/{content_id}/language/{language}` - Get translation by language
- `DELETE /api/v1/translations/content/{translation_id}` - Delete a translation

## Project Structure

```
.
├── backend/
│   ├── __init__.py
│   ├── main.py              # Main application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection and session
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic schemas for validation
│   ├── requirements.txt     # Python dependencies
│   └── routers/             # API route handlers
│       ├── __init__.py
│       ├── students.py      # Student endpoints
│       ├── courses.py       # Course endpoints
│       └── translations.py  # Translation endpoints
├── .env.example             # Example environment variables
└── README.md                # This file
```

## Database Models

### Student
- Email, full name, native language, preferred language
- Relationships: enrollments

### Course
- Title, description, original language, instructor name
- Relationships: enrollments, content items

### Enrollment
- Links students to courses
- Tracks enrollment date

### CourseContent
- Course materials (text, video, audio)
- Relationships: translations

### ContentTranslation
- Translated versions of course content
- Supports multiple languages per content item

## Development

### Adding New Features

1. Create new models in `backend/models.py`
2. Create corresponding schemas in `backend/schemas.py`
3. Create router in `backend/routers/`
4. Register router in `backend/main.py`

### Database Migrations

The application automatically creates tables on startup. For production, consider using Alembic for proper database migrations.

## Security Considerations

- Change `SECRET_KEY` in `.env` to a strong random string in production
- Use PostgreSQL or MySQL instead of SQLite for production
- Implement proper authentication and authorization
- Enable HTTPS in production
- Configure CORS appropriately for your frontend domain
- Implement rate limiting for API endpoints

## Future Enhancements

- Integration with translation APIs (Google Translate, DeepL)
- Real-time translation during lectures
- Video/audio content translation
- User authentication and authorization
- Progress tracking and analytics
- Mobile application
- Advanced search and filtering
- Notification system

## License

This project is part of an educational initiative to make learning accessible to all students regardless of language barriers.

## Support

For questions or issues, please contact the development team or create an issue in the project repository.

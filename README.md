# EduTranslate API

Transform global education by making language proficiency irrelevant to academic success, creating a world where every student can access world-class education in their native language and knowledge transcends linguistic boundaries.

## Product Vision

EduTranslate enables international university students with varying English proficiency levels to access educational content in their native language. The platform supports professors teaching diverse classrooms, helps university administrators improve global competitiveness, and provides accessibility support for students with hearing impairments.

## Target Audience

- **International University Students**: Students with varying English proficiency levels who need educational content in their native language
- **Professors**: Educators teaching diverse classrooms who want to make their content accessible to all students
- **University Administrators**: Leaders seeking to improve their institution's global competitiveness and inclusivity
- **Students with Hearing Impairments**: Students requiring accessibility support for educational content

## Core Features

- **Content Management**: Create, read, update, and delete educational content (lectures, assignments, readings, exams)
- **Multi-language Support**: Support for 10+ languages including English, Spanish, French, German, Chinese, Japanese, Korean, Arabic, Hindi, and Portuguese
- **Translation Management**: Create and manage translations for educational content in multiple languages
- **Content Types**: Support for various educational content types (lectures, assignments, readings, exams, and more)

## Technology Stack

- **Backend Framework**: FastAPI 0.104.1
- **Database**: SQLAlchemy 2.0.23 with SQLite (development) / PostgreSQL (production)
- **Data Validation**: Pydantic 2.5.0
- **Server**: Uvicorn 0.24.0
- **Architecture**: Modular Monolith with clear separation of concerns

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
Edit `.env` file and update the configuration values as needed.

## Running the Application

### Development Mode

1. **Start the FastAPI server**:
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

2. **Access the application**:
- API: http://localhost:8000
- Interactive API Documentation (Swagger UI): http://localhost:8000/docs
- Alternative API Documentation (ReDoc): http://localhost:8000/redoc

### Production Mode

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Health Check
- `GET /` - Root endpoint
- `GET /health` - Health check endpoint

### Content Management
- `POST /api/v1/content/` - Create new educational content
- `GET /api/v1/content/` - List all contents (with optional filtering)
- `GET /api/v1/content/{content_id}` - Get specific content with translations
- `PUT /api/v1/content/{content_id}` - Update content
- `DELETE /api/v1/content/{content_id}` - Delete content

### Translation Management
- `POST /api/v1/translations/` - Create new translation
- `GET /api/v1/translations/content/{content_id}` - List translations for specific content
- `GET /api/v1/translations/{translation_id}` - Get specific translation
- `PUT /api/v1/translations/{translation_id}` - Update translation
- `DELETE /api/v1/translations/{translation_id}` - Delete translation

## Project Structure

```
.
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection and session
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic schemas for validation
│   ├── requirements.txt     # Python dependencies
│   └── routers/
│       ├── __init__.py
│       ├── content.py       # Content management endpoints
│       └── translations.py  # Translation management endpoints
├── .env.example             # Example environment variables
└── README.md               # This file
```

## Database Models

### Content
- Educational content with support for multiple content types
- Fields: id, title, description, content_type, original_language, original_text, created_by, timestamps

### Translation
- Translations of educational content in different languages
- Fields: id, content_id, target_language, translated_text, translated_title, timestamps

## Supported Languages

- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Chinese (zh)
- Japanese (ja)
- Korean (ko)
- Arabic (ar)
- Hindi (hi)
- Portuguese (pt)

## Supported Content Types

- Lecture
- Assignment
- Reading
- Exam
- Other

## Environment Variables

See `.env.example` for all available configuration options:

- `DATABASE_URL`: Database connection string
- `ALLOWED_ORIGINS`: CORS allowed origins
- `SECRET_KEY`: Secret key for security features
- `DEBUG`: Enable/disable debug mode

## Development

### Database Migrations

The application automatically creates database tables on startup. For production environments, consider using Alembic for database migrations.

### Adding New Features

1. Define models in `backend/models.py`
2. Create Pydantic schemas in `backend/schemas.py`
3. Implement API routes in `backend/routers/`
4. Update `backend/main.py` to include new routers

## Security Best Practices

- Never commit `.env` file with real credentials
- Use strong SECRET_KEY in production
- Enable HTTPS in production
- Implement rate limiting for production
- Use PostgreSQL or MySQL for production (not SQLite)
- Implement proper authentication and authorization

## Future Enhancements

- Integration with translation APIs (Google Translate, DeepL)
- Real-time translation capabilities
- Audio transcription and translation
- User authentication and authorization
- Role-based access control
- Content versioning
- Analytics and usage tracking

## License

Proprietary - All rights reserved

## Support

For questions or issues, please contact the development team.

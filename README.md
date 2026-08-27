# Educational Translation Platform

Transform global education into a truly borderless experience where every student can learn in their native language while maintaining technical accuracy, making knowledge universally accessible regardless of linguistic origin.

## Product Vision

This platform enables international university students with diverse language backgrounds to access educational content in their native languages. It supports professors teaching multilingual classrooms and helps university administrators improve educational accessibility and institutional reputation.

## Target Audience

- **International university students** with diverse language backgrounds
- **Professors** teaching multilingual classrooms
- **University administrators** seeking to improve educational accessibility

## Core Features

- **CRUD Operations for Translations**: Create, read, update, and delete translation entries
- **Multi-language Support**: Handle translations between various language pairs
- **RESTful API**: Clean API endpoints for integration with educational platforms

## Technology Stack

- **Backend Framework**: FastAPI (Python)
- **Database**: SQLite (easily upgradeable to PostgreSQL)
- **ORM**: SQLAlchemy
- **Data Validation**: Pydantic
- **Architecture**: Modular Monolith

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
Edit `.env` file with your configuration values.

## Running the Application

### Development Mode

Run the FastAPI application with auto-reload:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive API Documentation (Swagger)**: http://localhost:8000/docs
- **Alternative API Documentation (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

### Health Check
- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint

### Translations
- `POST /api/v1/translations/` - Create a new translation
- `GET /api/v1/translations/` - Get all translations (with pagination)
- `GET /api/v1/translations/{translation_id}` - Get a specific translation
- `PUT /api/v1/translations/{translation_id}` - Update a translation
- `DELETE /api/v1/translations/{translation_id}` - Delete a translation

### Example API Usage

**Create a translation**:
```bash
curl -X POST "http://localhost:8000/api/v1/translations/" \
  -H "Content-Type: application/json" \
  -d '{
    "source_text": "Hello, world!",
    "source_language": "en",
    "target_language": "es"
  }'
```

**Get all translations**:
```bash
curl -X GET "http://localhost:8000/api/v1/translations/"
```

**Get a specific translation**:
```bash
curl -X GET "http://localhost:8000/api/v1/translations/1"
```

**Update a translation**:
```bash
curl -X PUT "http://localhost:8000/api/v1/translations/1" \
  -H "Content-Type: application/json" \
  -d '{
    "translated_text": "¡Hola, mundo!"
  }'
```

**Delete a translation**:
```bash
curl -X DELETE "http://localhost:8000/api/v1/translations/1"
```

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
│       └── translations.py  # Translation API endpoints
├── .env.example             # Environment variables template
└── README.md                # This file
```

## Architecture Overview

This application follows a **Modular Monolith** architecture with clear separation of concerns:

- **Routers**: Handle HTTP requests and responses
- **Models**: Define database schema using SQLAlchemy ORM
- **Schemas**: Validate request/response data using Pydantic
- **Database**: Manage database connections and sessions
- **Config**: Centralize configuration management

## Environment Variables

Key environment variables (see `.env.example` for full list):

- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Secret key for security features
- `CORS_ORIGINS`: Allowed CORS origins
- `DEBUG`: Enable/disable debug mode

## Database

The application uses SQLite by default for easy setup. The database file (`translations.db`) will be created automatically on first run.

To use PostgreSQL in production, update the `DATABASE_URL` in your `.env` file:
```
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## Security Features

- **Input Validation**: All inputs validated using Pydantic schemas
- **CORS Configuration**: Configurable CORS origins
- **Error Handling**: Comprehensive error handling with appropriate HTTP status codes
- **Logging**: Application-wide logging for monitoring and debugging

## Future Enhancements

- Integration with translation APIs (Google Translate, DeepL, etc.)
- User authentication and authorization
- Translation history and versioning
- Batch translation support
- Real-time translation updates via WebSockets
- Advanced search and filtering capabilities
- Analytics and usage metrics

## Contributing

This is an MVP (Minimum Viable Product) focused on core CRUD operations. Contributions are welcome to enhance functionality and add new features.

## License

[Specify your license here]

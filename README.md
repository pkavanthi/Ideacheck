# Rural Healthcare Platform

AI-augmented healthcare delivery platform for rural areas, transforming healthcare access through technology innovation combined with human expertise.

## Product Vision

To become the leading healthcare delivery platform for rural areas globally, transforming healthcare access through AI-augmented care that combines technology innovation with human expertise.

## Target Audience

- **Rural Patients**: Seeking medical care in underserved areas
- **Community Health Workers**: Providing frontline healthcare services
- **Specialist Doctors**: Offering remote consultations to rural communities

## Core Features

- Patient management with comprehensive medical history tracking
- Health worker registration and management
- Consultation scheduling and management
- CRUD operations for all core entities

## Technology Stack

- **Backend Framework**: FastAPI 0.104.1
- **Database**: SQLite (SQLAlchemy ORM)
- **Data Validation**: Pydantic 2.5.0
- **Server**: Uvicorn
- **Architecture**: Modular Monolith

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## Installation

1. Clone the repository or navigate to the project directory

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - On Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

5. Set up environment variables:
```bash
cp .env.example .env
```

6. Edit `.env` file and update the `SECRET_KEY` with a secure random string:
```bash
# Generate a secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Running the Application

1. Start the FastAPI server:
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

2. Access the application:
   - API: http://localhost:8000
   - Interactive API Documentation (Swagger): http://localhost:8000/docs
   - Alternative API Documentation (ReDoc): http://localhost:8000/redoc

## API Endpoints

### Health Check
- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint

### Patients
- `POST /api/v1/patients` - Create a new patient
- `GET /api/v1/patients` - Get all patients (with pagination)
- `GET /api/v1/patients/{patient_id}` - Get a specific patient
- `PUT /api/v1/patients/{patient_id}` - Update a patient
- `DELETE /api/v1/patients/{patient_id}` - Delete a patient

### Health Workers
- `POST /api/v1/health-workers` - Create a new health worker
- `GET /api/v1/health-workers` - Get all health workers (with pagination)
- `GET /api/v1/health-workers/{worker_id}` - Get a specific health worker
- `PUT /api/v1/health-workers/{worker_id}` - Update a health worker
- `DELETE /api/v1/health-workers/{worker_id}` - Delete a health worker

### Consultations
- `POST /api/v1/consultations` - Create a new consultation
- `GET /api/v1/consultations` - Get all consultations (with pagination)
- `GET /api/v1/consultations/{consultation_id}` - Get a specific consultation
- `PUT /api/v1/consultations/{consultation_id}` - Update a consultation
- `DELETE /api/v1/consultations/{consultation_id}` - Delete a consultation
- `GET /api/v1/consultations/patient/{patient_id}` - Get all consultations for a patient
- `GET /api/v1/consultations/health-worker/{worker_id}` - Get all consultations for a health worker

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
│   └── routers/             # API route handlers
│       ├── __init__.py
│       ├── patients.py      # Patient endpoints
│       ├── health_workers.py # Health worker endpoints
│       └── consultations.py  # Consultation endpoints
├── .env.example             # Environment variables template
├── README.md                # This file
└── requirements.txt         # Python dependencies

```

## Database

The application uses SQLite by default for simplicity. The database file (`healthcare.db`) will be created automatically in the project root when you first run the application.

### Database Models

- **Patient**: Stores patient information and medical history
- **HealthWorker**: Stores health worker credentials and location
- **Consultation**: Manages consultation scheduling and records

## Development

### Code Quality

The codebase follows:
- PEP 8 style guidelines
- Type hints for better code clarity
- Comprehensive error handling
- Input validation using Pydantic
- RESTful API design principles

### Security Features

- Environment-based configuration (no hardcoded secrets)
- CORS middleware for cross-origin requests
- Input validation and sanitization
- SQL injection prevention through ORM
- Proper HTTP status codes and error messages

## Architecture

The application follows a **Modular Monolith** architecture with clear separation of concerns:

- **Routers**: Handle HTTP requests and responses
- **Models**: Define database schema and relationships
- **Schemas**: Validate input/output data
- **Database**: Manage database connections and sessions
- **Config**: Centralize configuration management

## Future Enhancements

- Authentication and authorization (JWT tokens)
- AI-powered symptom analysis
- Real-time video consultations
- Mobile application support
- Advanced analytics and reporting
- Multi-language support
- SMS/WhatsApp notifications

## License

Proprietary - All rights reserved

## Support

For support and questions, please contact the development team.

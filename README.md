# Rural Healthcare API

An AI-powered telemedicine platform designed to eliminate geographic barriers in rural healthcare, ensuring every rural patient receives quality medical care comparable to urban hospitals.

## Product Vision

To create an interconnected rural healthcare ecosystem where AI and telemedicine eliminate geographic barriers, ensuring every rural patient receives quality medical care comparable to urban hospitals regardless of location.

## Target Audience

- **Rural Health Workers**: Frontline care providers in remote areas
- **Rural Patients**: Individuals in remote villages lacking specialist access
- **Remote Doctors**: Medical professionals offering telemedicine consultations to underserved communities

## Core Features

- **Patient Management**: Complete CRUD operations for patient records
- **Medical History Tracking**: Comprehensive patient medical history, allergies, and current medications
- **Emergency Contact Management**: Store and manage emergency contact information
- **Village/District Tracking**: Geographic organization for rural healthcare delivery

## Technology Stack

- **Backend Framework**: FastAPI (Python)
- **Database**: SQLAlchemy ORM with SQLite (development) / PostgreSQL (production)
- **Data Validation**: Pydantic
- **Architecture**: Modular Monolith with clear separation of concerns

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
   Edit `.env` file with your configuration if needed.

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

### Production Mode

For production deployment:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Health Check
- `GET /` - Root health check
- `GET /health` - Detailed health status

### Patient Management
- `POST /api/v1/patients` - Create a new patient
- `GET /api/v1/patients` - List all patients (with pagination)
- `GET /api/v1/patients/{patient_id}` - Get specific patient details
- `PUT /api/v1/patients/{patient_id}` - Update patient information
- `DELETE /api/v1/patients/{patient_id}` - Soft delete patient (deactivate)

### Query Parameters
- `skip`: Number of records to skip (pagination)
- `limit`: Maximum number of records to return (default: 100)
- `active_only`: Filter for active patients only (default: true)

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
│   └── routers/
│       ├── __init__.py
│       └── patients.py      # Patient CRUD endpoints
├── .env.example             # Environment variables template
├── README.md                # This file
└── requirements.txt         # Python dependencies
```

## Database Schema

### Patient Model
- **id**: Primary key
- **first_name**: Patient's first name
- **last_name**: Patient's last name
- **date_of_birth**: Date of birth
- **gender**: Gender
- **phone_number**: Contact phone number
- **email**: Email address (optional)
- **address**: Physical address
- **village**: Village name
- **district**: District name
- **medical_history**: Medical history notes
- **allergies**: Known allergies
- **current_medications**: Current medications
- **emergency_contact_name**: Emergency contact person
- **emergency_contact_phone**: Emergency contact phone
- **is_active**: Active status (soft delete flag)
- **created_at**: Record creation timestamp
- **updated_at**: Last update timestamp

## Configuration

Key configuration options in `.env`:

- `DATABASE_URL`: Database connection string
- `ALLOWED_ORIGINS`: CORS allowed origins
- `DEBUG`: Debug mode (true/false)
- `APP_NAME`: Application name
- `APP_VERSION`: Application version

## Development

### Adding New Features

1. Create new models in `backend/models.py`
2. Create corresponding schemas in `backend/schemas.py`
3. Create router files in `backend/routers/`
4. Register routers in `backend/main.py`

### Database Migrations

For production use, consider implementing Alembic for database migrations:

```bash
pip install alembic
alembic init alembic
```

## Security Considerations

- Input validation using Pydantic schemas
- SQL injection prevention through SQLAlchemy ORM
- CORS configuration for API security
- Environment variables for sensitive configuration
- Soft delete for data retention

## Error Handling

The API implements comprehensive error handling:
- 404: Resource not found
- 500: Internal server error
- Detailed error messages in responses
- Logging for debugging and monitoring

## Future Enhancements

- Authentication and authorization (JWT)
- Telemedicine consultation scheduling
- AI-powered diagnosis assistance
- Medical image storage and analysis
- Real-time chat for consultations
- Mobile application integration
- Multi-language support

## Support

For issues, questions, or contributions, please refer to the project documentation or contact the development team.

## License

[Specify your license here]

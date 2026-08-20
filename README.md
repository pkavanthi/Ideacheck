# Rural Healthcare Diagnostic Hub

Transform every rural health center into a connected diagnostic hub where geography no longer determines access to quality medical care, creating a comprehensive healthcare network that ensures no patient is left behind.

## Product Vision

This application enables rural health workers and remote physician specialists to provide quality medical care to patients in underserved communities. It creates a connected network of healthcare facilities that bridges the gap between rural areas and specialized medical expertise.

## Target Audience

- Rural health workers
- Remote physician specialists
- Patients in underserved communities
- Government health departments
- Healthcare technology partners in developing regions

## Core Features

- **Health Center Management**: Complete CRUD operations for managing rural health centers
- **Diagnostic Records**: Track and manage patient diagnostic information
- **Connected Network**: Link health centers with specialists for remote consultations

## Technology Stack

- **Backend Framework**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **API Architecture**: RESTful API with modular monolith design
- **Configuration**: Pydantic Settings with environment variables

## Prerequisites

- Python 3.9 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory

2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

4. **Set up environment variables**:
```bash
cp .env.example .env
```

Edit `.env` file with your configuration:
- Set `DATABASE_URL` to your PostgreSQL connection string
- Generate secure values for `SECRET_KEY` and `JWT_SECRET_KEY`
- Configure `ALLOWED_ORIGINS` for CORS

5. **Initialize the database**:
```bash
# Create the database in PostgreSQL
createdb healthcare_db

# Run the application to create tables
python -m backend.main
```

## Running the Application

### Development Mode

```bash
cd backend
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### Production Mode

```bash
cd backend
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once the application is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health Centers

- `POST /api/v1/health-centers/` - Create a new health center
- `GET /api/v1/health-centers/` - List all health centers
- `GET /api/v1/health-centers/{id}` - Get a specific health center
- `PUT /api/v1/health-centers/{id}` - Update a health center
- `DELETE /api/v1/health-centers/{id}` - Delete a health center

### Diagnostics

- `POST /api/v1/diagnostics/` - Create a new diagnostic record
- `GET /api/v1/diagnostics/` - List all diagnostic records
- `GET /api/v1/diagnostics/{id}` - Get a specific diagnostic record
- `PUT /api/v1/diagnostics/{id}` - Update a diagnostic record
- `DELETE /api/v1/diagnostics/{id}` - Delete a diagnostic record

### System

- `GET /` - API information
- `GET /health` - Health check endpoint

## Project Structure

```
.
├── backend/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection and session
│   ├── models.py            # SQLAlchemy models
│   ├── requirements.txt     # Python dependencies
│   └── routers/
│       ├── __init__.py
│       ├── health_centers.py  # Health center endpoints
│       └── diagnostics.py     # Diagnostic endpoints
├── .env.example             # Environment variables template
└── README.md               # This file
```

## Architecture

This application follows a **Modular Monolith** architecture with clear separation of concerns:

- **Routers**: Handle HTTP requests and responses
- **Models**: Define database schema using SQLAlchemy
- **Database**: Manage database connections and sessions
- **Config**: Centralized configuration management

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `SECRET_KEY` | Application secret key | Yes |
| `JWT_SECRET_KEY` | JWT token secret key | Yes |
| `JWT_ALGORITHM` | JWT algorithm (default: HS256) | No |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | No |
| `ALLOWED_ORIGINS` | CORS allowed origins | No |
| `DEBUG` | Enable debug mode | No |

## Security Features

- Environment-based configuration (no hardcoded secrets)
- CORS middleware for cross-origin requests
- Input validation using Pydantic models
- SQL injection prevention through SQLAlchemy ORM
- Prepared for JWT authentication implementation

## Development Guidelines

- Follow PEP 8 style guide for Python code
- Use type hints for better code clarity
- Add logging for important operations
- Validate all user inputs
- Handle errors gracefully with appropriate HTTP status codes

## Contributing

When contributing to this project:

1. Ensure all new endpoints include proper error handling
2. Add logging for debugging purposes
3. Update this README if adding new features
4. Follow the existing code structure and patterns

## License

[Specify your license here]

## Support

For issues, questions, or contributions, please contact the development team or open an issue in the project repository.

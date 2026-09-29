import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database import Base, get_db
from backend.main import app

# In-memory SQLite for isolated tests
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_crud_incident(client):
    # 1. CREATE Incident
    payload = {
        "title": "Severe Waterlogging at Wayanad Pass",
        "district": "Wayanad",
        "location_name": "Vythiri Ghat Road",
        "latitude": 11.5534,
        "longitude": 76.0407,
        "threat_level": "CRITICAL",
        "status": "ACTIVE",
        "description": "Landslide warning and intense flash flood",
        "affected_population": 850
    }
    res = client.post("/api/v1/incidents/", json=payload)
    assert res.status_code == 201
    created = res.json()
    assert created["id"] is not None
    assert created["district"] == "Wayanad"
    incident_id = created["id"]

    # 2. READ All & Filter
    res = client.get("/api/v1/incidents/?district=Wayanad")
    assert res.status_code == 200
    assert len(res.json()) >= 1

    # 3. READ By ID
    res = client.get(f"/api/v1/incidents/{incident_id}")
    assert res.status_code == 200
    assert res.json()["title"] == "Severe Waterlogging at Wayanad Pass"

    # 4. UPDATE
    update_payload = {"status": "CONTAINED", "affected_population": 600}
    res = client.put(f"/api/v1/incidents/{incident_id}", json=update_payload)
    assert res.status_code == 200
    assert res.json()["status"] == "CONTAINED"
    assert res.json()["affected_population"] == 600

    # 5. DELETE
    res = client.delete(f"/api/v1/incidents/{incident_id}")
    assert res.status_code == 204

    # Verify 404
    res = client.get(f"/api/v1/incidents/{incident_id}")
    assert res.status_code == 404

def test_crud_resource(client):
    # 1. CREATE Resource
    payload = {
        "name": "NDRF Inflatable Rafts",
        "resource_type": "RESCUE_BOAT",
        "district": "Alappuzha",
        "quantity": 15,
        "available_quantity": 12,
        "location_hub": "Kuttanad Emergency Base",
        "status": "AVAILABLE"
    }
    res = client.post("/api/v1/resources/", json=payload)
    assert res.status_code == 201
    resource_id = res.json()["id"]

    # 2. READ All
    res = client.get("/api/v1/resources/?district=Alappuzha")
    assert res.status_code == 200
    assert len(res.json()) == 1

    # 3. UPDATE
    res = client.put(f"/api/v1/resources/{resource_id}", json={"available_quantity": 8})
    assert res.status_code == 200
    assert res.json()["available_quantity"] == 8

    # 4. DELETE
    res = client.delete(f"/api/v1/resources/{resource_id}")
    assert res.status_code == 204

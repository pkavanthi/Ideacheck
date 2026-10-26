import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.database import Base, get_db
from backend.main import app

# In-memory SQLite with StaticPool for isolated in-memory test database
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    return TestClient(app)


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_frontend_serving(client):
    # Test index.html served at root
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "DisasterOps" in response.text
    assert "tacticalMap" in response.text

    # Test static assets
    resp_css = client.get("/static/styles.css")
    assert resp_css.status_code == 200
    assert "dark-theme" in resp_css.text

    resp_js = client.get("/static/app.js")
    assert resp_js.status_code == 200
    assert "DisasterOpsApp" in resp_js.text


def test_incidents_crud(client):
    # 1. Create incident
    payload = {
        "title": "Severe Flood in Zone 4",
        "description": "Embankment breach at river basin",
        "location": "Cuttack, Ward 12",
        "latitude": 20.4625,
        "longitude": 85.8830,
        "severity": "critical",
        "affected_population": 5000,
        "reported_by": "NDRF Station 4",
    }
    create_resp = client.post("/api/v1/incidents/", json=payload)
    assert create_resp.status_code == 201
    inc_data = create_resp.json()
    assert inc_data["id"] is not None
    assert inc_data["title"] == payload["title"]
    assert inc_data["severity"] == "critical"
    assert inc_data["status"] == "reported"
    incident_id = inc_data["id"]

    # 2. List incidents
    list_resp = client.get("/api/v1/incidents/")
    assert list_resp.status_code == 200
    incidents = list_resp.json()
    assert len(incidents) == 1

    # 3. Filter by severity
    filter_resp = client.get("/api/v1/incidents/?severity=critical")
    assert filter_resp.status_code == 200
    assert len(filter_resp.json()) == 1

    filter_empty = client.get("/api/v1/incidents/?severity=low")
    assert filter_empty.status_code == 200
    assert len(filter_empty.json()) == 0

    # 4. Get by ID
    get_resp = client.get(f"/api/v1/incidents/{incident_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == incident_id

    # 5. Patch status & severity
    patch_resp = client.patch(
        f"/api/v1/incidents/{incident_id}",
        json={"status": "active", "severity": "high"},
    )
    assert patch_resp.status_code == 200
    assert patch_resp.json()["status"] == "active"
    assert patch_resp.json()["severity"] == "high"

    # 6. Delete
    del_resp = client.delete(f"/api/v1/incidents/{incident_id}")
    assert del_resp.status_code == 204

    # Confirm 404 after deletion
    get_del = client.get(f"/api/v1/incidents/{incident_id}")
    assert get_del.status_code == 404


def test_resources_crud(client):
    # 1. Create resource
    payload = {
        "name": "NDRF Quick Response Boat Unit",
        "type": "rescue_team",
        "quantity": 10,
        "unit": "boats",
        "location": "Bhubaneswar Central Hub",
        "status": "available",
        "contact_info": "Cmdt. Sharma (VHF Ch 16)",
        "notes": "Equipped with 25HP outboard motors",
    }
    create_resp = client.post("/api/v1/resources/", json=payload)
    assert create_resp.status_code == 201
    res_data = create_resp.json()
    assert res_data["id"] is not None
    assert res_data["name"] == payload["name"]
    assert res_data["status"] == "available"
    resource_id = res_data["id"]

    # 2. List resources
    list_resp = client.get("/api/v1/resources/")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

    # 3. Filter by type & status
    type_resp = client.get("/api/v1/resources/?type=rescue_team")
    assert type_resp.status_code == 200
    assert len(type_resp.json()) == 1

    # 4. Patch status (Deploy resource)
    patch_resp = client.patch(
        f"/api/v1/resources/{resource_id}",
        json={"status": "deployed"},
    )
    assert patch_resp.status_code == 200
    assert patch_resp.json()["status"] == "deployed"

    # 5. Delete resource
    del_resp = client.delete(f"/api/v1/resources/{resource_id}")
    assert del_resp.status_code == 204

    # Confirm 404
    get_del = client.get(f"/api/v1/resources/{resource_id}")
    assert get_del.status_code == 404

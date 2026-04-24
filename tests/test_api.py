import pytest
from fastapi.testclient import TestClient
from api.index import app, MASTER_API_KEY

client = TestClient(app)

def test_health_check():
    """Verifica que el endpoint de salud sea público y funcione."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_protected_route_without_key():
    """Verifica que las rutas protegidas fallen sin la API Key."""
    response = client.get("/api/config")
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized: Invalid API Key"

def test_protected_route_with_wrong_key():
    """Verifica que las rutas protegidas fallen con una API Key incorrecta."""
    response = client.get("/api/config", headers={"X-API-KEY": "WRONG_KEY"})
    assert response.status_code == 401

def test_protected_route_with_correct_key():
    """Verifica que las rutas protegidas funcionen con la API Key correcta."""
    # Nota: Esto fallará si la DB no está inicializada, pero el status no debería ser 401
    response = client.get("/api/config", headers={"X-API-KEY": MASTER_API_KEY})
    assert response.status_code != 401

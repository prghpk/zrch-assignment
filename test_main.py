import pytest
from fastapi.testclient import TestClient

from main import app  # Replace with your actual FastAPI app file

# Test client instance
client = TestClient(app)

# Test data for creating a car
test_car_data = {
    "brand": "Toyota",
    "model": "Camry",
    "year": 2020,
    "color": "Silver",
    "mileage": 30000,
    "status": "active",
}

# Test data for creating a broker
test_broker_data = {
    "name": "John Doe",
    "branches": "Main Branch",
    "mobile": "+123456789",
    "email": "john.doe@example.com",
}

def test_create_car():
    response = client.post("/cars/", json=test_car_data)
    assert response.status_code == 201
    assert "car_id" in response.json()
    
    # Cleanup: Delete the created cars
    car_id = response.json()["car_id"]
    client.delete(f"/cars/{car_id}")

def test_create_multiple_cars():
    cars_data = [
        {"brand": "Toyota", "model": "Camry", "year": 2020, "color": "Silver", "mileage": 30000, "status": "active"},
        {"brand": "Nissan", "model": "Altima", "year": 2021, "color": "White", "mileage": 16000, "status": "inactive"},
        # Add more cars as needed
    ]

    response = client.post("/cars/", json=cars_data)
    assert response.status_code == 201
    assert "car_ids" in response.json()
    
    # Cleanup: Delete the created cars
    car_ids = response.json()["car_ids"]
    for car_id in car_ids:
        client.delete(f"/cars/{car_id}")

def test_read_car():
    # Create a car for testing
    create_response = client.post("/cars/", json=test_car_data)
    assert create_response.status_code == 201

    car_id = create_response.json()["car_id"]
    read_response = client.get(f"/cars/{car_id}")
    assert read_response.status_code == 200
    assert read_response.json()["brand"] == test_car_data["brand"]
    
    # Cleanup: Delete the created cars
    client.delete(f"/cars/{car_id}")

def test_update_car():
    # Create a car for testing
    create_response = client.post("/cars/", json=test_car_data)
    assert create_response.status_code == 201

    car_id = create_response.json()["car_id"]
    update_data = {"brand": "Honda"}
    update_response = client.put(f"/cars/{car_id}", json=update_data)
    assert update_response.status_code == 200
    assert update_response.json()["message"] == "Car updated successfully"
    
    # Cleanup: Delete the created cars
    client.delete(f"/cars/{car_id}")

def test_delete_car():
    # Create a car for testing
    create_response = client.post("/cars/", json=test_car_data)
    assert create_response.status_code == 201

    car_id = create_response.json()["car_id"]
    delete_response = client.delete(f"/cars/{car_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Car deleted successfully"

# Similar tests for broker endpoints
def test_create_broker():
    response = client.post("/brokers/", json=test_broker_data)
    assert response.status_code == 201
    assert "broker_id" in response.json()
    
    # Cleanup: Delete the created broker
    broker_id = response.json()["broker_id"]
    client.delete(f"/brokers/{broker_id}")

def test_create_multiple_brokers():
    brokers_data = [
        {"name": "John Doe", "branches": "Main Branch", "mobile": "+123456789", "email": "john.doe@example.com"},
        {"name": "Jane Smith", "branches": "Branch A", "mobile": "+987654321", "email": "jane.smith@example.com"},
        # Add more brokers as needed
    ]

    response = client.post("/brokers/", json=brokers_data)
    assert response.status_code == 201
    assert "broker_ids" in response.json()
    
    # Cleanup: Delete the created broker
    broker_ids = response.json()["broker_ids"]
    for broker_id in broker_ids:
        client.delete(f"/brokers/{broker_id}")

def test_read_broker():
    # Create a broker for testing
    create_response = client.post("/brokers/", json=test_broker_data)
    assert create_response.status_code == 201

    broker_id = create_response.json()["broker_id"]
    read_response = client.get(f"/brokers/{broker_id}")
    assert read_response.status_code == 200
    assert read_response.json()["name"] == test_broker_data["name"]
    
    # Cleanup: Delete the created broker
    client.delete(f"/brokers/{broker_id}")

def test_update_broker():
    # Create a broker for testing
    create_response = client.post("/brokers/", json=test_broker_data)
    assert create_response.status_code == 201

    broker_id = create_response.json()["broker_id"]
    update_data = {"name": "Jane Doe"}
    update_response = client.put(f"/brokers/{broker_id}", json=update_data)
    assert update_response.status_code == 200
    assert update_response.json()["message"] == "Broker updated successfully"
    
    # Cleanup: Delete the created broker
    client.delete(f"/brokers/{broker_id}")

def test_delete_broker():
    # Create a broker for testing
    create_response = client.post("/brokers/", json=test_broker_data)
    assert create_response.status_code == 201

    broker_id = create_response.json()["broker_id"]
    delete_response = client.delete(f"/brokers/{broker_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Broker deleted successfully"


# Test case for listing cars
# def test_list_cars():
#     response = client.get("/listing/cars/")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

# Run tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])

import pytest
import uuid

@pytest.mark.asyncio
async def test_calculate_distance(test_client, mock_utility_service):
    payload = {
        "origin_latitude": -33.4489,
        "origin_longitude": -70.6693,
        "target_latitude": -33.4569,
        "target_longitude": -70.6483
    }
    
    mock_utility_service.calculate_distance.return_value = 1250.5
    
    response = await test_client.post("/utilities/distance", json=payload)
    
    assert response.status_code == 201 
    assert response.json() == {"distance_meters": 1250.5}
    mock_utility_service.calculate_distance.assert_called_once()


@pytest.mark.asyncio
async def test_get_pets_in_radius(test_client, mock_utility_service):
    payload = {
        "latitude": -33.4489,
        "longitude": -70.6693,
        "radius_meters": 5000.0
    }
    
    pet_id = str(uuid.uuid4())
    
    mock_utility_service.find_pets_in_radius.return_value = [
        {"pet_id": uuid.UUID(pet_id), "distance_meters": 2500.0}
    ]
    
    response = await test_client.post("/utilities/radius", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    
    assert "pets" in data
    assert len(data["pets"]) == 1
    assert data["pets"][0]["pet_id"] == pet_id
    assert data["pets"][0]["distance_meters"] == 2500.0
    
    mock_utility_service.find_pets_in_radius.assert_called_once_with(
        -33.4489, -70.6693, 5000.0
    )
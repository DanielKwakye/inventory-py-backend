from fastapi.testclient import TestClient
from main import app
import pytest
from io import BytesIO

client = TestClient(app)

@pytest.fixture
def mock_get_products_command(mocker):
    # Patch where GetProductsCommand is used in your code
    mock_cmd = mocker.patch("controllers.inventory_controller.GetProductsCommand")
    instance = mock_cmd.return_value
    instance.execute.return_value = {
        "success": True,
        "data": [
            {"id": 1, "name": "Mock Shoe", "quantity": 10},
            {"id": 2, "name": "Mock Shirt", "quantity": 5}
        ]
    }
    return instance

def test_get_products_with_category(mock_get_products_command):
    response = client.get("/products?category=shirts")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert isinstance(json_data["data"], list)
    assert json_data["data"][0]["name"] == "Mock Shoe"

# ---------- POST /product ----------
@pytest.fixture
def mock_add_product_command(mocker):
    mock_cmd = mocker.patch("controllers.inventory_controller.AddProductCommand")
    instance = mock_cmd.return_value
    instance.execute.return_value = {"success": True, "data": {"id": 1, "message": "Product added"}}
    return instance

def test_add_product(mock_add_product_command):
    file_content = b"fake image data"
    files = {
        "image": ("test_image.jpg", BytesIO(file_content), "image/jpeg")
    }
    data = {
        "title": "Test Product",
        "category": "shoes",
        "cost_price": "10.0",
        "selling_price": "20.0",
        "quantity": "5",
        "user_role": "admin",
        "tax_value": "1.5",
        "discount_perc": "10"
    }
    response = client.post("/product", data=data, files=files)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert "data" in json_data

# ---------- PUT /product/{product_id} ----------
@pytest.fixture
def mock_edit_product_command(mocker):
    mock_cmd = mocker.patch("controllers.inventory_controller.EditProductCommand")
    instance = mock_cmd.return_value
    instance.execute.return_value = {"success": True, "data": {"id": 1, "message": "Product updated"}}
    return instance

def test_edit_product(mock_edit_product_command):
    payload = {
        "title": "Updated Product",
        "cost_price": 12.0,
        "selling_price": 25.0,
        "tax_value": 2.0,
        "discount_perc": 5.0,
        "user_role": "admin"
    }
    response = client.put("/product/1", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True

# ---------- DELETE /product/{product_id} ----------
@pytest.fixture
def mock_delete_product_command(mocker):
    mock_cmd = mocker.patch("controllers.inventory_controller.DeleteProductCommand")
    instance = mock_cmd.return_value
    instance.execute.return_value = {"success": True, "data": {"id": 1, "message": "Product deleted"}}
    return instance

def test_delete_product(mock_delete_product_command):
    response = client.delete("/product/1?user_role=admin")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True

# ---------- PUT /update-stock/{product_id} ----------
@pytest.fixture
def mock_update_stock_command(mocker):
    mock_cmd = mocker.patch("controllers.inventory_controller.UpdateStockCommand")
    instance = mock_cmd.return_value
    instance.execute.return_value = {"success": True, "data": {"id": 1, "message": "Stock updated"}}
    return instance

def test_update_stock(mock_update_stock_command):
    payload = {
        "user_role": "admin",
        "quantity": 15
    }
    response = client.put("/update-stock/1", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True

# ---------- POST /checkout ----------
@pytest.fixture
def mock_checkout_command(mocker):
    mock_cmd = mocker.patch("controllers.inventory_controller.CheckoutCommand")
    instance = mock_cmd.return_value
    instance.execute.return_value = {"success": True, "data": {"message": "Checkout complete"}}
    return instance

def test_checkout(mock_checkout_command):
    payload = {
        "user_role": "admin",
        "payload": [
            {"product_id": 1, "quantity": 2},
            {"product_id": 2, "quantity": 3}
        ]
    }
    response = client.post("/checkout", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True

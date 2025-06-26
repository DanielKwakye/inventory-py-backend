from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from typing import List, Dict

from patterns.commands.checkout_command import CheckoutCommand
from patterns.commands.delete_product_command import DeleteProductCommand
from patterns.commands.update_product_command import EditProductCommand
from patterns.commands.get_products_command import GetProductsCommand
from patterns.commands.add_product_command import AddProductCommand
from patterns.commands.update_stock_command import UpdateStockCommand
from patterns.observables.inventory_observable import Inventory
from patterns.observables.logger_observer import LoggerObserver
from patterns.proxys.inventory_proxy import InventoryProxy
from fastapi import UploadFile
import os

router = APIRouter()

inventory = Inventory()
inventory_proxy = InventoryProxy(inventory)

logger = LoggerObserver() # Logs every product action into the console
inventory_proxy.add_observer(logger) # add observers to listen to any action updates
inventory.add_observer(logger)


# Fetch all products with their quantity
@router.get("/products")
async def get_products(request: Request):
    category = request.query_params['category']
    if category is None:
        category = "shoes"
    cmd = GetProductsCommand(inventory_proxy=inventory_proxy, category=category)
    result = cmd.execute()
    return JSONResponse(content=result)


# Create a new product
@router.post("/product")
async def add_product(request: Request):
    form = await request.form()

    # Extract required fields from input
    title = form["title"]
    category = form["category"]
    cost_price = float(form["cost_price"])
    selling_price = float(form["selling_price"])
    quantity = int(form["quantity"])
    user_role = form["user_role"]
    tax_value = float(form["tax_value"])
    discount_perc = float(form["discount_perc"])

    # Get uploaded image file
    image: UploadFile = form["image"]

    # Save image
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    save_path = os.path.join(upload_dir, image.filename)
    with open(save_path, "wb") as f:
        f.write(await image.read())

    image_path = f"/uploads/{image.filename}"

    # Set author role (simulated user object with role)
    inventory_proxy.role = user_role

    # Construct and execute command
    command = AddProductCommand(
        inventory=inventory_proxy,
        title=title,
        category=category,
        cost_price=cost_price,
        selling_price=selling_price,
        quantity=quantity,
        image_path=image_path,
        tax_value=tax_value,
        discount_perc=discount_perc
    )
    result = command.execute()
    # result["image_url"] = image_url

    return JSONResponse(content=result)

# Update Product details
@router.put("/product/{product_id}")
async def edit_product(product_id: int, request: Request):
    data = await request.json()
    inventory_proxy.role = data["user_role"]
    cmd = EditProductCommand(
        inventory_proxy=inventory_proxy,
        product_id = product_id,
        title= data["title"],
        cost_price=float(data["cost_price"]),
        selling_price=float(data["selling_price"]),
        tax_value=float(data["tax_value"]),
        discount_perc=float(data["discount_perc"])
    )
    result = cmd.execute()
    return JSONResponse(content=result)

# Remove Product
@router.delete("/product/{product_id}")
async def delete_product(product_id:int, request: Request):
    user_role = request.query_params["user_role"]
    inventory_proxy.role = user_role
    cmd = DeleteProductCommand(inventory_proxy=inventory_proxy, product_id=product_id)
    result = cmd.execute()
    return JSONResponse(content=result)

# Update a product's stock ( product quantity )
@router.put("/update-stock/{product_id}")
async def update_stock(product_id: int, request: Request):
    data = await request.json()
    user_role, quantity =  data["user_role"], float(data["quantity"])
    inventory_proxy.role = user_role
    print("customLogV2:=", user_role, quantity)
    cmd = UpdateStockCommand(inventory_proxy=inventory_proxy, product_id=product_id, new_quantity=quantity)
    result = cmd.execute()
    return JSONResponse(content=result)

# Reduction of stock quantities
@router.post("/checkout")
async def checkout(request: Request):
    data = await request.json()
    user_role = data["user_role"]
    inventory_proxy.role = user_role
    payload: List[Dict[str, int]] = data.get("payload", [])

    # validate payload structure
    for item in payload:
        if not isinstance(item, dict) or \
                not isinstance(item.get("product_id"), int) or \
                not isinstance(item.get("quantity"), int):
            raise ValueError("Invalid payload format")

    cmd = CheckoutCommand(inventory_proxy=inventory_proxy, payload=payload)
    result = cmd.execute()
    return JSONResponse(content=result)



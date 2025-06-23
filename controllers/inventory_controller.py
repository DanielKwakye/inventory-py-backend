from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from patterns.commands.add_product_command import AddProductCommand
from patterns.commands.add_stock_command import AddStockCommand
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

@router.post("/increase-stock")
async def increase_stock(request: Request):

    author_id, product_id, quantity = request.get("user_role"), request.get('product_id'), request.get("quantity")
    cmd = AddStockCommand(author_id=author_id, product_id=product_id, quantity=quantity, inventory_proxy=inventory_proxy)
    cmd.execute()
    return JSONResponse(content={"message": "Stock updated successfully"})

@router.post("/reduce-stock")
async def reduce_stock(request: Request):
    data = await request.json()
    author_id = data["user_role"]
    product_name = data["name"]
    product_price = data["price"]
    cmd = AddProductCommand(inventory=inventory_proxy, name=product_name, price=product_price, author_id=author_id)
    cmd.execute()
    return JSONResponse(content={"message": "Product added"})

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

    # Build image URL
    base_url = str(request.base_url).rstrip("/")
    image_path = f"/uploads/{image.filename}"
    image_url = f"{base_url}/uploads/{image.filename}"

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
    result["image_url"] = image_url

    return JSONResponse(content=result)
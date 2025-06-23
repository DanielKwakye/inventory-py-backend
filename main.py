from fastapi import FastAPI
import controllers.inventory_controller as products_controller
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def index():
    return {"message": "API version 1.0.0"}

app.include_router(products_controller.router)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")



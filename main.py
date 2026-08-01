from fastapi import FastAPI
from model import Product

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}



products = [
    Product(
        id=1,
        name="Sample Product",
        description="This is a sample product.",
        price=9.99,
        quantity=100,
    )
]


@app.get("/products")
def get_all_products():
    return products


@app.get("/products/{id}")
def get_product_by_id(id: int):
    for p in products:
        if p.id == id:
            return p
    return {"error": "Product not found"}


@app.post("/products")
def add_a_product(product: Product):
    products.append(product)
    return product
  #  return {"message": "Product created successfully", "product": product_data}


@app.put("/products/{id}")
def update_product(id: int, updated_product: Product):
    for index, p in enumerate(products):
        if p.id == id:
            products[index] = updated_product
            return updated_product
    return {"error": "Product not found"}

@app.delete("/products/{id}")
def delete_product(id: int):
    for index, p in enumerate(products):
        if p.id == id:
            deleted_product = products.pop(index)
            return {"message": "Product deleted successfully", "product": deleted_product}
    return {"error": "Product not found"}
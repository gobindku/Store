from fastapi import Depends, FastAPI, HTTPException
from model import Product
from db import SessionLocal, engine
import db_model
from sqlalchemy.orm import Session

app = FastAPI()

db_model.Base.metadata.create_all(bind=engine)

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = SessionLocal()
    try:
        existing_ids = {row.id for row in db.query(db_model.Product.id).all()}
        for product in products:
            if product.id not in existing_ids:
                db.add(db_model.Product(**product.model_dump()))
        db.commit()
    finally:
        db.close()


init_db()


@app.get("/products")
def get_all_products( db: Session = Depends(get_db)):
   
   db_products = db.query(db_model.Product).all()

   return db_products


@app.get("/products/{id}")
def get_product_by_id(id: int,db: Session = Depends(get_db)):
    db_products = db.query(db_model.Product).filter(db_model.Product.id == id).first()

    if db_products:
            return db_products
    return {"error": "Product not found"}


@app.post("/products", response_model=Product)
def add_a_product(product: Product, db: Session = Depends(get_db)):
    db_product = db_model.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.put("/products/{id}", response_model=Product)
def update_product(id: int, updated_product: Product, db: Session = Depends(get_db)):
    db_product = db.query(db_model.Product).filter(db_model.Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    updated_data = updated_product.model_dump(exclude={"id"})
    for field, value in updated_data.items():
        setattr(db_product, field, value)

    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(db_model.Product).filter(db_model.Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    response = {
        "id": db_product.id,
        "name": db_product.name,
        "description": db_product.description,
        "price": db_product.price,
        "quantity": db_product.quantity,
    }
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully", "product": response}
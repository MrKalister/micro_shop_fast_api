from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str
    price: int


class ProductCreate(ProductBase):
    id: int


class Product(ProductBase):
    id: int

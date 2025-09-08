from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    description: str
    price: int


class ProductCreate(ProductBase):
    id: int


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

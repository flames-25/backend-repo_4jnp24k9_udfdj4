"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl, conlist
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Add your own schemas here:
# --------------------------------------------------

class MenuItem(BaseModel):
    """
    Cafe menu items
    Collection name: "menuitem"
    """
    name: str = Field(..., description="Item name")
    description: Optional[str] = Field(None, description="Short description")
    price: float = Field(..., ge=0, description="Price in local currency")
    category: str = Field(..., description="Category such as Tea, Coffee, Pastry, Seasonal")
    tags: Optional[List[str]] = Field(default=None, description="Optional tags like matcha, vegan, iced")
    image: Optional[str] = Field(default=None, description="Image URL")

class Inquiry(BaseModel):
    """
    Contact form submissions
    Collection name: "inquiry"
    """
    name: str = Field(..., description="Sender name")
    email: str = Field(..., description="Sender email")
    message: str = Field(..., min_length=5, max_length=2000, description="Message body")
    subject: Optional[str] = Field(None, description="Optional subject line")

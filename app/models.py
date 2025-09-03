from sqlmodel import SQLModel, Field, Relationship, JSON, Column
from datetime import datetime
from typing import Optional, List, Dict, Any
from decimal import Decimal
from enum import Enum


# Enums for structured data
class AnalysisStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AllergenSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    SEVERE = "severe"


# Persistent models (stored in database)
class User(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=50, unique=True)
    email: str = Field(unique=True, max_length=255, regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    full_name: Optional[str] = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    food_images: List["FoodImage"] = Relationship(back_populates="user")
    user_allergens: List["UserAllergen"] = Relationship(back_populates="user")


class FoodImage(SQLModel, table=True):
    __tablename__ = "food_images"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    filename: str = Field(max_length=255)
    file_path: str = Field(max_length=500)
    file_size: int = Field(gt=0)  # Size in bytes
    mime_type: str = Field(max_length=100)
    original_filename: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="food_images")
    nutritional_analysis: Optional["NutritionalAnalysis"] = Relationship(back_populates="food_image")


class NutritionalAnalysis(SQLModel, table=True):
    __tablename__ = "nutritional_analyses"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    food_image_id: int = Field(foreign_key="food_images.id", unique=True)
    status: AnalysisStatus = Field(default=AnalysisStatus.PENDING)

    # Food identification
    food_name: Optional[str] = Field(default=None, max_length=200)
    food_category: Optional[str] = Field(default=None, max_length=100)
    confidence_score: Optional[Decimal] = Field(default=None, decimal_places=4, max_digits=5)  # 0.0000 to 1.0000

    # Nutritional values per 100g
    calories: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)  # kcal
    protein: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)  # grams
    carbohydrates: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)  # grams
    total_fat: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)  # grams
    saturated_fat: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)  # grams
    fiber: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)  # grams
    sugar: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)  # grams
    sodium: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)  # mg

    # Vitamins (in mg or mcg as appropriate)
    vitamin_a: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)
    vitamin_c: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)
    vitamin_d: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)
    vitamin_e: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)
    vitamin_k: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)
    vitamin_b1: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)
    vitamin_b2: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)
    vitamin_b3: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)
    vitamin_b6: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)
    vitamin_b12: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)
    folate: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)

    # Minerals (in mg or mcg as appropriate)
    calcium: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)
    iron: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)
    magnesium: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)
    phosphorus: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)
    potassium: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)
    zinc: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)

    # Estimated portion information
    estimated_weight: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)  # grams
    serving_size: Optional[str] = Field(default=None, max_length=100)

    # Analysis metadata
    analysis_model: Optional[str] = Field(default=None, max_length=100)  # AI model used
    analysis_version: Optional[str] = Field(default=None, max_length=50)
    processing_time: Optional[Decimal] = Field(default=None, decimal_places=3, max_digits=8)  # seconds
    error_message: Optional[str] = Field(default=None, max_length=1000)
    raw_response: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    food_image: FoodImage = Relationship(back_populates="nutritional_analysis")
    allergens: List["AnalysisAllergen"] = Relationship(back_populates="analysis")


class Allergen(SQLModel, table=True):
    __tablename__ = "allergens"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True)  # e.g., "Peanuts", "Milk", "Eggs"
    category: Optional[str] = Field(default=None, max_length=50)  # e.g., "Tree Nuts", "Dairy"
    description: Optional[str] = Field(default=None, max_length=500)
    is_common: bool = Field(default=False)  # Flag for common allergens (top 8/14)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    analysis_allergens: List["AnalysisAllergen"] = Relationship(back_populates="allergen")
    user_allergens: List["UserAllergen"] = Relationship(back_populates="allergen")


class AnalysisAllergen(SQLModel, table=True):
    __tablename__ = "analysis_allergens"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    analysis_id: int = Field(foreign_key="nutritional_analyses.id")
    allergen_id: int = Field(foreign_key="allergens.id")
    severity: AllergenSeverity = Field(default=AllergenSeverity.LOW)
    confidence: Optional[Decimal] = Field(default=None, decimal_places=4, max_digits=5)  # 0.0000 to 1.0000
    notes: Optional[str] = Field(default=None, max_length=500)
    detected_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    analysis: NutritionalAnalysis = Relationship(back_populates="allergens")
    allergen: Allergen = Relationship(back_populates="analysis_allergens")


class UserAllergen(SQLModel, table=True):
    __tablename__ = "user_allergens"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    allergen_id: int = Field(foreign_key="allergens.id")
    severity: AllergenSeverity = Field(default=AllergenSeverity.MEDIUM)
    notes: Optional[str] = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="user_allergens")
    allergen: Allergen = Relationship(back_populates="user_allergens")


# Non-persistent schemas (for validation, forms, API requests/responses)
class UserCreate(SQLModel, table=False):
    username: str = Field(max_length=50)
    email: str = Field(max_length=255)
    full_name: Optional[str] = Field(default=None, max_length=100)


class UserUpdate(SQLModel, table=False):
    username: Optional[str] = Field(default=None, max_length=50)
    email: Optional[str] = Field(default=None, max_length=255)
    full_name: Optional[str] = Field(default=None, max_length=100)
    is_active: Optional[bool] = Field(default=None)


class FoodImageUpload(SQLModel, table=False):
    filename: str = Field(max_length=255)
    file_path: str = Field(max_length=500)
    file_size: int = Field(gt=0)
    mime_type: str = Field(max_length=100)
    original_filename: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)


class NutritionalAnalysisCreate(SQLModel, table=False):
    food_image_id: int
    food_name: Optional[str] = Field(default=None, max_length=200)
    food_category: Optional[str] = Field(default=None, max_length=100)
    confidence_score: Optional[Decimal] = Field(default=None)

    # Nutritional values
    calories: Optional[Decimal] = Field(default=None)
    protein: Optional[Decimal] = Field(default=None)
    carbohydrates: Optional[Decimal] = Field(default=None)
    total_fat: Optional[Decimal] = Field(default=None)
    saturated_fat: Optional[Decimal] = Field(default=None)
    fiber: Optional[Decimal] = Field(default=None)
    sugar: Optional[Decimal] = Field(default=None)
    sodium: Optional[Decimal] = Field(default=None)

    # Vitamins
    vitamin_a: Optional[Decimal] = Field(default=None)
    vitamin_c: Optional[Decimal] = Field(default=None)
    vitamin_d: Optional[Decimal] = Field(default=None)
    vitamin_e: Optional[Decimal] = Field(default=None)
    vitamin_k: Optional[Decimal] = Field(default=None)
    vitamin_b1: Optional[Decimal] = Field(default=None)
    vitamin_b2: Optional[Decimal] = Field(default=None)
    vitamin_b3: Optional[Decimal] = Field(default=None)
    vitamin_b6: Optional[Decimal] = Field(default=None)
    vitamin_b12: Optional[Decimal] = Field(default=None)
    folate: Optional[Decimal] = Field(default=None)

    # Minerals
    calcium: Optional[Decimal] = Field(default=None)
    iron: Optional[Decimal] = Field(default=None)
    magnesium: Optional[Decimal] = Field(default=None)
    phosphorus: Optional[Decimal] = Field(default=None)
    potassium: Optional[Decimal] = Field(default=None)
    zinc: Optional[Decimal] = Field(default=None)

    # Portion information
    estimated_weight: Optional[Decimal] = Field(default=None)
    serving_size: Optional[str] = Field(default=None, max_length=100)

    # Analysis metadata
    analysis_model: Optional[str] = Field(default=None, max_length=100)
    analysis_version: Optional[str] = Field(default=None, max_length=50)
    processing_time: Optional[Decimal] = Field(default=None)


class NutritionalAnalysisUpdate(SQLModel, table=False):
    status: Optional[AnalysisStatus] = Field(default=None)
    error_message: Optional[str] = Field(default=None, max_length=1000)
    raw_response: Optional[Dict[str, Any]] = Field(default=None)


class AllergenCreate(SQLModel, table=False):
    name: str = Field(max_length=100)
    category: Optional[str] = Field(default=None, max_length=50)
    description: Optional[str] = Field(default=None, max_length=500)
    is_common: bool = Field(default=False)


class AnalysisAllergenCreate(SQLModel, table=False):
    analysis_id: int
    allergen_id: int
    severity: AllergenSeverity = Field(default=AllergenSeverity.LOW)
    confidence: Optional[Decimal] = Field(default=None)
    notes: Optional[str] = Field(default=None, max_length=500)


class UserAllergenCreate(SQLModel, table=False):
    user_id: int
    allergen_id: int
    severity: AllergenSeverity = Field(default=AllergenSeverity.MEDIUM)
    notes: Optional[str] = Field(default=None, max_length=500)


# Response schemas for API
class NutritionalAnalysisResponse(SQLModel, table=False):
    id: int
    food_image_id: int
    status: AnalysisStatus
    food_name: Optional[str]
    food_category: Optional[str]
    confidence_score: Optional[Decimal]

    # Nutritional values
    calories: Optional[Decimal]
    protein: Optional[Decimal]
    carbohydrates: Optional[Decimal]
    total_fat: Optional[Decimal]
    fiber: Optional[Decimal]
    sugar: Optional[Decimal]
    sodium: Optional[Decimal]

    # Key vitamins and minerals
    vitamin_c: Optional[Decimal]
    calcium: Optional[Decimal]
    iron: Optional[Decimal]

    # Portion information
    estimated_weight: Optional[Decimal]
    serving_size: Optional[str]

    created_at: str  # ISO format datetime string
    allergens: List[str] = Field(default_factory=list)  # Simple allergen names


class FoodImageResponse(SQLModel, table=False):
    id: int
    filename: str
    original_filename: Optional[str]
    file_size: int
    description: Optional[str]
    uploaded_at: str  # ISO format datetime string
    analysis_status: Optional[AnalysisStatus]

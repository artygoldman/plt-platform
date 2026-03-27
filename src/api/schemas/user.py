from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    email: EmailStr
    name: str
    date_of_birth: date
    sex: str  # "male" or "female"
    timezone: str = "UTC"


class UserResponse(BaseModel):
    """Schema for user response."""

    id: UUID
    email: str
    name: str
    date_of_birth: date
    sex: str
    created_at: datetime
    subscription_tier: str

    model_config = ConfigDict(from_attributes=True)


class UserProfileResponse(BaseModel):
    """Schema for user profile data."""

    height_cm: float | None = None
    weight_kg: float | None = None
    blood_type: str | None = None
    allergies: list = []
    medications: list = []
    genetic_risks: dict = {}
    goals: list = []

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    """Schema for user login request."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password")


class UserRegister(BaseModel):
    """Schema for user registration request."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password (min 8 chars)")
    name: str = Field(..., min_length=2, description="User full name")
    date_of_birth: date = Field(..., description="User date of birth (YYYY-MM-DD)")
    sex: str = Field(..., description="Biological sex (male/female)")
    timezone: str = Field(default="UTC", description="User timezone (IANA format)")


class TokenResponse(BaseModel):
    """Schema for JWT token response."""

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration in seconds")
    user: UserResponse = Field(..., description="Authenticated user details")


class UserProfileUpdate(BaseModel):
    """Schema for updating user health profile."""

    height_cm: float | None = None
    weight_kg: float | None = None
    blood_type: str | None = None
    allergies: list[str] | None = None
    medications: list[str] | None = None
    genetic_risks: dict | None = None
    goals: list[str] | None = None

    model_config = ConfigDict(from_attributes=True)

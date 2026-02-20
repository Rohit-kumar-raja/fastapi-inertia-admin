from pydantic import Field, EmailStr
from typing import Optional, List, Dict
from ....core.common.schemas import BaseSchema


class ProfileUpdateSchema(BaseSchema):
    """Schema for updating user profile."""
    username: str = Field(max_length=150, description="Username")
    email: EmailStr = Field(description="Email Address")
    phone: Optional[str] = Field(None, max_length=20, description="Phone Number")


class PasswordChangeSchema(BaseSchema):
    """Schema for changing password."""
    current_password: str = Field(min_length=1, description="Current Password")
    new_password: str = Field(min_length=8, max_length=128, description="New Password")
    confirm_password: str = Field(min_length=8, max_length=128, description="Confirm Password")


class CompanyInfoSchema(BaseSchema):
    """Schema for company info — all fields optional for partial updates."""
    name: Optional[str] = Field(None, max_length=255)
    legal_name: Optional[str] = Field(None, max_length=255)
    tagline: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = Field(None)

    # Contact
    email: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=50)
    fax: Optional[str] = Field(None, max_length=50)
    website: Optional[str] = Field(None, max_length=500)

    # Address
    address_line1: Optional[str] = Field(None, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    zip_code: Optional[str] = Field(None, max_length=20)

    # Tax & Registration
    tax_id: Optional[str] = Field(None, max_length=100)
    gst_number: Optional[str] = Field(None, max_length=100)
    registration_number: Optional[str] = Field(None, max_length=100)
    pan_number: Optional[str] = Field(None, max_length=50)

    # Branding
    logo_url: Optional[str] = Field(None, max_length=500)
    favicon_url: Optional[str] = Field(None, max_length=500)

    # Social Media
    facebook: Optional[str] = Field(None, max_length=500)
    twitter: Optional[str] = Field(None, max_length=500)
    linkedin: Optional[str] = Field(None, max_length=500)
    instagram: Optional[str] = Field(None, max_length=500)
    youtube: Optional[str] = Field(None, max_length=500)
    github: Optional[str] = Field(None, max_length=500)

    # Locale
    currency: Optional[str] = Field(None, max_length=10)
    timezone: Optional[str] = Field(None, max_length=100)
    date_format: Optional[str] = Field(None, max_length=50)
    language: Optional[str] = Field(None, max_length=10)

    # Legal
    copyright_text: Optional[str] = Field(None, max_length=500)
    terms_url: Optional[str] = Field(None, max_length=500)
    privacy_url: Optional[str] = Field(None, max_length=500)


class AppSettingSchema(BaseSchema):
    """Schema for a single key-value setting."""
    key: str = Field(max_length=255, description="Setting key")
    value: Optional[str] = Field(None, description="Setting value")
    group: Optional[str] = Field("general", max_length=100, description="Setting group")
    description: Optional[str] = Field(None, max_length=500)


class AppSettingBulkSchema(BaseSchema):
    """Schema for bulk upsert of settings."""
    settings: List[AppSettingSchema] = Field(description="List of settings to upsert")

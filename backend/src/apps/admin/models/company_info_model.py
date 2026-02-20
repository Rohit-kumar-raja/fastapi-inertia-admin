from typing import Optional
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from .. import BaseModel


class CompanyInfoModel(BaseModel):
    """
    Stores company/organization details.
    Only one row expected — the application's company info.
    """

    __tablename__ = "app_company_info"

    # Basic Info
    name: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    legal_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    tagline: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Contact
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    fax: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Address
    address_line1: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address_line2: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    zip_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # Tax & Registration
    tax_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    gst_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    registration_number: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )
    pan_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Branding
    logo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    favicon_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Social Media
    facebook: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    twitter: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    linkedin: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    instagram: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    youtube: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    github: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Currency & Locale
    currency: Mapped[Optional[str]] = mapped_column(
        String(10), nullable=True, default="INR"
    )
    timezone: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, default="Asia/Kolkata"
    )
    date_format: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default="DD/MM/YYYY"
    )
    language: Mapped[Optional[str]] = mapped_column(
        String(10), nullable=True, default="en"
    )

    # Footer / Legal
    copyright_text: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    terms_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    privacy_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

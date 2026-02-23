from typing import Optional, List, Dict
from uuid import UUID
from datetime import datetime

from core.security.models.user_model import UserModel
from core.security.repositories.user_repository import UserRepository
from core.security.utils.hash import verify_password, make_password
from core.common.uow.uow import AsyncUnitOfWork
from ..models.company_info_model import CompanyInfoModel
from ..models.app_setting_model import AppSettingModel
from ..repositories.app_setting_repository import AppSettingRepository
from ..repositories.company_info_repository import CompanyInfoRepository


class SettingService:
    """Service for managing user settings, company info, and app settings."""
    def __init__(self, uow: AsyncUnitOfWork[AppSettingRepository]):
        self.uow = uow

    # ─── User Profile ────────────────────────────────────────────

    async def get_user_profile(self, user_id: UUID) -> Optional[dict]:
        """Fetch the current user's profile data."""
        user_repo = self.uow.get_repo(UserRepository)
        user = await user_repo.get_by_id(str(user_id))
        if user:
            return {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
            }
        return None

    async def update_profile(self, user_id: UUID, data: dict) -> Optional[dict]:
        """Update the current user's profile fields."""
        user_repo = self.uow.get_repo(UserRepository)
        
        # Check if username exists
        existing_by_username = await user_repo.get_by_username(data["username"])
        if existing_by_username and str(existing_by_username.id) != str(user_id):
            return {"error": "Username already exists"}

        # Check if email exists
        existing_by_email = await user_repo.get_by_email(data["email"])
        if existing_by_email and str(existing_by_email.id) != str(user_id):
            return {"error": "Email already exists"}

        # Perform update
        user = await user_repo.get_by_id(str(user_id))
        if user:
            for key, value in data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            await user_repo.update(user)
            return await self.get_user_profile(user_id)
        return {"error": "User not found"}

    async def change_password(self, user_id: UUID, current_password: str, new_password: str) -> dict:
        """Verify current password and update to new password."""
        user_repo = self.uow.get_repo(UserRepository)
        user = await user_repo.get_by_id(str(user_id))
        if not user:
            return {"error": "User not found"}

        if not verify_password(current_password, user.password):
            return {"error": "Current password is incorrect"}

        user.password = make_password(new_password)
        await user_repo.update(user)
        return {"success": True}

    # ─── Company Info ────────────────────────────────────────────

    async def get_company_info(self) -> Optional[dict]:
        """Fetch company info (first/only row)."""
        company_repo = self.uow.get_repo(CompanyInfoRepository)
        company = await company_repo.get_company_info()
        if not company:
            return None
        # Convert to dict, exclude internal fields
        data = {}
        for col in CompanyInfoModel.__table__.columns:
            if col.name not in ("deleted_at",):
                val = getattr(company, col.name)
                data[col.name] = str(val) if val is not None and col.name == "id" else val
        return data

    async def upsert_company_info(self, data: dict) -> dict:
        """Create or update company info (single row)."""
        company_repo = self.uow.get_repo(CompanyInfoRepository)
        company = await company_repo.get_company_info()

        # Remove keys with None values so we don't overwrite existing data with nulls
        clean_data = {k: v for k, v in data.items() if v is not None}
        clean_data.pop("id", None)
        clean_data.pop("is_active", None)

        if company:
            for key, value in clean_data.items():
                if hasattr(company, key):
                    setattr(company, key, value)
            await company_repo.update(company)
        else:
            company = CompanyInfoModel(**clean_data)
            await company_repo.add(company)

        return await self.get_company_info()

    # ─── App Settings (Key-Value) ────────────────────────────────

    async def get_all_settings(self, group: Optional[str] = None) -> List[dict]:
        """Fetch all settings, optionally filtered by group."""
        settings = await self.uow.repo.get_all_settings(group)
        return [
            {
                "id": str(s.id),
                "key": s.key,
                "value": s.value,
                "group": s.group,
                "description": s.description,
            }
            for s in settings
        ]

    async def get_setting(self, key: str) -> Optional[dict]:
        """Fetch a single setting by key."""
        setting = await self.uow.repo.get_by_key(key)
        if setting:
            return {
                "id": str(setting.id),
                "key": setting.key,
                "value": setting.value,
                "group": setting.group,
                "description": setting.description,
            }
        return None

    async def upsert_setting(self, data: dict) -> dict:
        """Create or update a single setting by key."""
        setting = await self.uow.repo.get_by_key(data["key"])

        if setting:
            setting.value = data.get("value", setting.value)
            setting.group = data.get("group", setting.group)
            setting.description = data.get("description", setting.description)
            await self.uow.repo.update(setting)
        else:
            clean_data = {k: v for k, v in data.items() if k in ("key", "value", "group", "description")}
            setting = AppSettingModel(**clean_data)
            await self.uow.repo.add(setting)

        return {
            "id": str(setting.id),
            "key": setting.key,
            "value": setting.value,
            "group": setting.group,
            "description": setting.description,
        }

    async def bulk_upsert_settings(self, settings_list: List[dict]) -> List[dict]:
        """Bulk create/update settings."""
        for data in settings_list:
            await self.upsert_setting(data)
        return await self.get_all_settings()

    async def delete_setting(self, key: str) -> bool:
        """Delete a setting by key (soft delete)."""
        setting = await self.uow.repo.get_by_key(key)
        if setting:
            await self.uow.repo.delete(setting)
            return True
        return False

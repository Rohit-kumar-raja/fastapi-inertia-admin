from typing import Optional, List, Dict
from uuid import UUID
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.security.models.user_model import UserModel
from core.security.utils.hash import verify_password, make_password
from ..models.company_info_model import CompanyInfoModel
from ..models.app_setting_model import AppSettingModel


class SettingService:
    """Service for managing user settings, company info, and app settings."""

    # ─── User Profile ────────────────────────────────────────────

    @staticmethod
    async def get_user_profile(user_id: UUID, session: AsyncSession) -> Optional[dict]:
        """Fetch the current user's profile data."""
        statement = select(UserModel).where(
            UserModel.id == user_id,
            UserModel.deleted_at.is_(None),
        )
        result = await session.execute(statement)
        user = result.scalars().first()
        if user:
            return {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
            }
        return None

    @staticmethod
    async def update_profile(user_id: UUID, data: dict, session: AsyncSession) -> Optional[dict]:
        """Update the current user's profile fields."""
        try:
            existing = await session.execute(
                select(UserModel).where(
                    UserModel.username == data["username"],
                    UserModel.id != user_id,
                    UserModel.deleted_at.is_(None),
                )
            )
            if existing.scalars().first():
                return {"error": "Username already exists"}

            existing = await session.execute(
                select(UserModel).where(
                    UserModel.email == data["email"],
                    UserModel.id != user_id,
                    UserModel.deleted_at.is_(None),
                )
            )
            if existing.scalars().first():
                return {"error": "Email already exists"}

            await session.execute(
                update(UserModel)
                .where(UserModel.id == user_id, UserModel.deleted_at.is_(None))
                .values(**data)
            )
            await session.commit()
            return await SettingService.get_user_profile(user_id, session)
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def change_password(
        user_id: UUID,
        current_password: str,
        new_password: str,
        session: AsyncSession,
    ) -> dict:
        """Verify current password and update to new password."""
        user = await session.get(UserModel, user_id)
        if not user:
            return {"error": "User not found"}

        if not verify_password(current_password, user.password):
            return {"error": "Current password is incorrect"}

        user.password = make_password(new_password)
        await session.commit()
        return {"success": True}

    # ─── Company Info ────────────────────────────────────────────

    @staticmethod
    async def get_company_info(session: AsyncSession) -> Optional[dict]:
        """Fetch company info (first/only row)."""
        result = await session.execute(
            select(CompanyInfoModel).where(CompanyInfoModel.deleted_at.is_(None)).limit(1)
        )
        company = result.scalars().first()
        if not company:
            return None
        # Convert to dict, exclude internal fields
        data = {}
        for col in CompanyInfoModel.__table__.columns:
            if col.name not in ("deleted_at",):
                val = getattr(company, col.name)
                data[col.name] = str(val) if val is not None and col.name == "id" else val
        return data

    @staticmethod
    async def upsert_company_info(data: dict, session: AsyncSession) -> dict:
        """Create or update company info (single row)."""
        try:
            result = await session.execute(
                select(CompanyInfoModel).where(CompanyInfoModel.deleted_at.is_(None)).limit(1)
            )
            company = result.scalars().first()

            # Remove keys with None values so we don't overwrite existing data with nulls
            clean_data = {k: v for k, v in data.items() if v is not None}
            clean_data.pop("id", None)
            clean_data.pop("is_active", None)

            if company:
                for key, value in clean_data.items():
                    if hasattr(company, key):
                        setattr(company, key, value)
            else:
                company = CompanyInfoModel(**clean_data)
                session.add(company)

            await session.commit()
            await session.refresh(company)
            return await SettingService.get_company_info(session)
        except Exception as e:
            await session.rollback()
            raise e

    # ─── App Settings (Key-Value) ────────────────────────────────

    @staticmethod
    async def get_all_settings(session: AsyncSession, group: Optional[str] = None) -> List[dict]:
        """Fetch all settings, optionally filtered by group."""
        stmt = select(AppSettingModel).where(AppSettingModel.deleted_at.is_(None))
        if group:
            stmt = stmt.where(AppSettingModel.group == group)
        stmt = stmt.order_by(AppSettingModel.group, AppSettingModel.key)
        result = await session.execute(stmt)
        settings = result.scalars().all()
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

    @staticmethod
    async def get_setting(key: str, session: AsyncSession) -> Optional[dict]:
        """Fetch a single setting by key."""
        result = await session.execute(
            select(AppSettingModel).where(
                AppSettingModel.key == key,
                AppSettingModel.deleted_at.is_(None),
            )
        )
        setting = result.scalars().first()
        if setting:
            return {
                "id": str(setting.id),
                "key": setting.key,
                "value": setting.value,
                "group": setting.group,
                "description": setting.description,
            }
        return None

    @staticmethod
    async def upsert_setting(data: dict, session: AsyncSession) -> dict:
        """Create or update a single setting by key."""
        try:
            result = await session.execute(
                select(AppSettingModel).where(
                    AppSettingModel.key == data["key"],
                    AppSettingModel.deleted_at.is_(None),
                )
            )
            setting = result.scalars().first()

            if setting:
                setting.value = data.get("value", setting.value)
                setting.group = data.get("group", setting.group)
                setting.description = data.get("description", setting.description)
            else:
                clean_data = {k: v for k, v in data.items() if k in ("key", "value", "group", "description")}
                setting = AppSettingModel(**clean_data)
                session.add(setting)

            await session.commit()
            await session.refresh(setting)
            return {
                "id": str(setting.id),
                "key": setting.key,
                "value": setting.value,
                "group": setting.group,
                "description": setting.description,
            }
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def bulk_upsert_settings(settings_list: List[dict], session: AsyncSession) -> List[dict]:
        """Bulk create/update settings."""
        try:
            for data in settings_list:
                await SettingService.upsert_setting(data, session)
            return await SettingService.get_all_settings(session)
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def delete_setting(key: str, session: AsyncSession) -> bool:
        """Delete a setting by key (soft delete)."""
        result = await session.execute(
            select(AppSettingModel).where(
                AppSettingModel.key == key,
                AppSettingModel.deleted_at.is_(None),
            )
        )
        setting = result.scalars().first()
        if setting:
            from datetime import datetime
            setting.deleted_at = datetime.utcnow()
            await session.commit()
            return True
        return False

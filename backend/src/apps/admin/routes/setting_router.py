from typing import Optional
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from .. import InertiaDep, web_auth, get_db
from ..schemas.setting_schema import (
    ProfileUpdateSchema,
    PasswordChangeSchema,
    CompanyInfoSchema,
    AppSettingSchema,
    AppSettingBulkSchema,
)
from ..services.setting_service import SettingService
from core.security.utils import response, error_response

setting_router = APIRouter(dependencies=[Depends(web_auth)])


# ─── Page Render ─────────────────────────────────────────────

@setting_router.get("/settings")
async def settings(request: Request, inertia: InertiaDep, session: AsyncSession = Depends(get_db)):
    """Render the settings page with user + company data."""
    current_user = request.state.user
    user_data = await SettingService.get_user_profile(current_user["id"], session)
    company_data = await SettingService.get_company_info(session)
    app_settings = await SettingService.get_all_settings(session)
    return await inertia.render("Admin/Settings/Index", {
        "user": user_data,
        "company": company_data,
        "app_settings": app_settings,
    })


# ─── User Profile ───────────────────────────────────────────

@setting_router.get("/settings/profile")
async def get_profile(
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    """Get current user's profile."""
    current_user = request.state.user
    user_data = await SettingService.get_user_profile(current_user["id"], session)
    if not user_data:
        return error_response(message="User not found", status_code=404)
    return response(data=user_data, message="Profile fetched successfully")


@setting_router.put("/settings/profile")
async def update_profile(
    data: ProfileUpdateSchema,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    """Update current user's profile."""
    current_user = request.state.user
    result = await SettingService.update_profile(
        current_user["id"], data.model_dump(exclude_none=True), session
    )
    if result and "error" in result:
        return error_response(message=result["error"], status_code=422)
    return response(data=result, message="Profile updated successfully")


@setting_router.put("/settings/password")
async def change_password(
    data: PasswordChangeSchema,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    """Change current user's password."""
    if data.new_password != data.confirm_password:
        return error_response(message="Passwords do not match", status_code=422)

    current_user = request.state.user
    result = await SettingService.change_password(
        current_user["id"],
        data.current_password,
        data.new_password,
        session,
    )
    if "error" in result:
        return error_response(message=result["error"], status_code=422)
    return response(data=None, message="Password changed successfully")


# ─── Company Info ────────────────────────────────────────────

@setting_router.get("/settings/company")
async def get_company_info(session: AsyncSession = Depends(get_db)):
    """Fetch company info."""
    data = await SettingService.get_company_info(session)
    return response(data=data, message="Company info fetched successfully")


@setting_router.put("/settings/company")
async def update_company_info(
    data: CompanyInfoSchema,
    session: AsyncSession = Depends(get_db),
):
    """Create or update company info."""
    result = await SettingService.upsert_company_info(data.model_dump(), session)
    return response(data=result, message="Company info updated successfully")


# ─── App Settings (Key-Value) ────────────────────────────────

@setting_router.get("/settings/app")
async def get_app_settings(
    group: Optional[str] = None,
    session: AsyncSession = Depends(get_db),
):
    """Fetch all app settings, optionally filtered by group."""
    data = await SettingService.get_all_settings(session, group=group)
    return response(data=data, message="Settings fetched successfully")


@setting_router.get("/settings/app/{key}")
async def get_app_setting(key: str, session: AsyncSession = Depends(get_db)):
    """Fetch a single app setting by key."""
    data = await SettingService.get_setting(key, session)
    if not data:
        return error_response(message="Setting not found", status_code=404)
    return response(data=data, message="Setting fetched successfully")


@setting_router.put("/settings/app")
async def upsert_app_setting(
    data: AppSettingSchema,
    session: AsyncSession = Depends(get_db),
):
    """Create or update a single app setting."""
    result = await SettingService.upsert_setting(data.model_dump(), session)
    return response(data=result, message="Setting saved successfully")


@setting_router.put("/settings/app/bulk")
async def bulk_upsert_app_settings(
    data: AppSettingBulkSchema,
    session: AsyncSession = Depends(get_db),
):
    """Bulk create/update app settings."""
    settings_list = [s.model_dump() for s in data.settings]
    result = await SettingService.bulk_upsert_settings(settings_list, session)
    return response(data=result, message="Settings saved successfully")


@setting_router.delete("/settings/app/{key}")
async def delete_app_setting(key: str, session: AsyncSession = Depends(get_db)):
    """Delete an app setting by key."""
    deleted = await SettingService.delete_setting(key, session)
    if not deleted:
        return error_response(message="Setting not found", status_code=404)
    return response(data=None, message="Setting deleted successfully")

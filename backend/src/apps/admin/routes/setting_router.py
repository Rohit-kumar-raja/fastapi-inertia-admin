from typing import Optional
from fastapi import APIRouter, Depends, Request
from .. import InertiaDep, web_auth
from ..schemas.setting_schema import (
    ProfileUpdateSchema,
    PasswordChangeSchema,
    CompanyInfoSchema,
    AppSettingSchema,
    AppSettingBulkSchema,
)
from ..services.setting_service import SettingService
from ..repositories.app_setting_repository import AppSettingRepository
from core.dependencies.service_dependency import get_service
from core.security.utils import response, error_response

setting_router = APIRouter(dependencies=[Depends(web_auth)])


# ─── Page Render ─────────────────────────────────────────────

@setting_router.get("/settings")
async def settings(
    request: Request, 
    inertia: InertiaDep, 
    setting_service: SettingService = Depends(get_service(SettingService, AppSettingRepository))
):
    """Render the settings page with user + company data."""
    current_user = request.state.user
    user_data = await setting_service.get_user_profile(current_user["id"])
    company_data = await setting_service.get_company_info()
    app_settings = await setting_service.get_all_settings()
    return await inertia.render("Admin/Settings/Index", {
        "user": user_data,
        "company": company_data,
        "app_settings": app_settings,
    })


# ─── User Profile ───────────────────────────────────────────

@setting_router.get("/settings/profile")
async def get_profile(
    request: Request,
    setting_service: SettingService = Depends(get_service(SettingService, AppSettingRepository))
):
    """Get current user's profile."""
    current_user = request.state.user
    user_data = await setting_service.get_user_profile(current_user["id"])
    if not user_data:
        return error_response(message="User not found", status_code=404)
    return response(data=user_data, message="Profile fetched successfully")


@setting_router.put("/settings/profile")
async def update_profile(
    data: ProfileUpdateSchema,
    request: Request,
    setting_service: SettingService = Depends(get_service(SettingService, AppSettingRepository))
):
    """Update current user's profile."""
    current_user = request.state.user
    result = await setting_service.update_profile(
        current_user["id"], data.model_dump(exclude_none=True)
    )
    if result and "error" in result:
        return error_response(message=result["error"], status_code=422)
    return response(data=result, message="Profile updated successfully")


@setting_router.put("/settings/password")
async def change_password(
    data: PasswordChangeSchema,
    request: Request,
    setting_service: SettingService = Depends(get_service(SettingService, AppSettingRepository))
):
    """Change current user's password."""
    if data.new_password != data.confirm_password:
        return error_response(message="Passwords do not match", status_code=422)

    current_user = request.state.user
    result = await setting_service.change_password(
        current_user["id"],
        data.current_password,
        data.new_password,
    )
    if "error" in result:
        return error_response(message=result["error"], status_code=422)
    return response(data=None, message="Password changed successfully")


# ─── Company Info ────────────────────────────────────────────

@setting_router.get("/settings/company")
async def get_company_info(
    setting_service: SettingService = Depends(get_service(SettingService, AppSettingRepository))
):
    """Fetch company info."""
    data = await setting_service.get_company_info()
    return response(data=data, message="Company info fetched successfully")


@setting_router.put("/settings/company")
async def update_company_info(
    data: CompanyInfoSchema,
    setting_service: SettingService = Depends(get_service(SettingService, AppSettingRepository))
):
    """Create or update company info."""
    result = await setting_service.upsert_company_info(data.model_dump())
    return response(data=result, message="Company info updated successfully")


# ─── App Settings (Key-Value) ────────────────────────────────

@setting_router.get("/settings/app")
async def get_app_settings(
    group: Optional[str] = None,
    setting_service: SettingService = Depends(get_service(SettingService, AppSettingRepository))
):
    """Fetch all app settings, optionally filtered by group."""
    data = await setting_service.get_all_settings(group=group)
    return response(data=data, message="Settings fetched successfully")


@setting_router.get("/settings/app/{key}")
async def get_app_setting(
    key: str, 
    setting_service: SettingService = Depends(get_service(SettingService, AppSettingRepository))
):
    """Fetch a single app setting by key."""
    data = await setting_service.get_setting(key)
    if not data:
        return error_response(message="Setting not found", status_code=404)
    return response(data=data, message="Setting fetched successfully")


@setting_router.put("/settings/app")
async def upsert_app_setting(
    data: AppSettingSchema,
    setting_service: SettingService = Depends(get_service(SettingService, AppSettingRepository))
):
    """Create or update a single app setting."""
    result = await setting_service.upsert_setting(data.model_dump())
    return response(data=result, message="Setting saved successfully")


@setting_router.put("/settings/app/bulk")
async def bulk_upsert_app_settings(
    data: AppSettingBulkSchema,
    setting_service: SettingService = Depends(get_service(SettingService, AppSettingRepository))
):
    """Bulk create/update app settings."""
    settings_list = [s.model_dump() for s in data.settings]
    result = await setting_service.bulk_upsert_settings(settings_list)
    return response(data=result, message="Settings saved successfully")


@setting_router.delete("/settings/app/{key}")
async def delete_app_setting(
    key: str, 
    setting_service: SettingService = Depends(get_service(SettingService, AppSettingRepository))
):
    """Delete an app setting by key."""
    deleted = await setting_service.delete_setting(key)
    if not deleted:
        return error_response(message="Setting not found", status_code=404)
    return response(data=None, message="Setting deleted successfully")

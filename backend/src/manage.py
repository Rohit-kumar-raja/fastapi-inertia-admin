import asyncio
import subprocess
import typer

# from fastapi_cli.cli import app
from fastapi.routing import APIRoute
from fpcli import app


@app.command()
def shell():
    import IPython

    IPython.start_ipython(argv=[])


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True}, add_help_option=False)
def linter(ctx: typer.Context):
    import subprocess

    subprocess.run(["ruff"] + ctx.args)


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True}, add_help_option=False)
def migrationmanager(ctx: typer.Context):
    import subprocess

    subprocess.run(["alembic"] + ctx.args)


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True}, add_help_option=False)
def test(ctx: typer.Context):
    import subprocess

    subprocess.run(["pytest"] + ctx.args)


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True}, add_help_option=False)
def docs(ctx: typer.Context):
    import subprocess

    subprocess.run(["mkdocs"] + ctx.args)


async def url_generator():
    from main import app
    from apps.admin.services.backend_url_service import BackendUrlService
    from core.config.database import AsyncSessionLocal

    async with AsyncSessionLocal() as session:
        for route in app.routes:
            if isinstance(route, APIRoute):
                name = route.name
                path: str = route.path
                methods = list(route.methods)[0]
                data = {
                    "name": name,
                    "path": path.replace("{uuid}", ""),
                    "method": methods,
                    "description": "Auto-generated URL",
                    "is_active": True,
                }
                await BackendUrlService.create(
                    data=data,
                    session=session,
                )


@app.command()
def generateurl():
    import asyncio

    asyncio.run(url_generator())


@app.command()
def dropall():
    import shutil
    import os
    from sqlalchemy import text
    from core.config.database import engine

    async def async_drop():
        async with engine.begin() as conn:
            print("Dropping public schema...")
            await conn.execute(text("DROP SCHEMA public CASCADE"))
            await conn.execute(text("CREATE SCHEMA public"))
        # Engine will reconnect cleanly on next use

        print("Schema dropped and recreated.")

    asyncio.run(async_drop())
    # Delete all files inside migrations/versions but keep the folder
    versions_dir = os.path.join("migrations", "versions")
    if os.path.exists(versions_dir):
        for filename in os.listdir(versions_dir):
            file_path = os.path.join(versions_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
        print(f"Deleted all files in '{versions_dir}'")
    else:
        print(f"Folder '{versions_dir}' not found.")


@app.command()
def dbfresh():
    import typer
    import sys
    import os
    import time
    from pathlib import Path

    """
    Drops all tables, re-runs migrations, and applies all seeders sequentially.
    """
    project_root = Path(__file__).resolve().parent
    manage_py = project_root / "manage.py"

    if not manage_py.exists():
        typer.secho(f"❌ Could not find manage.py at {manage_py}", fg=typer.colors.RED)
        raise typer.Exit(1)

    # 1. Prepare Environment
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root)
    env["FASTAPI_ENV"] = "development"
    env["PYTHONUNBUFFERED"] = "1"  # <--- Crucial: Forces output to print immediately

    # 2. Define the exact python executable to use (avoids path issues)
    py_exec = sys.executable

    commands = [
        [py_exec, str(manage_py), "dropall"],
        [py_exec, str(manage_py), "makemigrations"],
        [py_exec, str(manage_py), "migrate"],
        [py_exec, "-m", "core.security.seeders"],
    ]

    def run_command(cmd: list[str]):
        cmd_str = " ".join(cmd)
        typer.secho(f"\n🚀 Running: {cmd_str}", fg=typer.colors.BLUE, bold=True)

        # Flush current output so the "Running" message appears BEFORE the command starts
        sys.stdout.flush()

        try:
            # subprocess.run waits until the command is totally finished
            subprocess.run(
                cmd,
                cwd=project_root,
                env=env,
                stdout=sys.stdout,  # Connect directly to terminal
                stderr=sys.stderr,  # Connect errors directly to terminal
                check=True,  # Stop immediately if command fails
            )
        except subprocess.CalledProcessError as e:
            typer.secho(f"\n❌ Command failed: {cmd_str}", fg=typer.colors.RED)
            # Flush stderr to ensure we see the error
            sys.stderr.flush()
            raise typer.Exit(code=e.returncode)

        # Allow a tiny pause to let the OS release file locks (helps with SQLite/Windows)
        sys.stdout.flush()
        time.sleep(0.5)

    # --- Execution Start ---

    # 1. Run Core Commands
    for cmd in commands:
        run_command(cmd)

    typer.secho("\n🎉 Core Security Seeders applied successfully!", fg=typer.colors.GREEN)

    # 2. Run App Seeders
    apps_dir = project_root / "apps"
    if apps_dir.exists():
        for app_dir in apps_dir.iterdir():
            if app_dir.is_dir() and (app_dir / "seeders").exists():
                seeder_module = f"apps.{app_dir.name}.seeders"
                typer.echo(f"🌱 Found seeder for: {app_dir.name}")
                run_command([py_exec, "-m", seeder_module])
    else:
        typer.echo("⚠️ No 'apps' directory found — skipping app seeders.")

    typer.secho("\n✅ Database refreshed and all seeders applied successfully!", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()

#!/usr/bin/env python3
"""
Setup script for Harmoniq Django project.
This script helps with initial setup and dependency installation.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False


def check_poetry():
    """Check if Poetry is installed."""
    try:
        subprocess.run(["poetry", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_node():
    """Check if Node.js is installed."""
    try:
        subprocess.run(["node", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def setup_environment():
    """Set up the environment file."""
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file...")
        with open(env_file, "w") as f:
            f.write("""# Django Settings
SECRET_KEY=django-insecure-change-me-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Music API Credentials
SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
TIDAL_CLIENT_ID=
TIDAL_CLIENT_SECRET=

# Development Settings
TAILWIND_APP_NAME=theme
""")
        print("✅ .env file created")
    else:
        print("✅ .env file already exists")


def main():
    """Main setup function."""
    print("🎵 Welcome to Harmoniq Setup!")
    print("=" * 50)
    
    # Check prerequisites
    print("🔍 Checking prerequisites...")
    
    if not check_poetry():
        print("❌ Poetry is not installed. Please install Poetry first:")
        print("   curl -sSL https://install.python-poetry.org | python3 -")
        sys.exit(1)
    
    if not check_node():
        print("❌ Node.js is not installed. Please install Node.js first:")
        print("   https://nodejs.org/")
        sys.exit(1)
    
    print("✅ All prerequisites are installed")
    
    # Install Python dependencies
    if not run_command("poetry install", "Installing Python dependencies"):
        sys.exit(1)
    
    # Set up environment file
    setup_environment()
    
    # Install Tailwind CSS
    if not run_command("poetry run python manage.py tailwind install", "Installing Tailwind CSS"):
        sys.exit(1)
    
    # Build Tailwind CSS
    if not run_command("poetry run python manage.py tailwind build", "Building Tailwind CSS"):
        sys.exit(1)
    
    # Run database migrations
    if not run_command("poetry run python manage.py migrate", "Running database migrations"):
        sys.exit(1)
    
    # Create superuser
    print("👤 Creating superuser...")
    print("Please enter the following information for your admin account:")
    try:
        subprocess.run("poetry run python manage.py createsuperuser", shell=True)
        print("✅ Superuser created successfully")
    except KeyboardInterrupt:
        print("⚠️  Superuser creation cancelled")
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Copy env.example to .env and configure your API keys")
    print("2. Run: poetry run python manage.py runserver")
    print("3. In another terminal, run: poetry run python manage.py tailwind start")
    print("4. Visit http://localhost:8000 to access the application")
    print("5. Visit http://localhost:8000/admin to access the admin interface")


if __name__ == "__main__":
    main()
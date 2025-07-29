#!/usr/bin/env python3
"""
Database initialization script for Harmoniq
"""

from app.db.base import engine, Base
from app.db.models import User, Track, Playlist, PlaylistTrack, Favorite

def init_db():
    """Initialize the database by creating all tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db() 
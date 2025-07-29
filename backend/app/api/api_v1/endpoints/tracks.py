from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.base import get_db
from app.db.models import Track, User
from app.services.auth import get_current_user
from pydantic import BaseModel

router = APIRouter()

class TrackResponse(BaseModel):
    id: int
    tidal_id: str
    title: str
    artist: str
    album: str
    duration: int
    cover_url: Optional[str] = None
    preview_url: Optional[str] = None
    
    class Config:
        from_attributes = True

class TrackCreate(BaseModel):
    tidal_id: str
    title: str
    artist: str
    album: str
    duration: int
    cover_url: Optional[str] = None
    preview_url: Optional[str] = None

@router.get("/", response_model=List[TrackResponse])
def get_tracks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Track)
    
    if search:
        query = query.filter(
            (Track.title.contains(search)) |
            (Track.artist.contains(search)) |
            (Track.album.contains(search))
        )
    
    tracks = query.offset(skip).limit(limit).all()
    return tracks

@router.get("/{track_id}", response_model=TrackResponse)
def get_track(track_id: int, db: Session = Depends(get_db)):
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Track not found"
        )
    return track

@router.post("/", response_model=TrackResponse)
def create_track(track: TrackCreate, db: Session = Depends(get_db)):
    # Check if track already exists
    existing_track = db.query(Track).filter(Track.tidal_id == track.tidal_id).first()
    if existing_track:
        return existing_track
    
    db_track = Track(**track.dict())
    db.add(db_track)
    db.commit()
    db.refresh(db_track)
    return db_track

@router.get("/search/{query}", response_model=List[TrackResponse])
def search_tracks(query: str, db: Session = Depends(get_db)):
    tracks = db.query(Track).filter(
        (Track.title.contains(query)) |
        (Track.artist.contains(query)) |
        (Track.album.contains(query))
    ).all()
    return tracks 
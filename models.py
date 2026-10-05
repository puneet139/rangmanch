from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    play_name: str = Field(index=True)
    reviewer_name: str
    rating: int = Field(ge=1, le=5, description="Rating must be between 1 and 5")
    comment: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)


class ReviewCreate(SQLModel):
    play_name: str = Field(index=True)
    reviewer_name: str
    rating: int = Field(ge=1, le=5, description="Rating must be between 1 and 5")
    comment: Optional[str] = None

class ReviewRead(SQLModel):
    id: int
    play_name: str
    reviewer_name: str
    rating: int
    comment: Optional[str] = None
    created_at: datetime

class ReviewUpdate(SQLModel):
    play_name: Optional[str] = None
    reviewer_name: Optional[str] = None
    rating: Optional[int] = Field(default=None, ge=1, le=5, description="Rating must be between 1 and 5")
    comment: Optional[str] = None
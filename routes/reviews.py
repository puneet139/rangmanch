from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from database import get_session
from models import Review, ReviewCreate, ReviewRead, ReviewUpdate

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/", response_model=ReviewRead)
def create_review(review: ReviewCreate, session:Session = Depends(get_session)):
    """
    Create a new review.
    """
    db_review = Review(**review.model_dump())
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review

@router.get("/", response_model=list[ReviewRead])
def read_reviews(play_name: str | None = Query(None, description="Filter by play names"),
                 skip : int = Query(0, ge=0, description="No of reviews to skip"),
                  limit: int = Query(10, ge=1, le=50, description="No of reviews to return"), 
                  session: Session = Depends(get_session)):
    """
    Retrieve all reviews.
    """
    reviews = select(Review)
    if play_name:
        reviews = reviews.where(func.lower(Review.play_name) == play_name.lower())
    reviews = reviews.offset(skip).limit(limit)
    reviews = session.exec(reviews).all()
    return reviews

@router.get("/average_rating/{play_name}")
def get_average_rating(play_name: str, session: Session = Depends(get_session)):
    """
    Get the average rating for a specific play.
    """
    average_rating = session.exec(
        select(func.avg(Review.rating), func.count(Review.id)).where(func.lower(Review.play_name) == play_name.lower())
    ).one()
    
    if average_rating[0] is None:
        return {"play_name": play_name, "average_rating": None, "message": "No reviews found for this play."}
    
    return {"play_name": play_name, "average_rating": round(average_rating[0], 2)}


@router.get("/review/{review_id}")
def get_review_by_review_id(review_id:int, session : Session = Depends(get_session)):
    review = session.get(Review,review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    print(f"Retrieved review with ID {review_id}: {review}")
    return review

@router.patch("/review/{review_id}", response_model=ReviewRead)
def update_review(review_id:int, review_update: ReviewUpdate, session: Session = Depends(get_session)):
    """
    Update an existing review.
    """
    db_review = session.get(Review, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    review_data = review_update.model_dump(exclude_unset=True)
    print(f"Updating review {review_id} with data: {review_data}")
    for key, value in review_data.items():
        setattr(db_review, key, value)
    
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review
from typing import List, Optional
from pydantic import BaseModel


class RateLimitInfo(BaseModel):
    limit: int
    remaining: int
    reset: int

class Src(BaseModel):
    original: str
    large2x: str
    large: str
    medium: str
    small: str
    portrait: str
    landscape: str
    tiny: str

class Photo(BaseModel):
    id: int
    width: int
    height: int
    url: str
    photographer: str
    photographer_url: str
    photographer_id: int
    avg_color: str
    src: Src
    liked: bool
    alt: str

class Response(BaseModel):
    photos: List[Photo]
    page: int
    per_page: int
    total_results: int
    prev_page: Optional[str] = None
    next_page: Optional[str] = None

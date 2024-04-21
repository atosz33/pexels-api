# PexelsAPI Package Documentation

## Overview

The `PexelsAPI` package provides a convenient way to interact with the Pexels API, allowing you to search for and retrieve photos from the Pexels database. It offers methods for accessing curated collections of photos, searching for photos by keyword, and retrieving individual photos by ID.

## Installation

You can install the package using pip:

```bash
pip install pexels-api
```

## Usage

```python
from pexels_api import PexelsAPI, Color, Locale, PhotoSize

# Initialize the PexelsAPI object with your API key
api = PexelsAPI(authorization_token="your_api_key_here")

# Get curated photos
curated_photos = api.get_curated(page=1, per_page=10)
print(curated_photos)

# Search for photos
search_results = api.search_image(query="nature", page=1, per_page=10, color=Color.GREEN, locale=Locale.EN_US)
print(search_results)
```

## Class: PexelsAPI

### Methods

- `get_curated(page: Optional[int] = 1, per_page: Optional[int] = 15) -> Response`: Retrieves a curated collection of photos from Pexels.
- `search_image(query: str, orientation: Optional[str] = None, size: Optional[PhotoSize] = None, color: Optional[Color] = None, locale: Optional[Locale] = None, page: Optional[int] = 1, per_page: Optional[int] = 15) -> Response`: Searches for photos based on the specified query parameters.
- `get_photo_by_id(photo_id: int) -> Photo`: Retrieves a specific photo by its ID.

### Attributes

- `authorization_token`: Your Pexels API key.
- `headers`: Headers used for making requests.
- `remaining_requests_by_hour`: Number of remaining requests within the current rate limit window.

## Models

### Response

Represents the response object returned by the Pexels API.

- `photos`: List of Photo objects.
- `page`: Current page number.
- `per_page`: Number of results per page.
- `total_results`: Total number of results.
- `prev_page`: URL for the previous page of results (optional).
- `next_page`: URL for the next page of results (optional).

### Photo

Represents a single photo object returned by the Pexels API.

- `id`: Unique identifier for the photo.
- `width`: Width of the photo in pixels.
- `height`: Height of the photo in pixels.
- `url`: URL of the photo on the Pexels website.
- `photographer`: Name of the photographer.
- `photographer_url`: URL of the photographer's profile on Pexels.
- `photographer_id`: Unique identifier for the photographer.
- `avg_color`: Average color of the photo in hexadecimal format.
- `src`: Dictionary containing URLs for different sizes of the photo.
- `liked`: Boolean indicating whether the photo has been liked by the user.
- `alt`: Alternate text for the photo.

### RateLimitInfo

Represents rate limit information extracted from the API response headers.

- `limit`: Maximum number of requests allowed within the current rate limit window.
- `remaining`: Number of requests remaining within the current rate limit window.
- `reset`: Unix timestamp when the rate limit window will reset.


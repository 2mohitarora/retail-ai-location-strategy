import os
import googlemaps
from typing import Dict, Any, List

def search_places(query: str) -> Dict[str, Any]:
    """
    Search for places using Google Maps Places API.
    
    Args:
        query: Search query combining business type and location.
               Example: "fitness studio near Jersey City, New Jersey, US"
               
    Returns:
        dict: A dictionary containing status, results, count, etc.
    """
    api_key = os.environ.get("MAPS_API_KEY")
    if not api_key:
        return {
            "status": "error",
            "error_message": "MAPS_API_KEY environment variable not set.",
            "results": [],
            "count": 0,
        }

    try:
        gmaps = googlemaps.Client(key=api_key)
        result = gmaps.places(query)

        places = []
        for place in result.get("results", []):
            places.append({
                "name": place.get("name", "Unknown"),
                "address": place.get("formatted_address", place.get("vicinity", "N/A")),
                "rating": place.get("rating", 0),
                "user_ratings_total": place.get("user_ratings_total", 0),
                "price_level": place.get("price_level", "N/A"),
                "types": place.get("types", []),
                "business_status": place.get("business_status", "UNKNOWN"),
                "location": {
                    "lat": place.get("geometry", {}).get("location", {}).get("lat"),
                    "lng": place.get("geometry", {}).get("location", {}).get("lng"),
                },
                "place_id": place.get("place_id", ""),
            })

        return {
            "status": "success",
            "results": places,
            "count": len(places),
            "next_page_token": result.get("next_page_token"),
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e),
            "results": [],
            "count": 0,
        }

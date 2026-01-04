---
name: maps-search
description: Provides real-time access to Google Maps business data, allowing the agent to find physical locations, perform competitive market research, and retrieve business details like ratings, addresses, and price levels.
---

# Google Maps Places Search Skill

This skill allows the agent to perform real-world local business discovery and competitive research. It interfaces with the Google Maps Places API to retrieve high-fidelity data about physical locations.

## Usage Guidance
- **When to use:** Use this skill when the user asks for information about local businesses, service providers, or points of interest. It is ideal for "Find [type] in [location]" or "Who are the competitors for [business] in [area]?"
- **When NOT to use:** Do not use this for general web searches that don't involve physical locations or for driving directions/traffic data.
- **Dependency:** This skill requires a valid `MAPS_API_KEY` set in the environment or the tool context state.

## Tool Definitions

### `search_places`
Searches for businesses or locations matching a specific query and returns structured data including ratings and addresses.

**Parameters:**
- `query` (string, required): The search string combining the entity type and the geographical area. 
  - *Best practice:* "Plumbers in Austin, TX" or "Vegan restaurants near Central Park, NY".

**Returns:**
- `status`: "success" or "error"
- `results`: List of objects containing:
    - `name`: Name of the business.
    - `address`: The full physical location.
    - `rating`: User rating (0-5).
    - `user_ratings_total`: Total number of reviews.
    - `price_level`: Price range (1-4).
    - `location`: Dictionary with `lat` and `lng`.
    - `place_id`: Unique Google identifier for the place.
- `count`: Integer representing number of results found.

---

## Instructions for the Agent
1. **Query Construction:** Always attempt to be specific with the location. If the user says "Find gyms," check the current context for a city. If none is found, ask the user for a location before calling the tool.
2. **Key Handling:** If the tool returns an error regarding a missing API key, inform the user that the `MAPS_API_KEY` environment variable needs to be configured.
3. **Data Presentation:** When displaying results, use a clean list or table format. If a business has a high rating ($>4.5$) but few reviews, mention that it is "highly rated but has limited feedback."

## Examples

**User:** "I need to find a good auto repair shop in San Jose."
**Agent Thought:** The user is looking for a local service. I will use `search_places` to find highly-rated repair shops in San Jose, CA.
**Tool Call:** `search_places({"query": "highly rated auto repair shops in San Jose, CA"})`

**User:** "Who are the competitors for a new pizza shop in the 07030 zip code?"
**Agent Thought:** I need to identify existing pizza restaurants in Hoboken (07030) to provide a competitive landscape.
**Tool Call:** `search_places({"query": "pizza restaurants in 07030"})`
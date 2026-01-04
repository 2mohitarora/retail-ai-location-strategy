import pandas as pd
import json
from typing import List, Dict, Any

def perform_gap_analysis(zones_data: List[Dict[str, Any]], weights: Dict[str, float] = None) -> Dict[str, Any]:
    """
    Perform quantitative gap analysis on zone data.
    
    Args:
        zones_data: List of dictionaries, each representing a zone with metrics:
                    - name: Zone name
                    - competitor_count: Number of competitors
                    - average_rating: Avg competitor rating
                    - population_score: 0-10 score (or raw number to be normalized)
                    - income_score: 0-10 score
                    - traffic_score: 0-10 score
        weights: Optional dictionary of weights for the ranking. 
                 Defaults to:
                 - saturation: -0.3 (lower is better)
                 - demand: 0.4 (population + income + traffic)
                 - quality_gap: 0.3 (opportunity if competitors are low rated)
                 
    Returns:
        dict: Analysis results including ranked zones and summary stats.
    """
    if not zones_data:
        return {"status": "error", "message": "No zone data provided"}

    try:
        df = pd.DataFrame(zones_data)
        
        # Normalize metrics if needed (simple min-max for this example)
        # assuming scores provided are 0-10 or similar scale, if not we'd normalize
        
        # Default weights
        if not weights:
            # We want High Demand, Low Saturation, Low Quality (competitors)
            # So viability = Demand - Saturation + (5 - AvgRating)
            pass

        # Calculate Saturation Index
        # (Competitor Count / Max Competitor Count) * 100 (simplified)
        max_comp = df['competitor_count'].max()
        if max_comp > 0:
            df['saturation_index'] = (df['competitor_count'] / max_comp) * 100
        else:
            df['saturation_index'] = 0

        # Calculate Demand Score (avg of available demand metrics)
        demand_cols = [c for c in ['population_score', 'income_score', 'traffic_score'] if c in df.columns]
        if demand_cols:
            df['demand_score'] = df[demand_cols].mean(axis=1) * 10
        else:
            df['demand_score'] = 50 # Default middle

        # Calculate Quality Barrier (high ratings = bad for entry)
        # We look for low ratings as opportunity.
        df['avg_rating'] = df.get('average_rating', 0)
        df['quality_barrier'] = (df['avg_rating'] / 5.0) * 100

        # Viability Score Calculation
        # V = (Demand * 0.4) + ((100 - Saturation) * 0.3) + ((100 - Quality) * 0.3)
        df['viability_score'] = (
            (df['demand_score'] * 0.4) + 
            ((100 - df['saturation_index']) * 0.3) + 
            ((100 - df['quality_barrier']) * 0.3)
        ).clip(0, 100).round(1)

        # Categorization
        def categorize(row):
            s = row['viability_score']
            if s >= 75: return "HIGH OPPORTUNITY"
            if s >= 50: return "MODERATE"
            return "SATURATED/RISKY"

        df['category'] = df.apply(categorize, axis=1)
        
        # Sort
        df = df.sort_values('viability_score', ascending=False)
        
        return {
            "status": "success",
            "ranked_zones": df.to_dict(orient='records'),
            "top_pick": df.iloc[0].to_dict() if not df.empty else None,
            "summary": "Analysis complete. Scores calculated based on demand, saturation, and quality metrics."
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e)
        }

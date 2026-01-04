import os
from google import genai
from google.genai import types

def generate_html_report(report_data: str) -> dict:
    """
    Generate a HTML executive report and save as artifact.

    Args:
        report_data: The strategic report data in a formatted string.
        
    Returns:
        dict: Status and artifact details.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return {"status": "error", "error_message": "GOOGLE_API_KEY not found"}

    try:
        client = genai.Client(api_key=api_key)
        
        prompt = f"""Generate a comprehensive, professional HTML report for a location intelligence analysis.

This report should be in the professional style presentations:
- Multi-slide format using full-screen scrollable sections
- Modern, clean, executive-ready design
- Data-driven visualizations
- Professional color scheme and typography

CRITICAL REQUIREMENTS:

1. STRUCTURE - Create 7 distinct slides (full-screen sections):
   [... Same structure instructions as original ...]
   SLIDE 1: Executive Summary
   SLIDE 2: Top Recommendation
   SLIDE 3: Competition Analysis
   SLIDE 4: Market Characteristics
   SLIDE 5: Alternative Locations
   SLIDE 6: Key Insights
   SLIDE 7: Methodology

2. DESIGN:
   - Use professional consulting color palette (Navy Blue, Green for success, Amber for warning)
   - Modern sans-serif fonts
   - Responsive grid layouts

3. TECHNICAL:
   - Self-contained: ALL CSS embedded in <style> tag
   - No external dependencies
   - Each slide: min-height: 100vh; page-break-after: always;

4. DATA TO INCLUDE:
{report_data}

5. OUTPUT:
   - Generate ONLY the complete HTML code
   - Start with <!DOCTYPE html>
   - End with </html>
   - NO markdown code fences
"""

        response = client.models.generate_content(
            model="gemini-1.5-pro-002", # Or config.PRO_MODEL
            contents=prompt,
            config=types.GenerateContentConfig(temperature=1.0),
        )

        html_code = response.text
        # Cleanup markdown fences
        if html_code.startswith("```"):
            lines = html_code.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            html_code = "\n".join(lines)

        # In Claude Agent SDK, we can't directly "save_artifact" from the tool to the UI easily 
        # without passing the agent/context. 
        # But typically we return the content or a path.
        # For now, we will save to a local file in `artifacts` dir if it exists, or just return the HTML content 
        # and let the Agent/Subagent save it if needed, or better yet, return it and the caller logs it.
        # The user wants "same thing to happen". ADK saves artifact.
        
        # We'll save it locally to a known path that the UI might pick up or the user can find.
        output_path = "executive_report.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_code)

        return {
            "status": "success",
            "message": f"HTML report generated and saved to {output_path}",
            "html_file": output_path,
            "html_length": len(html_code)
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e)
        }

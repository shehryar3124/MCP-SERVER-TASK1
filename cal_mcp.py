import os
import logging
import httpx
from typing import Optional, Dict, Any
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# 1. Load the variables from the .env file
load_dotenv() 

# ---------------------------------------------------------
# Configuration & Logging
# ---------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()] 
)
logger = logging.getLogger("calcom-agent-mcp")

CAL_API_KEY = os.environ.get("CAL_API_KEY") 
BASE_URL = "https://api.cal.com/v2"

# 👈 NEW: Cal.com's extremely specific API versions for each endpoint
API_VERSIONS = {
    "slots": "2024-09-04",
    "bookings": "2026-02-25",
    "event_types": "2024-06-14",
}

# Initialize the FastMCP Server
mcp = FastMCP("CalCom-Voice-Agent")

# ---------------------------------------------------------
# Core API Client
# ---------------------------------------------------------
async def fetch_cal_api(method: str, endpoint: str, api_version: str, params: Optional[Dict] = None, json_body: Optional[Dict] = None) -> Dict[str, Any]:
    """A centralized, robust async HTTP client for the Cal.com v2 API."""
    if not CAL_API_KEY:
        raise RuntimeError("❌ CAL_API_KEY environment variable is missing.")

    headers = {
        "Authorization": f"Bearer {CAL_API_KEY}",
        "cal-api-version": api_version,  # 👈 Now injects the exact required version
        "Content-Type": "application/json"
    }

    if params:
        params = {k: v for k, v in params.items() if v is not None}

    url = f"{BASE_URL}{endpoint}"
    logger.info(f"📡 API Request: {method} {endpoint}")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json_body,
                timeout=20.0
            )
            response.raise_for_status()
            return response.json() 
            
        except httpx.HTTPStatusError as e:
            # Safely handle JSON decode errors if Cal.com returns blank 404s
            error_data = e.response.json() if e.response.text else {}
            err_msg = error_data.get("message", "Unknown API Error")
            logger.error(f"⚠️ Cal.com Error ({e.response.status_code}): {err_msg}")
            return {"error": True, "message": err_msg, "status_code": e.response.status_code}
        except Exception as e:
            logger.error(f"❌ Network Error: {str(e)}")
            return {"error": True, "message": str(e)}

# ---------------------------------------------------------
# Tools
# ---------------------------------------------------------
@mcp.tool()
async def list_event_types() -> dict:
    """Retrieve all available event types for the authenticated Cal.com account."""
    return await fetch_cal_api("GET", "/event-types", API_VERSIONS["event_types"])

@mcp.tool()
async def get_availability(event_type_id: int, start_date: str, end_date: str) -> dict:
    """Check available time slots for a specific Cal.com event type."""
    return await fetch_cal_api("GET", "/slots", API_VERSIONS["slots"], params={"eventTypeId": event_type_id, "startTime": start_date, "endTime": end_date})

@mcp.tool()
async def create_booking(event_type_id: int, start_time: str, name: str, email: str, time_zone: str = "UTC") -> dict:
    """Schedule a new meeting on the calendar."""
    payload = {
        "eventTypeId": event_type_id,
        "start": start_time,
        "attendee": {
            "name": name,
            "email": email,
            "timeZone": time_zone
        }
    }
    return await fetch_cal_api("POST", "/bookings", API_VERSIONS["bookings"], json_body=payload)

@mcp.tool()
async def cancel_booking(booking_uid: str, reason: str = "User requested cancellation via Voice Agent") -> dict:
    """Cancel an existing booking using its unique string ID."""
    return await fetch_cal_api("POST", f"/bookings/{booking_uid}/cancel", API_VERSIONS["bookings"], json_body={"cancellationReason": reason})

@mcp.tool()
async def reschedule_booking(booking_uid: str, new_start_time: str, reason: str = "User requested reschedule via Voice Agent") -> dict:
    """Move an existing booking to a new time slot."""
    return await fetch_cal_api("POST", f"/bookings/{booking_uid}/reschedule", API_VERSIONS["bookings"], json_body={"start": new_start_time, "reschedulingReason": reason})

# ---------------------------------------------------------
# Server Entry Point
# ---------------------------------------------------------
if __name__ == "__main__":
    logger.info("🚀 Starting Custom Cal.com MCP Server...")
    mcp.run(transport="stdio")
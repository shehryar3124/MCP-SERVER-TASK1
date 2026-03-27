from app.tools.list_event_types import list_event_types
from fastapi import FastAPI
from app.tools.get_availability import get_availability
from app.tools.create_booking import create_booking
from app.tools.cancel_booking import cancel_booking
from app.tools.reschedule_booking import reschedule_booking
from app.tools.schema import tools


app = FastAPI()



@app.get("/")
def root():
    return {"message": "Cal.com MCP Server Running 🚀"}

# 🔥 MCP TOOL ENDPOINT
@app.post("/tools/get_availability")
def availability():
    return get_availability()

@app.post("/tools/create_booking")
def booking():
    return create_booking()

@app.post("/tools/list_event_types")
def event_types():
    return list_event_types()

@app.post("/tools/cancel_booking")
def cancel():
    return cancel_booking()

@app.post("/tools/reschedule_booking")
def reschedule():
    return reschedule_booking()

@app.get("/tools")
def get_tools():
    return tools

@app.middleware("http")
async def log_requests(request, call_next):
    print(f"{request.method} {request.url}")
    response = await call_next(request)
    return response
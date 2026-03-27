from app.utils.calcom import get

def list_event_types():
    data = get("/event-types")

    import json
    print(json.dumps(data, indent=2))  # 🔥 full debug

    return data
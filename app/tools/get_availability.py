from app.utils.calcom import get

def get_availability():
    try:
        username = "sheheryar-nadir-euwiwu"
        event_type = "30min"

        path = f"/availability?username={username}&eventTypeSlug={event_type}"

        data = get(path)
        return data

    except Exception as e:
        return {"error": str(e)}
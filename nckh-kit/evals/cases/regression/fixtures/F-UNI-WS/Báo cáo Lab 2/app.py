def authorize(caller, owner):
    return caller == owner

def conversion(count, total):
    # Deliberate regression fixture: denominator is ignored.
    return count * 100

def validate_request(payload):
    return {"ok": True, "value": payload.get("count")}

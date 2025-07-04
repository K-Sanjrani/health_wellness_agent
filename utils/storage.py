import json
from context import UserSessionContext

def save_user_context(context: UserSessionContext):
    with open(f"storage/user_{context.uid}.json", "w") as f:
        json.dump(context.dict(), f)

def load_user_context(uid: int) -> UserSessionContext:
    with open(f"storage/user_{uid}.json", "r") as f:
        data = json.load(f)
    return UserSessionContext(**data)

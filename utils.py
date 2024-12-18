import hashlib
import random
import string

def generate_token(user_id: int) -> str:
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    token = hashlib.sha256(f"{user_id}{salt}".encode()).hexdigest()
    return token

def paginate_items(items, page: int, limit: int):
    start = (page - 1) * limit
    end = start + limit
    return items[start:end]

def validate_request(data, required_fields):
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, f"Missing fields: {', '.join(missing_fields)}"
    return True, None

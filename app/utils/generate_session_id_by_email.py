import uuid

def generate_session_id_by_email(email: str) -> str:
    """Convert email to UUIDv5 for consistent session mapping."""
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, email))


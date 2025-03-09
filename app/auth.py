import uuid
import hashlib
import secrets
from datetime import datetime, timedelta
from fastapi import HTTPException, Cookie, status
from fastapi.security import HTTPBearer
from typing import Optional, Tuple

from .database import get_db

security = HTTPBearer()


# Password hashing
def hash_password(password: str) -> str:
    """Hash a password for safe storage."""
    salt = secrets.token_hex(16)
    hash_obj = hashlib.sha256(f"{password}{salt}".encode())
    return f"{salt}:{hash_obj.hexdigest()}"


def verify_password(stored_password: str, provided_password: str) -> bool:
    """Verify a password against a stored hash."""
    salt, stored_hash = stored_password.split(":", 1)
    hash_obj = hashlib.sha256(f"{provided_password}{salt}".encode())
    return secrets.compare_digest(hash_obj.hexdigest(), stored_hash)


# Session management
async def create_session(user_id: str, role: str):
    """Create a new user session."""
    db = get_db()
    session_id = str(uuid.uuid4())
    expiry = datetime.utcnow() + timedelta(hours=24)

    await db.sessions.insert_one(
        {"session_id": session_id, "user_id": user_id, "role": role, "expiry": expiry}
    )

    return session_id


async def validate_session(
    session_id: Optional[str] = None,
) -> Tuple[bool, Optional[str], Optional[str]]:
    """Validate a session and return user_id and role if valid."""
    if not session_id:
        return False, None, None

    db = get_db()
    session = await db.sessions.find_one({"session_id": session_id})

    if not session:
        return False, None, None

    if session["expiry"] < datetime.utcnow():
        await db.sessions.delete_one({"session_id": session_id})
        return False, None, None

    return True, session["user_id"], session["role"]


# Authentication dependencies
async def get_current_user(session: Optional[str] = Cookie(None)) -> Tuple[str, str]:
    """Get current authenticated user from session cookie."""
    valid, user_id, role = await validate_session(session)
    if not valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        )
    return user_id, role


async def get_admin_user(session: Optional[str] = Cookie(None)) -> Tuple[str, str]:
    """Get current authenticated admin user."""
    valid, user_id, role = await validate_session(session)
    if not valid or role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return user_id, role


async def get_regular_user(session: Optional[str] = Cookie(None)) -> Tuple[str, str]:
    """Get current authenticated regular user."""
    valid, user_id, role = await validate_session(session)
    if not valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    return user_id, role

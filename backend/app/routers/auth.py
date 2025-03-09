from fastapi import APIRouter, HTTPException, Response, Cookie
from typing import Optional

from ..database import get_db
from ..auth import hash_password, verify_password, create_session, validate_session
from ..models.user import UserRegister, UserLogin, UsernameCheck

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register")
async def register(user: UserRegister):
    db = get_db()

    # Check if username already exists
    existing_user = await db.users.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Create new user with hashed password
    new_user = {
        "username": user.username,
        "password": hash_password(user.password),
        "role": "user",  # Default role is user
        "budget": 100,  # Default budget
        "team": {},  # Empty team
    }

    await db.users.insert_one(new_user)
    return {"success": True}


@router.post("/validate-session")
async def validate_user_session(session: Optional[str] = Cookie(None)):
    valid, user_id, role = await validate_session(session)
    return {"success": valid, "role": role if valid else None}


@router.post("/validate-username")
async def validate_username(username_check: UsernameCheck):
    db = get_db()

    # Validate username length
    if len(username_check.username) < 8:
        return {"success": True, "availability": False}

    # Check if username exists in database
    existing_user = await db.users.find_one({"username": username_check.username})
    return {"success": True, "availability": not bool(existing_user)}


@router.post("/login")
async def login(user: UserLogin, response: Response):
    db = get_db()

    # Find user by username
    db_user = await db.users.find_one({"username": user.username})
    if not db_user or not verify_password(db_user["password"], user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Create session
    session_id = await create_session(str(db_user["_id"]), db_user["role"])

    # Set session cookie
    response.set_cookie(
        key="session",
        value=session_id,
        httponly=True,
        max_age=86400,  # 24 hours
        samesite="lax",
    )

    return {"success": True, "role": db_user["role"]}


@router.post("/logout")
async def logout(response: Response, session: Optional[str] = Cookie(None)):
    db = get_db()

    # Delete session from database if it exists
    if session:
        await db.sessions.delete_one({"session_id": session})

    # Clear session cookie
    response.delete_cookie(key="session")

    return {"success": True}

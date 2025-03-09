from pydantic import BaseModel
from typing import Dict, Optional, List

from .player import PlayerDetail


class Team(BaseModel):
    success: bool
    username: str
    players: Dict[str, Optional[PlayerDetail]]
    total_points: Optional[int] = None


class TeamPlayerRequest(BaseModel):
    playerId: int


class BudgetResponse(BaseModel):
    success: bool
    total: int
    used: int
    remaining: int


class LeaderboardUser(BaseModel):
    username: str
    points: int


class LeaderboardResponse(BaseModel):
    success: bool
    users: List[LeaderboardUser]


class ChatbotRequest(BaseModel):
    query: str


class ChatbotResponse(BaseModel):
    success: bool
    response: str
    suggestion: Optional[List[PlayerDetail]] = None

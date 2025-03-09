from pydantic import BaseModel
from typing import List, Optional


class PlayerBase(BaseModel):
    id: int
    name: str
    university: str
    budget: int
    category: str
    value: int


class PlayerDetail(PlayerBase):
    bat_strike_rate: float
    bow_strike_rate: float
    bat_avg: float
    econ: float


class PlayerCreate(BaseModel):
    name: str
    university: str
    role: str
    runs: int
    wickets: int


class PlayerUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    university: Optional[str] = None
    role: Optional[str] = None
    runs: Optional[int] = None
    wickets: Optional[int] = None


class PlayerDelete(BaseModel):
    id: int


class PlayerRequest(BaseModel):
    id: int


class PlayerArrayResponse(BaseModel):
    success: bool
    player_array: List[PlayerBase]


class PlayerResponse(BaseModel):
    success: bool
    player: PlayerDetail


class TournamentSummary(BaseModel):
    success: bool
    total_runs: int
    total_wickets: int
    highest_runs: PlayerDetail
    highest_wickets: PlayerDetail

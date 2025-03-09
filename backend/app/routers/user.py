from fastapi import APIRouter, HTTPException, Depends

from ..auth import get_regular_user
from ..database import get_db
from ..models.player import (
    PlayerBase,
    PlayerDetail,
    PlayerRequest,
    PlayerArrayResponse,
    PlayerResponse,
)
from ..models.team import (
    Team,
    TeamPlayerRequest,
    BudgetResponse,
    LeaderboardResponse,
    LeaderboardUser,
)

router = APIRouter(tags=["user"])


@router.get("/players", response_model=PlayerArrayResponse)
async def get_players(user_data: tuple = Depends(get_regular_user)):
    """Get all players (user access)"""
    user_id, role = user_data
    db = get_db()

    players = []
    cursor = db.players.find({})

    async for doc in cursor:
        player = PlayerBase(
            id=doc["id"],
            name=doc["name"],
            university=doc["university"],
            budget=doc["budget"],
            category=doc["category"],
            value=doc["value"],
        )
        players.append(player)

    return {"success": True, "player_array": players}


@router.post("/players", response_model=PlayerResponse)
async def get_player_detail(
    player_req: PlayerRequest, user_data: tuple = Depends(get_regular_user)
):
    """Get player detail (user access)"""
    user_id, role = user_data
    db = get_db()

    player_doc = await db.players.find_one({"id": player_req.id})
    if not player_doc:
        raise HTTPException(status_code=404, detail="Player not found")

    player = PlayerDetail(
        id=player_doc["id"],
        name=player_doc["name"],
        university=player_doc["university"],
        budget=player_doc["budget"],
        category=player_doc["category"],
        value=player_doc["value"],
        bat_strike_rate=player_doc["bat_strike_rate"],
        bow_strike_rate=player_doc["bow_strike_rate"],
        bat_avg=player_doc["bat_avg"],
        econ=player_doc["econ"],
    )

    return {"success": True, "player": player}


@router.get("/team", response_model=Team)
async def get_team(user_data: tuple = Depends(get_regular_user)):
    """Get user's current team"""
    user_id, role = user_data
    db = get_db()

    user = await db.users.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    team_data = user.get("team", {})
    players_dict = {}
    total_points = 0

    # Convert team data to dictionary of player objects
    for position, player_id in team_data.items():
        player_doc = await db.players.find_one({"id": player_id})
        if player_doc:
            player = PlayerDetail(
                id=player_doc["id"],
                name=player_doc["name"],
                university=player_doc["university"],
                budget=player_doc["budget"],
                category=player_doc["category"],
                value=player_doc["value"],
                bat_strike_rate=player_doc["bat_strike_rate"],
                bow_strike_rate=player_doc["bow_strike_rate"],
                bat_avg=player_doc["bat_avg"],
                econ=player_doc["econ"],
            )
            players_dict[position] = player
            total_points += player_doc["value"]

    # Fill in null values for missing positions
    for i in range(1, 12):
        pos = str(i)
        if pos not in players_dict:
            players_dict[pos] = None

    # Only include total_points if team is complete
    result = {"success": True, "username": user["username"], "players": players_dict}

    if len(team_data) == 11:
        result["total_points"] = total_points

    return result


@router.post("/team", response_model=Team)
async def add_player_to_team(
    team_req: TeamPlayerRequest, user_data: tuple = Depends(get_regular_user)
):
    """Add player to team"""
    user_id, role = user_data
    db = get_db()

    # Get user and check if exists
    user = await db.users.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get player and check if exists
    player = await db.players.find_one({"id": team_req.playerId})
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Get current team
    team_data = user.get("team", {})

    # Check team size limit
    if len(team_data) >= 11:
        raise HTTPException(
            status_code=400, detail="Team size limit reached (11 players)"
        )

    # Calculate current budget used
    current_budget_used = 0
    for player_id in team_data.values():
        player_doc = await db.players.find_one({"id": player_id})
        if player_doc:
            current_budget_used += player_doc["budget"]

    # Check budget
    if current_budget_used + player["budget"] > user.get("budget", 100):
        raise HTTPException(status_code=400, detail="Insufficient budget")

    # Find next available position
    next_position = str(len(team_data) + 1)

    # Add player to team
    team_data[next_position] = team_req.playerId
    await db.users.update_one({"_id": user_id}, {"$set": {"team": team_data}})

    # Get updated team for response
    players_dict = {}
    total_points = 0

    for position, player_id in team_data.items():
        player_doc = await db.players.find_one({"id": player_id})
        if player_doc:
            player_detail = PlayerDetail(
                id=player_doc["id"],
                name=player_doc["name"],
                university=player_doc["university"],
                budget=player_doc["budget"],
                category=player_doc["category"],
                value=player_doc["value"],
                bat_strike_rate=player_doc["bat_strike_rate"],
                bow_strike_rate=player_doc["bow_strike_rate"],
                bat_avg=player_doc["bat_avg"],
                econ=player_doc["econ"],
            )
            players_dict[position] = player_detail
            total_points += player_doc["value"]

    # Fill in null values for missing positions
    for i in range(1, 12):
        pos = str(i)
        if pos not in players_dict:
            players_dict[pos] = None

    # Only include total_points if team is complete
    result = {"success": True, "username": user["username"], "players": players_dict}

    if len(team_data) == 11:
        result["total_points"] = total_points

    return result


@router.delete("/team", response_model=Team)
async def remove_player_from_team(
    team_req: TeamPlayerRequest, user_data: tuple = Depends(get_regular_user)
):
    """Remove player from team"""
    user_id, role = user_data
    db = get_db()

    # Get user and check if exists
    user = await db.users.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get current team
    team_data = user.get("team", {})

    # Check if player is in team
    player_position = None
    for position, player_id in team_data.items():
        if player_id == team_req.playerId:
            player_position = position
            break

    if player_position is None:
        raise HTTPException(status_code=404, detail="Player not found in team")

    # Remove player from team
    del team_data[player_position]

    # Reorder positions to ensure consecutive numbering
    new_team_data = {}
    position_index = 1

    for _, player_id in sorted(team_data.items(), key=lambda x: int(x[0])):
        new_team_data[str(position_index)] = player_id
        position_index += 1

    # Update user's team
    await db.users.update_one({"_id": user_id}, {"$set": {"team": new_team_data}})

    # Get updated team for response
    players_dict = {}
    total_points = 0

    for position, player_id in new_team_data.items():
        player_doc = await db.players.find_one({"id": player_id})
        if player_doc:
            player_detail = PlayerDetail(
                id=player_doc["id"],
                name=player_doc["name"],
                university=player_doc["university"],
                budget=player_doc["budget"],
                category=player_doc["category"],
                value=player_doc["value"],
                bat_strike_rate=player_doc["bat_strike_rate"],
                bow_strike_rate=player_doc["bow_strike_rate"],
                bat_avg=player_doc["bat_avg"],
                econ=player_doc["econ"],
            )
            players_dict[position] = player_detail
            total_points += player_doc["value"]

    # Fill in null values for missing positions
    for i in range(1, 12):
        pos = str(i)
        if pos not in players_dict:
            players_dict[pos] = None

    # Only include total_points if team is complete
    result = {"success": True, "username": user["username"], "players": players_dict}

    if len(new_team_data) == 11:
        result["total_points"] = total_points

    return result


@router.get("/budget", response_model=BudgetResponse)
async def get_budget(user_data: tuple = Depends(get_regular_user)):
    """Get user's budget information"""
    user_id, role = user_data
    db = get_db()

    user = await db.users.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    total_budget = user.get("budget", 100)
    team_data = user.get("team", {})

    # Calculate used budget
    used_budget = 0
    for player_id in team_data.values():
        player_doc = await db.players.find_one({"id": player_id})
        if player_doc:
            used_budget += player_doc["budget"]

    return {
        "success": True,
        "total": total_budget,
        "used": used_budget,
        "remaining": total_budget - used_budget,
    }


@router.get("/leaderboard", response_model=LeaderboardResponse)
async def get_leaderboard(user_data: tuple = Depends(get_regular_user)):
    """Get user leaderboard"""
    user_id, role = user_data
    db = get_db()

    users = []

    # Get all users with their teams
    cursor = db.users.find({})

    async for user in cursor:
        team = user.get("team", {})

        # Only include users with complete teams (11 players)
        if len(team) == 11:
            # Calculate total team points
            points = 0
            for player_id in team.values():
                player = await db.players.find_one({"id": player_id})
                if player:
                    points += player.get("value", 0)

            users.append(LeaderboardUser(username=user["username"], points=points))

    # Sort users by points (descending)
    users.sort(key=lambda x: x.points, reverse=True)

    return {"success": True, "users": users}

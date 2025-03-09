from fastapi import APIRouter, HTTPException, Depends

from ..auth import get_admin_user
from ..database import get_db
from ..models.player import (
    PlayerBase,
    PlayerDetail,
    PlayerCreate,
    PlayerUpdate,
    PlayerDelete,
    PlayerRequest,
    PlayerArrayResponse,
    PlayerResponse,
    TournamentSummary,
)
from ..models.team import LeaderboardResponse, LeaderboardUser

router = APIRouter(tags=["admin"])


@router.get("/players", response_model=PlayerArrayResponse)
async def get_players(user_data: tuple = Depends(get_admin_user)):
    """Get all players (admin access)"""
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
    player_req: PlayerRequest, user_data: tuple = Depends(get_admin_user)
):
    """Get player detail (admin access)"""
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


@router.put("/players")
async def create_player(
    player: PlayerCreate, user_data: tuple = Depends(get_admin_user)
):
    """Create new player (admin access)"""
    user_id, role = user_data
    db = get_db()

    # Generate player ID
    last_player = await db.players.find_one(sort=[("id", -1)])
    new_id = 1 if not last_player else last_player["id"] + 1

    # Calculate player value based on runs and wickets
    value = player.runs // 10 + player.wickets * 5

    # Calculate stats
    matches = max(1, (player.runs // 25) + (player.wickets // 2))  # Estimate matches
    bat_strike_rate = 100 * (
        player.runs / max(1, matches * 20)
    )  # Estimated balls faced
    bow_strike_rate = 6 * (
        player.wickets / max(1, matches * 24)
    )  # Estimated balls bowled
    bat_avg = player.runs / max(1, matches)
    econ = 6 * (player.runs / max(1, matches * 4))  # Estimated overs bowled

    # Set budget based on value
    if value > 100:
        budget = 15
    elif value > 75:
        budget = 12
    elif value > 50:
        budget = 10
    elif value > 25:
        budget = 8
    else:
        budget = 5

    # Create new player
    new_player = {
        "id": new_id,
        "name": player.name,
        "university": player.university,
        "category": player.role,
        "budget": budget,
        "value": value,
        "runs": player.runs,
        "wickets": player.wickets,
        "bat_strike_rate": bat_strike_rate,
        "bow_strike_rate": bow_strike_rate,
        "bat_avg": bat_avg,
        "econ": econ,
    }

    await db.players.insert_one(new_player)

    return {"success": True}


@router.patch("/players", response_model=PlayerResponse)
async def update_player(
    player: PlayerUpdate, user_data: tuple = Depends(get_admin_user)
):
    """Update player (admin access)"""
    user_id, role = user_data
    db = get_db()

    # Get existing player
    existing_player = await db.players.find_one({"id": player.id})
    if not existing_player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Update fields
    update_data = {}
    if player.name:
        update_data["name"] = player.name
    if player.university:
        update_data["university"] = player.university
    if player.role:
        update_data["category"] = player.role

    # Update runs and recalculate stats if provided
    if player.runs is not None:
        update_data["runs"] = player.runs

        # Recalculate stats
        runs = player.runs
        wickets = existing_player["wickets"]
        if player.wickets is not None:
            wickets = player.wickets
            update_data["wickets"] = wickets

        # Recalculate value
        value = runs // 10 + wickets * 5
        update_data["value"] = value

        # Recalculate budget based on new value
        if value > 100:
            update_data["budget"] = 15
        elif value > 75:
            update_data["budget"] = 12
        elif value > 50:
            update_data["budget"] = 10
        elif value > 25:
            update_data["budget"] = 8
        else:
            update_data["budget"] = 5

        # Recalculate other stats
        matches = max(1, (runs // 25) + (wickets // 2))
        update_data["bat_strike_rate"] = 100 * (runs / max(1, matches * 20))
        update_data["bow_strike_rate"] = 6 * (wickets / max(1, matches * 24))
        update_data["bat_avg"] = runs / max(1, matches)
        update_data["econ"] = 6 * (runs / max(1, matches * 4))

    # Update wickets if provided but runs not provided
    elif player.wickets is not None:
        update_data["wickets"] = player.wickets

        # Recalculate stats
        wickets = player.wickets
        runs = existing_player["runs"]

        # Recalculate value
        value = runs // 10 + wickets * 5
        update_data["value"] = value

        # Recalculate budget based on new value
        if value > 100:
            update_data["budget"] = 15
        elif value > 75:
            update_data["budget"] = 12
        elif value > 50:
            update_data["budget"] = 10
        elif value > 25:
            update_data["budget"] = 8
        else:
            update_data["budget"] = 5

        # Recalculate other stats
        matches = max(1, (runs // 25) + (wickets // 2))
        update_data["bat_strike_rate"] = 100 * (runs / max(1, matches * 20))
        update_data["bow_strike_rate"] = 6 * (wickets / max(1, matches * 24))
        update_data["bat_avg"] = runs / max(1, matches)
        update_data["econ"] = 6 * (runs / max(1, matches * 4))

    # Update the player
    if update_data:
        await db.players.update_one({"id": player.id}, {"$set": update_data})

    # Get the updated player
    updated_player = await db.players.find_one({"id": player.id})

    player_detail = PlayerDetail(
        id=updated_player["id"],
        name=updated_player["name"],
        university=updated_player["university"],
        budget=updated_player["budget"],
        category=updated_player["category"],
        value=updated_player["value"],
        bat_strike_rate=updated_player["bat_strike_rate"],
        bow_strike_rate=updated_player["bow_strike_rate"],
        bat_avg=updated_player["bat_avg"],
        econ=updated_player["econ"],
    )

    return {"success": True, "player": player_detail}


@router.delete("/players")
async def delete_player(
    player: PlayerDelete, user_data: tuple = Depends(get_admin_user)
):
    """Delete player (admin access)"""
    user_id, role = user_data
    db = get_db()

    # Check if player exists
    existing_player = await db.players.find_one({"id": player.id})
    if not existing_player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Delete the player
    await db.players.delete_one({"id": player.id})

    # Update all user teams that have this player
    await db.users.update_many(
        {f"team.{player.id}": {"$exists": True}}, {"$unset": {f"team.{player.id}": ""}}
    )

    return {"success": True}


@router.get("/summary", response_model=TournamentSummary)
async def get_tournament_summary(user_data: tuple = Depends(get_admin_user)):
    """Get tournament summary (admin access)"""
    user_id, role = user_data
    db = get_db()

    # Calculate totals
    total_runs = 0
    total_wickets = 0
    highest_runs_player = None
    highest_wickets_player = None
    highest_runs = 0
    highest_wickets = 0

    cursor = db.players.find({})

    async for player in cursor:
        total_runs += player.get("runs", 0)
        total_wickets += player.get("wickets", 0)

        # Track highest runs
        if player.get("runs", 0) > highest_runs:
            highest_runs = player.get("runs", 0)
            highest_runs_player = player

        # Track highest wickets
        if player.get("wickets", 0) > highest_wickets:
            highest_wickets = player.get("wickets", 0)
            highest_wickets_player = player

    # Convert highest_runs_player to PlayerDetail
    highest_runs_detail = PlayerDetail(
        id=highest_runs_player["id"],
        name=highest_runs_player["name"],
        university=highest_runs_player["university"],
        budget=highest_runs_player["budget"],
        category=highest_runs_player["category"],
        value=highest_runs_player["value"],
        bat_strike_rate=highest_runs_player["bat_strike_rate"],
        bow_strike_rate=highest_runs_player["bow_strike_rate"],
        bat_avg=highest_runs_player["bat_avg"],
        econ=highest_runs_player["econ"],
    )

    # Convert highest_wickets_player to PlayerDetail
    highest_wickets_detail = PlayerDetail(
        id=highest_wickets_player["id"],
        name=highest_wickets_player["name"],
        university=highest_wickets_player["university"],
        budget=highest_wickets_player["budget"],
        category=highest_wickets_player["category"],
        value=highest_wickets_player["value"],
        bat_strike_rate=highest_wickets_player["bat_strike_rate"],
        bow_strike_rate=highest_wickets_player["bow_strike_rate"],
        bat_avg=highest_wickets_player["bat_avg"],
        econ=highest_wickets_player["econ"],
    )

    return {
        "success": True,
        "total_runs": total_runs,
        "total_wickets": total_wickets,
        "highest_runs": highest_runs_detail,
        "highest_wickets": highest_wickets_detail,
    }


@router.get("/leaderboard", response_model=LeaderboardResponse)
async def get_admin_leaderboard(user_data: tuple = Depends(get_admin_user)):
    """Get leaderboard (admin access)"""
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

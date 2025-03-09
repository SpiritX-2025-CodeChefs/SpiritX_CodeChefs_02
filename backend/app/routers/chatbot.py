from fastapi import APIRouter, Depends, HTTPException

from ..auth import get_regular_user
from ..database import get_db
from ..models.team import ChatbotRequest, ChatbotResponse
from ..models.player import PlayerDetail
from ..utils import get_openai_response, suggest_players

router = APIRouter(tags=["chatbot"])


@router.post("/chatbot", response_model=ChatbotResponse)
async def chat_with_ai(
    query: ChatbotRequest, user_data: tuple = Depends(get_regular_user)
):
    """Chat with AI assistant for cricket fantasy advice"""
    user_id, role = user_data
    db = get_db()

    if not query.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # Get user information
    user = await db.users.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get user's current team
    team = user.get("team", {})

    # Get all players from the database for context
    players = []
    async for player_doc in db.players.find({}):
        player = {
            "id": player_doc["id"],
            "name": player_doc["name"],
            "university": player_doc["university"],
            "category": player_doc["category"],
            "budget": player_doc["budget"],
            "value": player_doc["value"],
            "bat_strike_rate": player_doc["bat_strike_rate"],
            "bow_strike_rate": player_doc["bow_strike_rate"],
            "bat_avg": player_doc["bat_avg"],
            "econ": player_doc["econ"],
        }
        players.append(player)

    # Get remaining budget
    total_budget = user.get("budget", 100)
    used_budget = 0
    for player_id in team.values():
        player_doc = await db.players.find_one({"id": player_id})
        if player_doc:
            used_budget += player_doc["budget"]
    remaining_budget = total_budget - used_budget

    # Analyze query intent
    user_query = query.query.lower()

    suggested_players = None
    response_text = ""

    if "suggest" in user_query or "recommend" in user_query or "best" in user_query:
        # Get player suggestions based on team composition and budget
        suggested_players, response_text = await suggest_players(
            user_query, players, team, remaining_budget
        )
    else:
        # Get general response from OpenAI
        response_text = await get_openai_response(
            user_query, players, team, remaining_budget
        )

    # Format suggested players to match the PlayerDetail model
    formatted_suggestions = None
    if suggested_players:
        formatted_suggestions = []
        for player in suggested_players:
            formatted_player = PlayerDetail(
                id=player["id"],
                name=player["name"],
                university=player["university"],
                budget=player["budget"],
                category=player["category"],
                value=player["value"],
                bat_strike_rate=player["bat_strike_rate"],
                bow_strike_rate=player["bow_strike_rate"],
                bat_avg=player["bat_avg"],
                econ=player["econ"],
            )
            formatted_suggestions.append(formatted_player)

    return {
        "success": True,
        "response": response_text,
        "suggestion": formatted_suggestions,
    }

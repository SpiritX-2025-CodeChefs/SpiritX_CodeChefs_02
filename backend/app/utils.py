import os
from typing import Dict, List, Optional, Tuple, Any
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
# Initialize OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def get_openai_response(
    query: str,
    players: List[Dict[str, Any]],
    team: Dict[str, int],
    remaining_budget: int,
) -> str:
    """
    Get a response from OpenAI based on user query about cricket fantasy.

    Args:
        query: User's question
        players: List of all players in the system
        team: Current user's team (player IDs by position)
        remaining_budget: User's remaining budget

    Returns:
        Response text from AI
    """
    # Create a context for the AI with relevant information
    # Don't include player values in the context to avoid revealing points
    player_context = "\n".join(
        [
            f"Player {p['id']}: {p['name']} ({p['university']}, {p['category']}) - "
            f"Budget: {p['budget']}, "
            f"Batting SR: {p['bat_strike_rate']:.2f}, "
            f"Bowling SR: {p['bow_strike_rate']:.2f}, "
            f"Batting Avg: {p['bat_avg']:.2f}, "
            f"Economy: {p['econ']:.2f}"
            for p in players[:20]  # Limit context size by including only 20 players
        ]
    )

    # Get team player information
    team_info = []
    for position, player_id in team.items():
        for player in players:
            if player["id"] == player_id:
                team_info.append(
                    f"Position {position}: {player['name']} ({player['category']})"
                )
                break

    team_context = "\n".join(team_info) if team_info else "No players in team yet."

    system_prompt = f"""
    You are Spiriter, a cricket fantasy league assistant. Help users build their fantasy cricket team.
    
    Current team information:
    {team_context}
    
    Remaining budget: {remaining_budget}
    
    Important rules:
    1. NEVER reveal player point values to users
    2. Maximum team size is 11 players
    3. Users must stay within their budget
    4. Be helpful and give cricket-specific advice
    
    Some available players (but don't limit to just these):
    {player_context}
    """

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
            ],
            max_tokens=500,
            temperature=0.7,
        )

        return response.choices[0].message.content

    except Exception as e:
        # Fallback response in case of API issues
        return f"I'm sorry, I couldn't process your request at the moment. Please try again later. (Error: {str(e)})"


async def suggest_players(
    query: str,
    all_players: List[Dict[str, Any]],
    current_team: Dict[str, int],
    remaining_budget: int,
) -> Tuple[Optional[List[Dict[str, Any]]], str]:
    """
    Suggest players based on user query, team composition, and budget.

    Args:
        query: User's question
        all_players: List of all players in the system
        current_team: Current user's team (player IDs by position)
        remaining_budget: User's remaining budget

    Returns:
        Tuple of (suggested players list, response text)
    """
    # Extract query intent
    looking_for_batters = any(
        term in query.lower() for term in ["bat", "batter", "batsman", "batting"]
    )
    looking_for_bowlers = any(
        term in query.lower() for term in ["bowl", "bowler", "bowling"]
    )
    looking_for_all_rounders = any(
        term in query.lower()
        for term in ["all round", "all-round", "allround", "all rounder"]
    )

    # Default to all player types if not specified
    if not any([looking_for_batters, looking_for_bowlers, looking_for_all_rounders]):
        looking_for_batters = looking_for_bowlers = looking_for_all_rounders = True

    # Filter out players already in team
    team_player_ids = set(current_team.values())
    available_players = [p for p in all_players if p["id"] not in team_player_ids]

    # Filter by budget
    affordable_players = [
        p for p in available_players if p["budget"] <= remaining_budget
    ]

    if not affordable_players:
        return None, "You don't have enough budget to add more players to your team."

    # Filter by player type based on query
    filtered_players = []

    for player in affordable_players:
        category = player["category"].lower()

        if (
            (looking_for_batters and "bat" in category)
            or (looking_for_bowlers and "bowl" in category)
            or (looking_for_all_rounders and ("all" in category or "round" in category))
        ):
            filtered_players.append(player)

    if not filtered_players:
        return (
            None,
            f"I couldn't find any suitable players that match your criteria within your budget of {remaining_budget}.",
        )

    # Sort players by value (best players first)
    filtered_players.sort(key=lambda p: p["value"], reverse=True)

    # Take top 5 suggestions
    top_suggestions = filtered_players[:5]

    # Create response text
    player_types = []
    if looking_for_batters:
        player_types.append("batters")
    if looking_for_bowlers:
        player_types.append("bowlers")
    if looking_for_all_rounders:
        player_types.append("all-rounders")

    player_type_text = " and ".join(player_types)

    response_text = f"Based on your team and budget of {remaining_budget}, here are some recommended {player_type_text} you might consider:"

    return top_suggestions, response_text

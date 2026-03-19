import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from flask import jsonify, request


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
PLAYER_INFO_PATH = os.path.join(PROJECT_ROOT, "player_info.json")

# In-memory cache so we don't re-parse the huge JSON file on every request.
_PLAYER_INFO_CACHE: Optional[Dict[str, Any]] = None


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default


def _parse_match_datetime(match: Dict[str, Any]) -> datetime:
    # Prefer `match_date` (YYYY-MM-DD) but fall back to `tourney_date` (YYYYMMDD).
    match_date = match.get("match_date")
    if isinstance(match_date, str) and len(match_date) == 10:
        try:
            return datetime.fromisoformat(match_date)
        except Exception:
            pass

    tourney_date = match.get("tourney_date")
    if isinstance(tourney_date, str) and len(tourney_date) == 8 and tourney_date.isdigit():
        try:
            return datetime.strptime(tourney_date, "%Y%m%d")
        except Exception:
            pass

    return datetime.min


def _load_player_info_from_disk() -> Optional[Dict[str, Any]]:
    if not os.path.exists(PLAYER_INFO_PATH):
        return None

    with open(PLAYER_INFO_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _ensure_player_cache() -> Dict[str, Any]:
    global _PLAYER_INFO_CACHE

    if _PLAYER_INFO_CACHE is not None:
        return _PLAYER_INFO_CACHE

    player_info: Optional[Dict[str, Any]] = _load_player_info_from_disk()

    if not player_info or "players" not in player_info:
        _PLAYER_INFO_CACHE = {"players_sorted": [], "players_by_id": {}, "fields_by_player_id": {}}
        return _PLAYER_INFO_CACHE

    players = player_info.get("players", [])
    for p in players:
        # Normalize the ranking field to a number for sorting.
        p["_ranking_sort_key"] = _safe_float(p.get("ranking_num"), _safe_float(p.get("ranking"), 1e18))

    players_sorted = sorted(players, key=lambda p: p.get("_ranking_sort_key", 1e18))
    players_by_id = {str(p.get("id")): p for p in players_sorted if p.get("id") is not None}

    _PLAYER_INFO_CACHE = {"players_sorted": players_sorted, "players_by_id": players_by_id, "fields_by_player_id": {}}
    return _PLAYER_INFO_CACHE


def _get_top_players(limit: int) -> List[Dict[str, Any]]:
    cache = _ensure_player_cache()
    top_players = cache["players_sorted"][:limit]
    return [
        {
            "id": p.get("id"),
            "player": p.get("player"),
            "ranking": p.get("ranking"),
            "ranking_num": p.get("ranking_num"),
            "points": p.get("points"),
        }
        for p in top_players
    ]


def _get_player_matches(player_id: str, offset: int, limit: int) -> Tuple[List[Dict[str, Any]], List[str], int]:
    cache = _ensure_player_cache()
    player = cache["players_by_id"].get(str(player_id))

    if not player:
        return [], [], 0

    matches = player.get("matches", []) or []
    # Sort most recent first.
    matches_sorted = sorted(matches, key=lambda m: (_parse_match_datetime(m), _safe_float(m.get("match_num"), -1)), reverse=True)
    total_matches = len(matches_sorted)
    slice_matches = matches_sorted[offset : offset + limit]

    fields_by_player_id: Dict[str, List[str]] = cache.setdefault("fields_by_player_id", {})
    cached_fields = fields_by_player_id.get(str(player_id))
    if cached_fields is not None:
        return slice_matches, cached_fields, total_matches

    # Compute once per player: union of all keys across all their matches.
    # This keeps the columns stable when the UI requests more results.
    fields_set = set()
    for m in matches:
        if isinstance(m, dict):
            fields_set.update(m.keys())

    fields = sorted(fields_set)
    fields_by_player_id[str(player_id)] = fields
    return slice_matches, fields, total_matches


def register_player_list_views(app) -> None:
    @app.route("/api/top-players")
    def api_top_players():
        limit = request.args.get("limit", default=500, type=int)
        limit = max(1, min(limit, 500))
        return jsonify(players=_get_top_players(limit))

    @app.route("/api/player-matches")
    def api_player_matches():
        player_id = request.args.get("player_id", default="", type=str)
        offset = request.args.get("offset", default=0, type=int)
        limit = request.args.get("limit", default=10, type=int)

        offset = max(0, offset)
        limit = max(1, min(limit, 50))

        matches, fields, total_matches = _get_player_matches(player_id, offset=offset, limit=limit)
        return jsonify(
            player_id=player_id,
            offset=offset,
            limit=limit,
            total_matches=total_matches,
            fields=fields,
            matches=matches,
        )


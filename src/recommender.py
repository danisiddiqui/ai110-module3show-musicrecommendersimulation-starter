"""MusicRecs: a small content-based music recommender."""

import csv
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple

# Algorithm Recipe: how many points each kind of match is worth.
DEFAULT_WEIGHTS = {
    "genre": 2.0,     # exact genre match
    "mood": 1.0,      # exact mood match
    "energy": 1.5,    # max points for a perfect energy match (scaled by closeness)
    "acoustic": 0.5,  # max bonus for matching the user's acoustic preference
}

NUMERIC_FIELDS = {
    "id": int,
    "energy": float,
    "tempo_bpm": float,
    "valence": float,
    "danceability": float,
    "acousticness": float,
}


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """

    def __init__(self, songs: List[Song]):
        """Store the song catalog."""
        self.songs = songs

    @staticmethod
    def _to_prefs(user: UserProfile) -> Dict:
        """Convert a UserProfile into the prefs dictionary used by score_song."""
        return {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects for this user, highest score first."""
        prefs = self._to_prefs(user)
        ranked = sorted(self.songs, key=lambda s: score_song(prefs, asdict(s))[0], reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a readable sentence listing why this song got its score."""
        score, reasons = score_song(self._to_prefs(user), asdict(song))
        return f"Score {score:.2f}: " + "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Read the songs CSV into a list of dicts, converting numeric columns to int/float."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field, cast in NUMERIC_FIELDS.items():
                if field in row:
                    row[field] = cast(row[field])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict, weights: Optional[Dict] = None) -> Tuple[float, List[str]]:
    """Score one song against the user's prefs; return (score, list of reasons)."""
    w = {**DEFAULT_WEIGHTS, **(weights or {})}
    score = 0.0
    reasons: List[str] = []

    # Genre: all-or-nothing match (case-insensitive).
    if "genre" in user_prefs and song["genre"].lower() == str(user_prefs["genre"]).lower():
        score += w["genre"]
        reasons.append(f"genre match (+{w['genre']:.1f})")

    # Mood: all-or-nothing match (case-insensitive).
    if "mood" in user_prefs and song["mood"].lower() == str(user_prefs["mood"]).lower():
        score += w["mood"]
        reasons.append(f"mood match (+{w['mood']:.1f})")

    # Energy: reward CLOSENESS to the target, not just high or low energy.
    # gap 0.0 -> full points, gap 1.0 -> zero points.
    if "energy" in user_prefs:
        gap = abs(song["energy"] - float(user_prefs["energy"]))
        pts = w["energy"] * (1 - gap)
        score += pts
        reasons.append(f"energy {song['energy']:.2f} vs target {float(user_prefs['energy']):.2f} (+{pts:.2f})")

    # Acoustic: optional bonus scaled by how acoustic (or not) the song is.
    if "likes_acoustic" in user_prefs:
        closeness = song["acousticness"] if user_prefs["likes_acoustic"] else 1 - song["acousticness"]
        pts = w["acoustic"] * closeness
        score += pts
        label = "acoustic" if user_prefs["likes_acoustic"] else "non-acoustic"
        reasons.append(f"{label} fit (+{pts:.2f})")

    return round(score, 2), reasons


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5, weights: Optional[Dict] = None
) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort highest to lowest, and return the top k as (song, score, explanation)."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights)
        scored.append((song, score, "; ".join(reasons)))
    # sorted() returns a NEW list and leaves `songs` untouched (unlike list.sort(), which sorts in place).
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]

"""
Command line runner for the Music Recommender Simulation.

Run from the project root with:  python -m src.main
"""

try:
    from src.recommender import load_songs, recommend_songs
except ModuleNotFoundError:  # allows `python src/main.py` too
    from recommender import load_songs, recommend_songs


PROFILES = {
    # Starter default profile
    "Default Pop/Happy": {"genre": "pop", "mood": "happy", "energy": 0.8},
    # Three distinct taste profiles
    "High-Energy Pop": {"genre": "pop", "mood": "intense", "energy": 0.95, "likes_acoustic": False},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False},
    # Adversarial / edge-case profiles
    "EDGE: Sad but High Energy": {"genre": "folk", "mood": "sad", "energy": 0.9},
    "EDGE: Genre Not In Catalog": {"genre": "k-pop", "mood": "happy", "energy": 0.7},
}

# Data experiment: double energy, halve genre.
EXPERIMENT_WEIGHTS = {"genre": 1.0, "energy": 3.0}


def print_recommendations(name, prefs, songs, k=5, weights=None):
    """Print a clean, numbered top-k list with scores and reasons."""
    print("=" * 64)
    print(f"Profile: {name}")
    print("Prefs:   " + ", ".join(f"{key}={val}" for key, val in prefs.items()))
    print("-" * 64)
    for rank, (song, score, explanation) in enumerate(recommend_songs(prefs, songs, k, weights), 1):
        print(f"{rank}. {song['title']} by {song['artist']} "
              f"[{song['genre']}, {song['mood']}]  Score: {score:.2f}")
        print(f"   Because: {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print()

    for name, prefs in PROFILES.items():
        print_recommendations(name, prefs, songs)

    print("#" * 64)
    print("EXPERIMENT: weight shift (genre 2.0 -> 1.0, energy 1.5 -> 3.0)")
    print("#" * 64 + "\n")
    print_recommendations("Default Pop/Happy (experiment weights)",
                          PROFILES["Default Pop/Happy"], songs, weights=EXPERIMENT_WEIGHTS)


if __name__ == "__main__":
    main()

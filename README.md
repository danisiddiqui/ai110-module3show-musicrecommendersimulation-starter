🎵 Music Recommender Simulation
Project Summary
In this project you will build and explain a small music recommender system.
Your goal is to:
Represent songs and a user "taste profile" as data
Design a scoring rule that turns that data into recommendations
Evaluate what your system gets right and wrong
Reflect on how this mirrors real world AI recommenders
My version, MusicRecs, is a content-based recommender. It reads a 20-song catalog from `data/songs.csv` and compares every song to a user's "taste profile" (favorite genre, favorite mood, target energy, and whether they like acoustic music). Each song gets a score with a list of plain-English reasons, and the top 5 are returned. I tested it with six user profiles, including two "adversarial" ones, ran a weight-shift experiment, and documented the biases I found in the Model Card.
---
How The System Works
How real recommenders work. Apps like Spotify and YouTube mix two main approaches. Collaborative filtering uses other people's behavior: "users who liked what you liked also played this." It learns from likes, skips, replays, saves, playlist adds, and listening time. Content-based filtering uses the songs themselves: genre, mood, tempo, energy, acousticness, and so on. It recommends songs that are similar to what you already like. Real platforms combine both with millions of users. My simulation is purely content-based, because I only have song attributes and one user's preferences, with no other users' listening history.
What my version prioritizes. Genre first, then mood, then how close the song's energy is to what the user wants. Energy is the "vibe" feature that best separates a calm study playlist from a workout playlist.
Features used
`Song`: `genre`, `mood`, `energy` (0.0–1.0), `acousticness` (0.0–1.0). The CSV also has `tempo_bpm`, `valence`, and `danceability`, which are loaded but not scored yet.
`UserProfile` (dict in `main.py`): `genre` / `favorite_genre`, `mood` / `favorite_mood`, `energy` / `target_energy`, and optional `likes_acoustic` (True/False).
Algorithm Recipe (Scoring Rule, for one song)
Rule	Points
Genre matches the user's favorite	+2.0
Mood matches the user's favorite	+1.0
Energy closeness	+1.5 × (1 − |song energy − target energy|), so a perfect match earns 1.5 and the farthest possible earns 0
Acoustic fit (only if `likes_acoustic` is set)	+0.5 × acousticness if they like acoustic, or +0.5 × (1 − acousticness) if they don't
Max possible score: 5.0. Energy uses closeness instead of "higher is better," so a user who wants 0.4 energy gets calm songs, not the loudest ones.
Ranking Rule (for the whole list). The scoring rule judges one song at a time, but recommending means comparing all of them. `recommend_songs()` runs `score_song()` on every song in the catalog, sorts the results from highest to lowest score with `sorted(..., reverse=True)`, and returns the top `k`.
Data flow
```
User prefs (genre, mood, energy, likes_acoustic)
        │
        ▼
For EACH song in songs.csv ──► score_song() ──► (score, reasons)
        │
        ▼
sorted() by score, highest first ──► top k = 5 recommendations (+ reasons)
```
Dataset changes. The starter had 10 songs. I added 10 more (hip hop, metal, classical, country, reggae, r&b, edm, folk, latin, blues) with new moods (confident, angry, peaceful, nostalgic, romantic, energetic, sad), for 20 songs total.
Biases I expect. Genre is worth the most points, so the system may over-prioritize genre and bury a great song that matches the user's mood and energy but not their genre. Genre also has to match exactly, so "indie pop" gets nothing for a "pop" fan.
---
Getting Started
Setup
Create a virtual environment (optional but recommended):
```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies
Install dependencies
```bash
pip install -r requirements.txt
```
Run the app:
```bash
python -m src.main
```
Running Tests
Run the tests from the project root with:
```bash
python -m pytest
```
`tests/test_recommender.py` has 7 tests. They cover the starter OOP tests, CSV loading with number conversion, score plus reasons, energy rewarding closeness, sorting with `k`, and custom weights.
```
============================= test session starts ==============================
platform linux -- Python 3.13.16, pytest-9.1.1, pluggy-1.7.0
rootdir: .
plugins: anyio-4.15.1
collected 7 items

tests/test_recommender.py .......                                        [100%]

============================== 7 passed in 0.03s ===============================
```
---
Sample Recommendation Output
Output of `python -m src.main` for the default "pop/happy" profile (all six profiles are in the Model Card):
```
Loaded songs: 20

================================================================
Profile: Default Pop/Happy
Prefs:   genre=pop, mood=happy, energy=0.8
----------------------------------------------------------------
1. Sunrise City by Neon Echo [pop, happy]  Score: 4.47
   Because: genre match (+2.0); mood match (+1.0); energy 0.82 vs target 0.80 (+1.47)
2. Gym Hero by Max Pulse [pop, intense]  Score: 3.30
   Because: genre match (+2.0); energy 0.93 vs target 0.80 (+1.30)
3. Rooftop Lights by Indigo Parade [indie pop, happy]  Score: 2.44
   Because: mood match (+1.0); energy 0.76 vs target 0.80 (+1.44)
4. Concrete Crown by Block Theory [hip hop, confident]  Score: 1.47
   Because: energy 0.78 vs target 0.80 (+1.47)
5. Night Drive Loop by Neon Echo [synthwave, moody]  Score: 1.42
   Because: energy 0.75 vs target 0.80 (+1.42)
```
The results match what I'd expect. "Sunrise City" is the only song that's pop, happy, and close to 0.8 energy, so it wins easily.
---
Experiments You Tried
Weight shift: double energy, halve genre (genre 2.0 → 1.0, energy 1.5 → 3.0), run on the Default Pop/Happy profile:
```
================================================================
Profile: Default Pop/Happy (experiment weights)
Prefs:   genre=pop, mood=happy, energy=0.8
----------------------------------------------------------------
1. Sunrise City by Neon Echo [pop, happy]  Score: 4.94
   Because: genre match (+1.0); mood match (+1.0); energy 0.82 vs target 0.80 (+2.94)
2. Rooftop Lights by Indigo Parade [indie pop, happy]  Score: 3.88
   Because: mood match (+1.0); energy 0.76 vs target 0.80 (+2.88)
3. Gym Hero by Max Pulse [pop, intense]  Score: 3.61
   Because: genre match (+1.0); energy 0.93 vs target 0.80 (+2.61)
4. Concrete Crown by Block Theory [hip hop, confident]  Score: 2.94
   Because: energy 0.78 vs target 0.80 (+2.94)
5. Night Drive Loop by Neon Echo [synthwave, moody]  Score: 2.85
   Because: energy 0.75 vs target 0.80 (+2.85)
```
Before: Sunrise City, Gym Hero, Rooftop Lights, Concrete Crown, Night Drive Loop.
After: Sunrise City, Rooftop Lights, Gym Hero, Concrete Crown, Night Drive Loop.
Rooftop Lights (indie pop, happy, 0.76 energy) moved above Gym Hero (pop, intense, 0.93 energy). For someone who wants happy pop, that's more accurate, not just different: Gym Hero is a workout song that was only ranking high because it shares the "pop" label.
The #1 song didn't change, because Sunrise City matches on everything.
Different types of users. I tested six profiles: Default Pop/Happy, High-Energy Pop, Chill Lofi, Deep Intense Rock, and two edge cases ("Sad but High Energy" and "Genre Not In Catalog"). The full outputs and comparisons are in the Model Card.
---
Limitations and Risks
Tiny catalog: only 20 songs, and most genres have just one song, so after the first match the list fills up with "close energy" songs from random genres.
Exact-match genre: "indie pop" gets 0 genre points for a "pop" fan, and a "k-pop" fan gets no genre points at all.
Genre dominates: at +2.0, genre can push a mismatched-mood song (like Gym Hero for a happy-pop fan) above a better-fitting song.
No sense of conflicting tastes: a user who wants sad and high-energy music still gets a quiet folk song first, because genre and mood together outweigh a big energy gap.
Doesn't understand lyrics, language, artists, or listening history, and doesn't use tempo, valence, or danceability yet.
---
Reflection
Read and complete `model_card.md`:
Model Card
I learned that a recommender is really just two simple rules stacked together: a scoring rule that turns one song's features into a number, and a ranking rule that sorts all the numbers. Even with four features and some hand-picked weights, the output feels like a real recommendation, especially because each song comes with reasons like "genre match (+2.0)." The weights are where the "opinions" of the system live. Changing genre from 2.0 to 1.0 noticeably reshuffled the list.
I also saw how easily bias sneaks in. The system can only recommend what's in the dataset, and it only rewards the labels I chose to score. Exact genre matching punishes "nearby" genres and anyone whose taste isn't in the catalog. A heavy genre weight creates a filter bubble where users keep getting the same genre even when another song fits their mood better. At Spotify's scale, those same choices decide which artists get heard, which is why documenting limitations in a model card matters.

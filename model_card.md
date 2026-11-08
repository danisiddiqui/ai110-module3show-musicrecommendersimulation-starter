🎧 Model Card: Music Recommender Simulation
1. Model Name
MusicRecs
---
2. Intended Use
MusicRecs suggests the top 5 songs from a small catalog that best fit one user's taste. You give it a favorite genre, favorite mood, target energy level (0.0 = very calm, 1.0 = very intense), and optionally whether you like acoustic music.
What it generates: a ranked list of 5 songs, each with a score and the reasons it was picked.
What it assumes about the user: that their taste can be described by one genre, one mood, and one energy level, and that these don't change with the time of day or activity.
Who it's for: classroom exploration, to understand how recommenders turn data into suggestions. It is not for real users.
Not intended for: real music apps or real listeners, making decisions about which artists get promoted or paid, or any user whose taste covers several genres or moods at once. It also shouldn't be used to judge whether a song is "good." It only measures how well a song matches a few labels.
---
3. How the Model Works
Think of it like a judge giving each song points, then lining the songs up from most points to fewest.
Genre: if the song's genre is the same as your favorite, it gets 2 points. This is worth the most because genre is usually the biggest part of someone's taste.
Mood: if the song's mood matches yours (happy, chill, intense, sad...), it gets 1 point.
Energy: every song gets up to 1.5 points based on how close its energy is to what you want. A perfect match gets all 1.5. The further away it is, the fewer points it gets. This means a calm-music fan gets calm songs, not just the loudest ones.
Acoustic (optional): if you said you like acoustic music, more acoustic songs get up to 0.5 bonus points. If you said you don't, less acoustic songs get the bonus.
Then it does this for every song, sorts them from highest to lowest score, and shows the top 5 along with the reasons (like "genre match (+2.0)").
Changes from the starter logic: the starter functions were empty. I wrote the CSV loader (which turns numbers like energy into real numbers), the scoring function with the recipe above, the ranking function, and the `Recommender` class used by the tests. I also made the weights adjustable so I could run experiments.
---
4. Data
Size: 20 songs in `data/songs.csv`. The starter had 10, and I added 10.
Features per song: title, artist, genre, mood, energy, tempo (BPM), valence (how positive it sounds), danceability, and acousticness. My scoring uses genre, mood, energy, and acousticness.
Genres (17): pop, indie pop, lofi, rock, metal, edm, synthwave, hip hop, r&b, latin, reggae, jazz, blues, country, folk, ambient, and classical. Lofi has 3 songs and pop has 2; every other genre has only 1.
Moods (13): chill, happy, intense, relaxed, romantic, sad, moody, focused, confident, angry, peaceful, nostalgic, and energetic.
What I added: 10 songs in genres and moods that weren't in the starter file (hip hop/confident, metal/angry, classical/peaceful, country/nostalgic, reggae/relaxed, r&b/romantic, edm/energetic, folk/sad, latin/romantic, blues/sad).
What's missing: the songs are made up. There's nothing about lyrics, language, artist popularity, release year, or what other people listen to. Many real genres (k-pop, gospel, punk, afrobeats...) aren't included at all, and one song per genre is far too few to represent a genre.
---
5. Strengths
Clear single-genre tastes work well. For "Chill Lofi," the top 3 were all lofi songs with low energy, and the top 2 were also chill. That's exactly what I'd put on a study playlist.
Energy closeness works. It correctly separates calm and intense music. The Chill Lofi list is all low-energy songs, while the Deep Intense Rock list falls back to high-energy edm and metal once the rock songs run out.
It explains itself. Every recommendation lists its reasons and points, so it's easy to see why a song was picked and to spot when a weight is too strong.
Results matched my intuition for the default pop/happy profile: "Sunrise City" is clearly the best fit.
---
6. Limitations and Bias
The biggest weakness I found is that genre is so strong (+2.0) and so strict (exact text match) that it creates a filter bubble around genre labels. "Gym Hero" is an intense workout pop song, but it ranked #2 for a user who wanted happy pop, just because it says "pop." Meanwhile "Rooftop Lights," which is happy, has nearly the right energy, and is basically pop, ranked lower because its genre is written as "indie pop" and gets zero genre points. A "k-pop" fan gets no genre points for anything at all, because k-pop isn't in the dataset, so they're effectively treated as a "mood + energy only" user. Because most genres have only one song, anyone outside lofi or pop gets one good match and then four songs from unrelated genres that just happen to have similar energy. In a real app, this kind of design would keep pushing users toward the most common, best-labeled genres and make it harder for niche or cross-genre artists to be discovered.
Other limits: it can't handle conflicting tastes (see the "Sad but High Energy" profile in Evaluation). It also ignores tempo, valence, and danceability, and it treats every user as having exactly one genre and one mood.
---
7. Evaluation
How I tested it: I ran `python -m src.main` with six profiles: one default, three "normal" taste profiles, and two adversarial or edge-case profiles meant to trick the scoring. I checked whether the top 5 "felt" right, which songs repeated across lists, and why each #1 song won. I also ran a weight-shift experiment, and I have 7 automated tests (`python -m pytest`) checking loading, scoring, closeness-based energy, sorting, and custom weights.
Profile 1: Default Pop/Happy (`genre=pop, mood=happy, energy=0.8`)
```
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
Profile 2: High-Energy Pop (`genre=pop, mood=intense, energy=0.95, likes_acoustic=False`)
```
================================================================
Profile: High-Energy Pop
Prefs:   genre=pop, mood=intense, energy=0.95, likes_acoustic=False
----------------------------------------------------------------
1. Gym Hero by Max Pulse [pop, intense]  Score: 4.95
   Because: genre match (+2.0); mood match (+1.0); energy 0.93 vs target 0.95 (+1.47); non-acoustic fit (+0.47)
2. Sunrise City by Neon Echo [pop, happy]  Score: 3.71
   Because: genre match (+2.0); energy 0.82 vs target 0.95 (+1.30); non-acoustic fit (+0.41)
3. Storm Runner by Voltline [rock, intense]  Score: 2.89
   Because: mood match (+1.0); energy 0.91 vs target 0.95 (+1.44); non-acoustic fit (+0.45)
4. Drop Zone by Kilowatt Kids [edm, energetic]  Score: 1.99
   Because: energy 0.95 vs target 0.95 (+1.50); non-acoustic fit (+0.49)
5. Iron Cathedral by Ashen Forge [metal, angry]  Score: 1.96
   Because: energy 0.97 vs target 0.95 (+1.47); non-acoustic fit (+0.48)
```
Profile 3: Chill Lofi (`genre=lofi, mood=chill, energy=0.35, likes_acoustic=True`)
```
================================================================
Profile: Chill Lofi
Prefs:   genre=lofi, mood=chill, energy=0.35, likes_acoustic=True
----------------------------------------------------------------
1. Library Rain by Paper Lanterns [lofi, chill]  Score: 4.93
   Because: genre match (+2.0); mood match (+1.0); energy 0.35 vs target 0.35 (+1.50); acoustic fit (+0.43)
2. Midnight Coding by LoRoom [lofi, chill]  Score: 4.75
   Because: genre match (+2.0); mood match (+1.0); energy 0.42 vs target 0.35 (+1.40); acoustic fit (+0.35)
3. Focus Flow by LoRoom [lofi, focused]  Score: 3.81
   Because: genre match (+2.0); energy 0.40 vs target 0.35 (+1.42); acoustic fit (+0.39)
4. Spacewalk Thoughts by Orbit Bloom [ambient, chill]  Score: 2.85
   Because: mood match (+1.0); energy 0.28 vs target 0.35 (+1.40); acoustic fit (+0.46)
5. Coffee Shop Stories by Slow Stereo [jazz, relaxed]  Score: 1.92
   Because: energy 0.37 vs target 0.35 (+1.47); acoustic fit (+0.45)
```
Profile 4: Deep Intense Rock (`genre=rock, mood=intense, energy=0.9, likes_acoustic=False`)
```
================================================================
Profile: Deep Intense Rock
Prefs:   genre=rock, mood=intense, energy=0.9, likes_acoustic=False
----------------------------------------------------------------
1. Storm Runner by Voltline [rock, intense]  Score: 4.93
   Because: genre match (+2.0); mood match (+1.0); energy 0.91 vs target 0.90 (+1.48); non-acoustic fit (+0.45)
2. Gym Hero by Max Pulse [pop, intense]  Score: 2.93
   Because: mood match (+1.0); energy 0.93 vs target 0.90 (+1.46); non-acoustic fit (+0.47)
3. Drop Zone by Kilowatt Kids [edm, energetic]  Score: 1.92
   Because: energy 0.95 vs target 0.90 (+1.43); non-acoustic fit (+0.49)
4. Iron Cathedral by Ashen Forge [metal, angry]  Score: 1.88
   Because: energy 0.97 vs target 0.90 (+1.40); non-acoustic fit (+0.48)
5. Sunrise City by Neon Echo [pop, happy]  Score: 1.79
   Because: energy 0.82 vs target 0.90 (+1.38); non-acoustic fit (+0.41)
```
Profile 5 (edge case): Sad but High Energy (`genre=folk, mood=sad, energy=0.9`), a conflicting combination
```
================================================================
Profile: EDGE: Sad but High Energy
Prefs:   genre=folk, mood=sad, energy=0.9
----------------------------------------------------------------
1. Paper Boats by Willow & Pine [folk, sad]  Score: 3.60
   Because: genre match (+2.0); mood match (+1.0); energy 0.30 vs target 0.90 (+0.60)
2. Rainy Day Blues by Big Earl Moss [blues, sad]  Score: 1.75
   Because: mood match (+1.0); energy 0.40 vs target 0.90 (+0.75)
3. Storm Runner by Voltline [rock, intense]  Score: 1.48
   Because: energy 0.91 vs target 0.90 (+1.48)
4. Gym Hero by Max Pulse [pop, intense]  Score: 1.46
   Because: energy 0.93 vs target 0.90 (+1.46)
5. Drop Zone by Kilowatt Kids [edm, energetic]  Score: 1.43
   Because: energy 0.95 vs target 0.90 (+1.43)
```
Profile 6 (edge case): Genre Not In Catalog (`genre=k-pop, mood=happy, energy=0.7`)
```
================================================================
Profile: EDGE: Genre Not In Catalog
Prefs:   genre=k-pop, mood=happy, energy=0.7
----------------------------------------------------------------
1. Rooftop Lights by Indigo Parade [indie pop, happy]  Score: 2.41
   Because: mood match (+1.0); energy 0.76 vs target 0.70 (+1.41)
2. Sunrise City by Neon Echo [pop, happy]  Score: 2.32
   Because: mood match (+1.0); energy 0.82 vs target 0.70 (+1.32)
3. Fuego Lento by Los Corazones [latin, romantic]  Score: 1.47
   Because: energy 0.68 vs target 0.70 (+1.47)
4. Night Drive Loop by Neon Echo [synthwave, moody]  Score: 1.42
   Because: energy 0.75 vs target 0.70 (+1.42)
5. Concrete Crown by Block Theory [hip hop, confident]  Score: 1.38
   Because: energy 0.78 vs target 0.70 (+1.38)

################################################################
EXPERIMENT: weight shift (genre 2.0 -> 1.0, energy 1.5 -> 3.0)
```
Comparing pairs of profiles:
Default Pop/Happy vs. High-Energy Pop: both get the same two pop songs at the top, but in swapped order. Changing the mood from "happy" to "intense" and raising energy to 0.95 moves Gym Hero to #1 and Sunrise City to #2. That makes sense: Gym Hero is the intense, high-energy one. The rest of the High-Energy list fills with the loudest songs (Storm Runner, Drop Zone, Iron Cathedral) instead of the happy ones.
High-Energy Pop vs. Chill Lofi: these are opposites, and the lists share zero songs. High-Energy Pop is all 0.82–0.97 energy and non-acoustic. Chill Lofi is all 0.28–0.42 energy and acoustic (lofi, ambient, jazz). This shows the energy-closeness rule really separates "workout" from "study" music.
Chill Lofi vs. Deep Intense Rock: Chill Lofi has 3 genre matches to pick from, so its list stays on-genre. Deep Intense Rock has only one rock song, so after Storm Runner the list falls back to pop, edm, and metal that just match the energy. Same algorithm, but the rock fan gets a much less "rock" list purely because of the dataset.
Deep Intense Rock vs. High-Energy Pop: both want intense, high-energy, non-acoustic music, so all 5 songs are the same, just in a different order. The order changes, depending on which genre gets the +2.0. This shows genre is the main thing separating these two users.
Sad but High Energy vs. Deep Intense Rock: both ask for about 0.9 energy, but the sad user's #1 is a quiet folk song (0.30 energy). Genre and mood together (+3.0) beat a big energy gap. Songs 3–5 on the sad user's list are the same loud songs the rock fan gets (Storm Runner, Gym Hero, Drop Zone), because once nothing matches genre or mood, only energy is left.
Genre Not In Catalog vs. Default Pop/Happy: both want happy music at similar energy, but with no genre points possible, the k-pop user's list is decided by mood plus energy. Rooftop Lights (indie pop) actually edges out Sunrise City, and Gym Hero disappears from the top 5 entirely.
Why does "Gym Hero" keep showing up? (in plain language) Gym Hero appears in 4 of the 6 lists: Default, High-Energy Pop, Deep Intense Rock, and even Sad but High Energy. For the happy-pop person, it isn't happy at all. It's an intense gym song. But the system gives 2 big points just for having the word "pop" in its genre, plus decent energy points, so it beats songs that actually sound happy. It's like a store recommending a product because it's in the right aisle, even though it's not what you were looking for.
Why did Sunrise City rank first for Default Pop/Happy? It's the only song that matches all three things at once: genre (pop, +2.0), mood (happy, +1.0), and energy (0.82 vs. a 0.80 target, +1.47). Its 4.47 is more than a full point ahead of #2.
Experiment: weight shift (genre 2.0 → 1.0, energy 1.5 → 3.0)
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
Rooftop Lights jumped from #3 to #2, above Gym Hero. For a happy-pop listener, I think that's more accurate, not just different. Rooftop Lights is happy with nearly the right energy, while Gym Hero only got ahead before because of its genre label. The #1 song stayed the same. The trade-off is that with genre weaker, users who care a lot about genre may start seeing more off-genre songs.
What surprised me: how much the dataset shapes the results, not just the weights. The rock fan and the lofi fan run through the exact same code, but the lofi fan gets a much better list just because there are three lofi songs and only one rock song. I was also surprised that the "sad but high energy" user gets a slow folk song first. The math works fine, but it ignores what that person actually asked for.
---
8. Future Work
Partial genre matches: treat related genres as close (for example, "indie pop" gets partial credit for a "pop" fan), and let users pick more than one favorite genre.
Use more features: add tempo, valence, and danceability to the closeness score, so a "happy" user's songs actually sound positive.
Diversity in the top 5: limit to one or two songs per genre or artist so the list isn't dominated by one label, and flag conflicting preferences (like sad plus 0.9 energy) instead of quietly ignoring one.
A much bigger dataset with several songs per genre, so a rock fan gets a rock list.
---
9. Personal Reflection
Biggest learning moment: realizing that a recommender is just a scoring rule for one song plus a ranking rule for the list. Then I saw that the weights I picked, like making genre worth 2.0, are really opinions built into the system. When I halved the genre weight, Gym Hero dropped below Rooftop Lights, and I realized the "best" recommendation depends on choices a person made, not some objective truth.
How AI helped, and when I double-checked: I used Claude as my AI coding assistant. It explained collaborative vs. content-based filtering, helped design the closeness formula for energy (`1.5 × (1 − gap)`) instead of "higher energy = better," generated the 10 extra songs, wrote the loader, scoring, and ranking functions, and suggested the adversarial profiles. I double-checked it by running `python -m src.main` and doing the math for the top songs by hand. For example, Sunrise City is 2.0 + 1.0 + 1.5 × (1 − 0.02) = 4.47, which matches the output. I also noticed that the starter `main.py` used `from recommender import ...`, which breaks when you run `python -m src.main`, so it had to be changed to import from `src.recommender`. The automated tests confirmed the scores and sorting.
What surprised me: how something this simple still feels like a real recommendation. Seeing "genre match (+2.0); mood match (+1.0)" next to each song makes it seem smart, even though it's just adding up a few numbers. It also made me realize how much power real apps have when they quietly decide these weights for millions of people.
What I'd try next: combine this with a simple form of collaborative filtering (for example, "users with a similar profile also liked..."), add partial genre matching, and test it on a much larger real dataset to see whether the same biases show up.

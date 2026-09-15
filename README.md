# Podcast audio pipeline (free, three voices)

## One-time setup (15 min, needs a laptop or the GitHub iOS app)
1. Create a GitHub repo, e.g. `Luke11038/Podcasts`, with this layout:
   ```
   episodes/episode-01-how-to-actually-talk-to-people.md
   episodes/episode-02-the-late-twenties-squeeze.md
   tools/md_to_vibevoice.py
   tools/make_episode_vibevoice.ipynb
   ```
2. Open https://colab.research.google.com, File → Upload notebook → `make_episode_vibevoice.ipynb`.
   It saves to your Drive as a Colab notebook. Bookmark it on your phone.

## Every episode (all from the phone)
1. Get the new script `.md` into `episodes/` in the repo (GitHub app, or Claude can push it via the API).
2. Open the Colab bookmark → edit `EPISODE_FILE` in cell 1 → Runtime → Run all.
3. Approve the Drive permission prompt when cell 5 asks.
4. 45–90 min later the MP3 is in Google Drive → `Podcasts/`. Play it from the Drive app or download to Files.

## Voices
- Default presets: Speaker 1 (NICK) = Carter, Speaker 2 (SOPHIE) = Alice, Speaker 3 (DAN) = Frank.
- For better/Aussie voices, add 10–30 s WAV samples named `en-Nick_man.wav`, `en-Sophie_woman.wav`, `en-Dan_man.wav`
  to `demo/voices/` and set the names in cell 1. Keep the same samples every episode so the cast stays consistent.

## If you'd rather pay a little and skip Colab
- Replicate: https://replicate.com/microsoft/vibevoice — upload the `.txt` produced by `md_to_vibevoice.py`.
- ElevenLabs v3 Dialogue mode via the website also works; use `make_episode.py` from earlier for the API version.

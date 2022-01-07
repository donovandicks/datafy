# Mood Tracker

Tracks the users relative mood over a recent period based on their listening habits.

__NOTE:__ This is only setup for myself right now.

## Desgin

The service functions as follows:

1. Retrieve a list of Spotify track IDs for the songs played within the time period
2. In parallel, retrieve the `energy` value of each song
3. Average the energy value of all songs retrieved within the time period
4. Make an assessment of the user's mood based on the average song energy
5. Report to the user

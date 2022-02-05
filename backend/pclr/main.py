"""Main driver"""


def main():
    """Drives the main play counting logic"""
    while True:
        pass
        # 1. Query for current song
        # 2a. If current song:
        #     -> send song to queue for processing
        #     -> calculate time to end of song
        #     -> sleep until end, query for song
        # 2b. If not current song:
        #     -> calculate length of time to sleep depending on current time of day
        #     -> sleep until next wake, query for song

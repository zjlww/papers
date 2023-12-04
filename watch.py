"""
Watch all notes in /notes. If any note changes, try to update meta information about that paper.
"""
import logging
from tasks import asyncio, watch_notes
from sys import stderr


if __name__ == "__main__":
    print("Watching /notes for changes...")
    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=stderr,
    )

    asyncio.run(watch_notes(), debug=True)

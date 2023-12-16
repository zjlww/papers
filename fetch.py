"""
Fetch meta data of a paper from S2 API. Then create the note file in /notes
automatically filled with the meta data.
"""
import argparse
import asyncio
from s2api import get_paper
from pathlib import Path


async def create_note(paper_id: str, nick_name: str):
    root = Path("./notes/")
    paper = await get_paper(paper_id)
    content = f"""---
corpus_id: {paper.corpusId}
title: "{paper.title}"
stars: 3
topics: []
---
"""
    if nick_name:
        file = root / f"{nick_name}.md"
    else:
        file = root / f"{paper.corpusId}.md"

    if file.is_file():
        print(
            f"Note file {file.relative_to(root)} exists for paper {paper.corpusId} -- {paper.title}"
        )
    else:
        with open(file, "w") as f:
            f.write(content)
        print(
            f"Note file {file.relative_to(root)} created for paper {paper.corpusId} -- {paper.title}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a meta note given paper's identifier."
    )
    parser.add_argument("paper_id", type=str, help="Paper Identifier")
    parser.add_argument(
        "nick_name", type=str, nargs="?", default=None, help="Optional Nickname"
    )

    args = parser.parse_args()

    paper_id = args.paper_id
    nick_name = args.nick_name
    asyncio.run(create_note(paper_id, nick_name))

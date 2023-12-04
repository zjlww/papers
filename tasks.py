from semanticscholar import PaperID, Paper
from yaml import safe_load
from pathlib import Path
from typing import List, Any, Dict, Optional
import watchfiles
import s2api
import graphapi
from time import time
import asyncio


UPDATE_INTERVAL = 24 * 60 * 60  # A day


async def get_paper(paper_id: PaperID) -> Paper:
    return await s2api.get_paper(paper_id)


async def add_paper(paper_id: PaperID, state: int) -> int:
    paper = await get_paper(paper_id)
    corpus_id = await graphapi.add_paper(paper, state)
    return corpus_id


async def get_links_range(
    citation: bool, corpus_id: int, first: int, last: int
) -> List[Paper]:
    if citation:
        task = asyncio.create_task(s2api.get_citations_range(corpus_id, first, last))
    else:
        task = asyncio.create_task(s2api.get_references_range(corpus_id, first, last))
    return await task


async def graph_add_links(ids: List[int], corpus_id: int, citation: bool) -> None:
    if citation:
        return await graphapi.add_citations(corpus_id, ids)
    else:
        return await graphapi.add_references(ids, corpus_id)


async def add_links_range(
    citation: bool, corpus_id: int, first: int, last: int, state: int
) -> None:
    papers = await get_links_range(citation, corpus_id, first, last)
    corpus_ids = await graphapi.add_papers(papers, state=state)
    await graph_add_links(corpus_ids, corpus_id, citation)


async def query_paper(corpus_id: int) -> Optional[Dict[str, Any]]:
    paper = await graphapi.get_paper(corpus_id)
    if paper is None:
        return None
    else:
        return {
            "citationCount": paper["citationCount"],
            "referenceCount": paper["referenceCount"],
            "corpusId": corpus_id,
            "addedDate": paper["addedDate"].to_native().timestamp(),
            "lastUpdate": paper["lastUpdate"].to_native().timestamp(),
            "state": paper["state"],
        }


async def add_links(
    citation: bool, corpus_id: int, batch: int, limit: int, state: int
) -> None:
    info = await query_paper(corpus_id)
    if info is not None:
        N = info["citationCount"] if citation else info["referenceCount"]
        N = min(N, limit)
        tasks = [
            add_links_range(citation, corpus_id, i, i + batch, state=state)
            for i in range(0, N, batch)
        ]
        await asyncio.gather(*tasks)


async def add_paper_and_links(
    paper_id: PaperID, batch: int = 50, state: int = 2
) -> None:
    corpus_id = await add_paper(paper_id, state)
    await asyncio.gather(
        add_links(True, corpus_id, batch, 200, -1),
        add_links(False, corpus_id, batch, 1000, 0),
    )
    # await add_links(False, corpus_id, limit)


async def try_update(corpus_id: int, state: int):
    info = await query_paper(corpus_id)
    if info is None:
        await add_paper_and_links(corpus_id, batch=50, state=state)
    else:
        if info["state"] <= 0 or time() - info["lastUpdate"] > UPDATE_INTERVAL:
            await add_paper_and_links(corpus_id, state=state)


async def scan_note(note_path: Path) -> None:
    with open(note_path, "r") as f:
        d = f.read()
        front_matter = d.split("---")[1]
    meta = safe_load(front_matter)  # type: dict
    topics = meta.get("topics", [])
    stars = meta.get("stars", 1)
    corpus_id = meta.get("corpus_id", -1)
    if "corpus_id" not in meta:
        return None

    await try_update(corpus_id, state=2)
    await graphapi.drop_topics(corpus_id)
    await graphapi.add_topics(corpus_id, topics)
    await graphapi.set_paper_stars(corpus_id, stars)


async def scan_notes(note_root=Path("./notes")):
    assert note_root.is_dir(), f"note root {note_root} not found"
    files = note_root.glob("**/*.md")
    tasks = [scan_note(file) for file in files]
    await asyncio.gather(*tasks)


async def watch_notes(note_root=Path("./notes")):
    async for changes in watchfiles.awatch(note_root):
        for change in changes:
            p = Path(change[1])
            print(f"Updating {p} ...")
            asyncio.create_task(scan_note(p))

from typing import List
import asyncio

from semanticscholar import Paper, SemanticScholar, PaperID, FIELDS


sch = SemanticScholar(timeout=60)
retry_schedule = [2, 4, 8, 16]
semaphor = asyncio.Semaphore(1)


async def get_paper(paper_id: PaperID) -> Paper:
    """Find a paper from SemanticScholar."""
    loop = asyncio.get_event_loop()
    for retry_time in retry_schedule:
        try:
            async with semaphor:
                return await loop.run_in_executor(None, sch.get_paper, paper_id)
        except:
            await asyncio.sleep(retry_time)
    raise Exception(f"Failed to get_paper({paper_id})")


async def get_citations_range(corpus_id: int, first: int, last: int) -> List[Paper]:
    loop = asyncio.get_event_loop()
    for retry_time in retry_schedule:
        try:
            async with semaphor:
                return await loop.run_in_executor(
                    None, sch.get_paper_citations, corpus_id, FIELDS, first, last
                )
        except:
            await asyncio.sleep(retry_time)
    raise Exception(f"Failed to get_citation_rage({corpus_id}, {first}, {last})")


async def get_references_range(corpus_id: int, first: int, last: int) -> List[Paper]:
    loop = asyncio.get_event_loop()
    for retry_time in retry_schedule:
        try:
            async with semaphor:
                return await loop.run_in_executor(
                    None, sch.get_paper_references, corpus_id, FIELDS, first, last
                )
        except:
            await asyncio.sleep(retry_time)
    raise Exception(f"Failed to get_references_range({corpus_id}, {first}, {last})")

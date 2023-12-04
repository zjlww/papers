from datetime import datetime
from typing import List, Optional

from neo4j import GraphDatabase, Driver, AsyncGraphDatabase
from semanticscholar.Paper import Paper
import asyncio

URI = "bolt://localhost:7687"
AUTH = ("", "")
driver = AsyncGraphDatabase.driver(uri=URI, auth=AUTH)
semaphore = asyncio.Semaphore(3)


async def create_index():
    async with semaphore:
        await driver.execute_query(
            """
            CREATE INDEX ON :Paper(corpusId);
            CREATE INDEX ON :Venue(name);
            CREATE INDEX ON :Author(name);
            CREATE INDEX ON :Topic(name);
            """
        )


async def get_paper(corpus_id: int) -> Optional[dict]:
    try:
        async with semaphore:
            result = await driver.execute_query(
                """
                MATCH (p:Paper {corpusId:$corpusId})
                RETURN p
                """,
                corpusId=corpus_id,
            )
            return result.records[0].data()["p"]
    except:
        return None


async def add_paper(p: Paper, state: int = 2) -> int:
    # We use corpusId as the unique identifier of a paper.
    async with semaphore:
        if p.corpusId is None:
            return
        corpusId = int(p.corpusId)
        publicationDate = (
            p.publicationDate.date() if p.publicationDate is not None else None
        )

        await driver.execute_query(
            """
            MERGE (p:Paper {corpusId:$corpusId})
            ON CREATE SET p.addedDate = $date
            SET p.name = $name
            SET p.year = $year
            SET p.abstract = $abstract
            SET p.publicationDate = $publicationDate
            SET p.referenceCount = $referenceCount
            SET p.citationCount = $citationCount
            SET p.lastUpdate = $date
            SET p.state = CASE WHEN p.state > $state THEN p.state ELSE $state END
            """,
            name=p.title,
            corpusId=corpusId,
            year=p.year,
            abstract=p.abstract,
            publicationDate=publicationDate,
            referenceCount=p.referenceCount,
            citationCount=p.citationCount,
            date=datetime.now(),
            state=state,
        )

        # Find or create the authors.
        for idx, author in enumerate(p.authors):
            await driver.execute_query(
                """
                MATCH (p:Paper {corpusId:$corpusId})
                MERGE (a:Author {id: $author_id, name: $author_name})
                MERGE (p)<-[r:AUTHORS]-(a)
                SET r.rank = $rank
                """,
                corpusId=corpusId,
                author_id=int(author["authorId"]) if author["authorId"] else 0,
                author_name=author["name"],
                rank=idx,
            )

        IGNORE_VENUES = ["arXiv.org"]
        if (
            p.publicationVenue is not None
            and p.publicationVenue.name not in IGNORE_VENUES
        ):
            # Find or create the publication venue.
            await driver.execute_query(
                """
                MATCH (p:Paper {corpusId:$corpusId})
                MERGE (v:Venue {id: $venue_id})
                MERGE (p)-[:JOINS]->(v)
                SET v.name = $venue_name
                SET v.type = $venue_type
                SET v.url = $venue_url
                """,
                corpusId=corpusId,
                venue_id=p.publicationVenue.id,
                venue_name=p.publicationVenue.name,
                venue_type=p.publicationVenue.type,
                venue_url=p.publicationVenue.url,
            )

        # Update external IDs:
        if p.externalIds is not None:
            for extName, extId in p.externalIds.items():
                await driver.execute_query(
                    "MATCH (p:Paper {corpusId:$corpusId})"
                    + f" SET p.{extName} = $extId",
                    corpusId=corpusId,
                    extId=extId,
                )

        return corpusId


async def add_papers(papers: List[Paper], state: int = 0) -> List[int]:
    tasks = [add_paper(paper, state=state) for paper in papers]
    ids = await asyncio.gather(*tasks, return_exceptions=False)
    ids = [id for id in ids if isinstance(id, int)]
    return ids


async def add_citations(src_id: int, tgt_ids: List[int]) -> None:
    async with semaphore:
        await driver.execute_query(
            """
            UNWIND $tgt_ids AS tgt_id
            MATCH (p:Paper {corpusId:$src_id}), (q:Paper {corpusId:tgt_id})
            MERGE (q)-[:CITES]->(p)
            """,
            src_id=src_id,
            tgt_ids=tgt_ids,
        )


async def add_references(src_ids: List[int], tgt_id: int):
    async with semaphore:
        await driver.execute_query(
            """
            UNWIND $src_ids AS src_id
            MATCH (p:Paper {corpusId:src_id}), (q:Paper {corpusId:$tgt_id})
            MERGE (q)-[:CITES]->(p)
            """,
            src_ids=src_ids,
            tgt_id=tgt_id,
        )


async def set_paper_stars(corpus_id: int, stars: int):
    async with semaphore:
        await driver.execute_query(
            """
            MATCH (p:Paper {corpusId:$corpusId})
            SET p.stars = $stars
            """,
            corpusId=corpus_id,
            stars=stars,
        )


async def drop_topics(corpus_id: int):
    async with semaphore:
        await driver.execute_query(
            """
            MATCH (p:Paper {corpusId:$corpus_id})<-[r:CONTAIN]-(t:Topic)
            DELETE r
            """,
            corpus_id=corpus_id,
        )


async def add_topic(corpus_id: int, tag: str):
    tag = tag.strip().lower()
    async with semaphore:
        await driver.execute_query(
            """
            MATCH (p:Paper {corpusId:$corpus_id})
            MERGE (t:Topic {name:$tag})
            MERGE (t)-[:CONTAIN]->(p)
            """,
            corpus_id=corpus_id,
            tag=tag,
        )


async def add_topics(corpus_id: int, topics: List[str]):
    topics = [topic.strip().lower() for topic in topics]
    async with semaphore:
        await driver.execute_query(
            """
            UNWIND $tags AS tag
            MATCH (p:Paper {corpusId:$corpus_id})
            MERGE (t:Topic {name:tag})
            MERGE (t)-[:CONTAIN]->(p)
            """,
            corpus_id=corpus_id,
            tags=topics,
        )


async def list_topics() -> List[str]:
    async with semaphore:
        result = await driver.execute_query(
            """
            MATCH (t:Topic)
            RETURN t.name
            """
        )
    topics = [rec.data()["t.name"] for rec in result.records]
    return topics

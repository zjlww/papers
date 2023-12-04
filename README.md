## Papers
![visualization of the citation network](<banner.png>)
Connected Papers is a great service, but it is too expensive, and uncustomizable. Here we implement a version with `memgraph`. The code is based on Python asyncio.

The service watches changes in the `notes` folder, which contains markdown files with YAML frontmatters. On file changes, it will try to update information about the paper.
- Meta data are read from markdown JSON front matter.
    - The front matter must contain the `corpus_id` field.
    - Optionally, it may contain a `topics` list of strings.
    - Optionally, it may contain a `star` field in 1, 2, 3, 4, 5.
- The file name and directory structure are ignored by the program.

### Quick Start

1. Set up memgraph on localhost by `docker compose up -d`. Access the memgraph-lab for visualization.
    - Ensure that `memgraph` is in `IN_MEMORY_ANALYTIC` mode. Otherwise parallel transactions might have conflict, and we haven't implemented retry yet.
2. Install Python dependencies `requests`, `neo4j`, `yaml`
3. Run `python watch.py` to start the service.
4. Write CYPHER queries and visualize citations in Memgraph Lab. (There is no plan for a custom GUI yet.)

### Database Schema

Node Types:
- Paper:
    - corpusId: int (key)
    - name: str
    - year: int
    - abstract: str
    - publicationDate: int
    - referenceCount: int
    - citationCount: int
    - star: int
- URL:
    - name: str
    - url: str
- Author:
    - id: int
    - name: str
- Venue:
    - id: int
    - name: str
    - type: str
    - url: str
- Topic:
    - name: str

Relations:
- (Author)-[:AUTHORS]->(Paper)
    - rank: int in {0, 1, 2, ...}, 0 for the first author.
- (Paper)-[:JOINS]->(Venue)
- (Paper)-[:CITES]->(Paper)
- (URL)-[:CITES]->(Paper)
- (Topic)-[:CONTAIN]->(Paper)


### SemanticScholar API

This project is based on the S2 API. Read the [documentation](https://api.semanticscholar.org/api-docs/) for more details. There is a Python wrapper of the S2 API [here](https://github.com/danielnsilva/semanticscholar). This wrapper is absorbed by this repository.

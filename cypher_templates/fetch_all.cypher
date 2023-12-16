// Plot all papers and their citations.
MATCH (p:Paper)-[r:CITES]-(q:Paper)
RETURN p, q, r

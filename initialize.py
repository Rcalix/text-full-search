#!/usr/bin/env python3
"""
Create and populate a minimal PostgreSQL schema for full text search
"""

import postgresql

DB_NAME = 'pgfts'
DB_HOST = 'localhost' # Uses a local socket
DB_USER = 'test'

DB = postgresql.open(host=DB_HOST, database=DB_NAME, user=DB_USER)

def load_db():
    """Add sample data to the database"""

    ins = DB.prepare("""
        INSERT INTO fulltext_search (doc, value)
        VALUES ($1, $2)
    """)
    ins('Sketching the trees', 15)
    ins('Found in schema.org', 20)
    ins('Sketched out in schema.org', 5)
    ins('Girl on a train', 3)
    ins('Sketching the Walden Theme', 9)
    ins('Found in Uol', 4)
    ins('Course title link', 3)
    ins('Sketching the Uol Theme', 9)

def init_db():
    """Initialize our database"""
    DB.execute("DROP TABLE IF EXISTS fulltext_search")
    DB.execute("""
        CREATE TABLE fulltext_search (id SERIAL, doc TEXT, value INT, tsv TSVECTOR)
    """)
    DB.execute("""
        CREATE TRIGGER tsvupdate BEFORE INSERT OR UPDATE ON fulltext_search
        FOR EACH ROW EXECUTE PROCEDURE
        tsvector_update_trigger(tsv, 'pg_catalog.english', doc)
    """)
    DB.execute("CREATE INDEX fts_idx ON fulltext_search USING GIN(tsv)")

if __name__ == "__main__":
    init_db()
    load_db()

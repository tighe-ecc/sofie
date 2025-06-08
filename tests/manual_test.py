# tests/manual_test.py
from pathlib import Path
from sofie.core.indexer import index_file
from sofie.cli.query import query_text

if __name__ == "__main__":
    index_file(Path("testdata/example.txt"))
    query_text("what is sofie for?")

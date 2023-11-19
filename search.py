import logging
import argparse
from sentence_transformers import SentenceTransformer

from logconfig import setup_logging
from src import search

setup_logging()
logger = logging.getLogger()

def main():
    model= SentenceTransformer('all-MiniLM-L6-v2')
    index, id_map = search.load_index(args.index_path)
    while True:
        query = input("Enter query: ")
        if query == 'exit':
            break
        res = search.search(query, index, id_map, model, 5)
        logging.info(f"Got {len(res)} results:"),
        for i, res in enumerate(res):
            logging.info(f"{i+1}. {res}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--index_path", type=str, default="index", help="path to index")
    args = parser.parse_args()
    main()
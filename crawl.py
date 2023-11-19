import logging
import argparse

from src.crawl import crawl
from src import index
from logconfig import setup_logging

setup_logging()
logger = logging.getLogger()

def main():
    results = crawl(args.root, args.page_limit)
    logger.info(f"Done crawling, indexed the following urls:")
    for url in results.keys():
        logger.info(f"\t {url}")
    logger.info("Indexing all data")
    index.save_index(results, args.save_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=str, required=True, help="url of root page")
    parser.add_argument("--page_limit", default=100, type=int, help="total pages to crawl")
    parser.add_argument("--save_path", type=str, default="index", help="where to store the index")
    args = parser.parse_args()
    main()
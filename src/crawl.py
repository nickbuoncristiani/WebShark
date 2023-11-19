import requests
from bs4 import BeautifulSoup as bs
import logging
from typing import Dict, List
from langdetect import detect as detect_language
from langdetect.lang_detect_exception import LangDetectException
import random

logger = logging.getLogger(__name__)

def crawl(root: str, max_pages: int) -> Dict[str, List[str]]:
    index = {}
    seen = set()
    queue = [root]
    while len(queue) > 0:
        url = queue.pop(0)
        if url in seen:
            continue
        
        seen.add(url)

        logger.debug(f"Opening {url}")
        try:
            resp = requests.get(url, timeout=4)
        except requests.RequestException as err:
            logger.error(f"Found error while opening {url}:\n{err}")
            continue

        if resp.status_code != 200:
            logger.error(f"Opening {url} gave invalid status code {resp.status_code}")
            continue

        soup = bs(resp.text, 'html.parser')
    
        # index all text on page under the url
        tags = ['h1', 'h2', 'h3', 'p', 'li']
        leafs = [elem.get_text() for elem in soup.find_all(tags)]
        sentences = []
        for leaf in leafs:
            sentences.extend(leaf.split('.'))
        texts = [_clean_text(sentence) for sentence in sentences]
        texts = list(filter(_filter, texts))

        # if page doesn't pass filter ignore it
        if not _filter_page(url, texts):
            logger.info(f"Skipping {url}")
            continue

        index[url] = texts
        logger.info(f"Succesfully added {url} to index")

        # get all outgoing http/https links
        children = [link.get('href') for link in soup.find_all('a') if link and link.get('href')]
        children = [link for link in children if _is_external_link(link)]

        # add child links to queue
        queue.extend(children)

        if len(index) > max_pages:
            logger.warn(f"Reached page limit of {max_pages}")
            break
            
    if len(index) < max_pages:
        logger.warn("Finished crawl without reaching page limit")

    return index

def _is_external_link(link: str) -> bool:
    return link.startswith('http://') or link.startswith('https://')

def _clean_text(s: str) -> str:
    s = ' '.join(s.split())
    s = ''.join([c for c in s if c.isalpha() or c.isspace()])
    s = s.strip()
    return s

# returns true if an individual piece of text should be indexed
def _filter(s: str) -> bool:
    return len(s) > 3

# returns true iff a certain threshold of text excerpts from the page are in english
def _filter_page(url: str, texts: List[str]) -> bool:
    if len(texts) < 32:
        return False
    num_samples, required_en = 32, 16
    en_count = 0
    for _ in range(num_samples):
        text = random.choice(texts)
        try:
            lang = detect_language(text)
        except LangDetectException: 
            continue
        if lang == 'en':
            en_count += 1
    if en_count < required_en:
        return False
    return True

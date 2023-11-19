from sentence_transformers import SentenceTransformer
import faiss
import json
import os
from typing import Dict, List
import logging
import numpy as np

logger = logging.getLogger(__name__)

def save_index(pages: Dict[str, List[str]], save_path: str) -> None:
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    dim = model.get_sentence_embedding_dimension()
    reverse_map = {}
    index = faiss.IndexFlatL2(dim)
    id = 0
    logger.info(f"Embedding crawled text & adding to index...")
    for url, texts in pages.items():
        logger.debug(f"encoding {url} with {len(texts)} elements")
        for text in texts:
            embed = model.encode(text)
            reverse_map[id] = [url, text]
            index.add(np.expand_dims(embed, 0))
            id += 1
    logger.info(f"Saving index to {save_path}")
    faiss.write_index(index, os.path.join(save_path, 'index'))
    with open(os.path.join(save_path, 'ids.json'), 'w') as fout:
        json.dump(reverse_map, fout)
    logger.info(f"Success!")

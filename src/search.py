from sentence_transformers import SentenceTransformer
import logging
import faiss
import os, json
from typing import Tuple, Dict, List

logger = logging.getLogger(__name__)

def search(query: str, idx: faiss.Index, id_map: Dict[int, Tuple[str, str]], model: SentenceTransformer, k: int) -> List[Tuple[str, str]]:
    logging.debug(f"received query {query}")
    embed = model.encode([query])
    _, ids = idx.search(embed, k=k)
    ids = ids[0] # just one query
    return [id_map[id] for id in ids]
   
def load_index(index_path: str) -> Tuple[faiss.Index, Dict[int, Tuple[str, str]]]:
    idx = faiss.read_index(os.path.join(index_path, 'index'))
    with open(os.path.join(index_path, 'ids.json'), 'r') as json_file:
        ids = json.load(json_file)
    int_keys = {}
    for i, url in ids.items():
        int_keys[int(i)] = url
    return idx, int_keys
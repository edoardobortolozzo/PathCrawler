from hashlib import blake2b
from pathlib import Path
from typing import Union
import multiprocessing as mp

global NUM_THREADS
NUM_THREADS = 1

def getFileHash(element: Path) -> str:
    with open(str(element),"rb") as f:
        bytes = f.read()
        hashstr = blake2b(bytes).hexdigest()
    f.close()
    return hashstr

def getMpFileHash(element: Path) -> Union[str,str]:
    hashstr = getFileHash(element)
    return str(element),hashstr

def updateHashmap(hashmap: dict, files: list) -> Union[dict, bool]:
    with mp.Pool(NUM_THREADS) as pool:
        duplicatesExist = False
        arr = list(zip(files, pool.map(getFileHash, files)))
        for path, hashstr in arr:
            hashmap, b = appendHashmap(hashmap, hashstr, path)
            duplicatesExist = duplicatesExist or b
                
    return hashmap, duplicatesExist

def appendHashmap(hashmap: dict, key: str, value: str) -> Union[dict, bool]:
    duplicatesExist = False
    if key in hashmap:
        duplicatesExist = True
        hashmap.get(key).append(value)
    else:
        hashmap[key] = [value]
    
    return hashmap, duplicatesExist
from pathlib import Path
from typing import Union
import multiprocessing as mp
import utils as lib
import global_settings as gs


def addFileHashesRecursive(path: Path, extensions=[]) -> Union[dict,bool]:
    #init function
    if gs.VERBOSITY_LEVEL > 0:
        print("Searching in " + str(path))
    hashmap = dict()
    dirs = list()
    duplicatesExist = False
    files = []

    #check if element is file or directory
    for el in path.iterdir():
        if gs.VERBOSITY_LEVEL > 1:
            print(el)
        if el.is_dir():
            if el.parts[-1] in extensions: continue
            dirs.append(el)
        else:
            if el.suffix in extensions: continue
            #add hash at dictionary
            files.append(el)

    #TODO FIXME chiamata funzione lib.updateHashmap()
    with mp.Pool(gs.NUM_THREADS) as pool:
        arr = pool.map(lib.getMpFileHash, files)
        for path, hashstr in arr:
            hashmap, b = lib.appendHashmap(hashmap, hashstr, path)
            duplicatesExist = duplicatesExist or b

    #call function recursively on subdirectories
    for subdir in dirs:
        h, de = addFileHashesRecursive(subdir, extensions)
        duplicatesExist = de or duplicatesExist
        for hashstr in h.keys():
            hashmap, de = lib.extendHashmap(hashmap, hashstr, h.get(hashstr))
            duplicatesExist = de or duplicatesExist

    return hashmap, duplicatesExist

def addFileHashesIterative(path: Path, extensions=[]) -> Union[dict,bool]:
    hashmap = dict()
    dirs = [path]
    duplicatesExist = False
    files = []

    while dirs:
        path = dirs.pop()
        if gs.VERBOSITY_LEVEL > 0:
            print("Searching in " + str(path))
        for el in path.iterdir():
            if gs.VERBOSITY_LEVEL > 1:
                print(el)
            if el.is_dir():
                if el.parts[-1] in extensions: continue
                dirs.append(el)
            else:
                if el.suffix in extensions: continue
                files.append(el)

    hashmap, duplicatesExist = lib.updateHashmap(hashmap, files)
    
    return hashmap, duplicatesExist

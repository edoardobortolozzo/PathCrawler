from hashlib import blake2b
from pathlib import Path
import sys
import platform
import win32com.client
from typing import Union
import multiprocessing as mp
import global_settings as gs

def openWinLink(element: Path) -> Path:
    shell = win32com.client.Dispatch("WScript.Shell")
    link = shell.CreateShortCut(element)
    return Path(link.Targetpath)


def getFileHash(element: Path) -> Union[str,IOError]:
    #TODO call openWinLink on win sys
    if element.is_symlink():
        element = element.readlink()
    try:
        with open(str(element),"rb") as f:
            bytes = f.read()
            hashstr = blake2b(bytes).hexdigest()
    except EnvironmentError as err:
        return None

    return hashstr

def getMpFileHash(element: Path) -> Union[str,str]:
    hashstr = getFileHash(element)
    return str(element),hashstr

def updateHashmap(hashmap: dict, files: list) -> Union[dict, bool]:
    if gs.DEBUG: print("\nNumber workers: ", gs.NUM_THREADS)
    with mp.Pool(gs.NUM_THREADS) as pool:
        duplicatesExist = False
        arr = list(zip(files, pool.map(getFileHash, files)))
        for path, hashstr in arr:
            if not hashstr:
                if gs.VERBOSITY_LEVEL > 0:
                    print("Warning: File not found")
                    print("\t", str(path), "could be missing reference link")
                continue
            hashmap, de = appendHashmap(hashmap, hashstr, path)
            duplicatesExist = duplicatesExist or de
                
    return hashmap, duplicatesExist

def appendHashmap(hashmap: dict, key: str, value: str) -> Union[dict, bool]:
    return extendHashmap(hashmap, key, [value])

def extendHashmap(hashmap: dict, key: str, value: list) -> Union[dict, bool]:
    duplicatesExist = False
    if key in hashmap:
        duplicatesExist = True
        hashmap.get(key).extend(value)
    else:
        hashmap[key] = value
    
    return hashmap, duplicatesExist
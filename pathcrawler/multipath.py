from pathlib import Path
from hashlib import blake2b
from typing import Union
import argparse
import multiprocessing as mp
import time

# Verbosity Levels:
#   0 -> non-verbose
#   1 -> verbose
#   2 -> very verbose
global VERBOSITY_LEVEL
VERBOSITY_LEVEL = 0

def getFileHash(element: Path) -> str:
    with open(str(element),"rb") as f:
        bytes = f.read()
        hashstr = blake2b(bytes).hexdigest()
    f.close()
    return hashstr

def getMpFileHash(element: Path) -> Union[str,str]:
    hashstr = getFileHash(element)
    return str(element),hashstr

def addFileHashesIterative(path: Path, extensions=[]) -> Union[dict,bool]:
    hashmap = dict()
    dirs = [path]
    duplicatesExist = False
    files = []

    while dirs:
        if VERBOSITY_LEVEL > 0:
            print("Searching in " + str(path))
        path = dirs.pop()
        for el in path.iterdir():
            if VERBOSITY_LEVEL > 1:
                print(el)
            if el.is_dir():
                if el.parts[-1] in extensions: continue
                dirs.append(el)
            else:
                if el.suffix in extensions: continue
                files.append(el)
                #hashstr = getFileHash(el)
                #if hashstr in hashmap:
                #    duplicatesExist = True
                #    hashmap.get(hashstr).append(str(el))
                #else:
                #    hashmap[hashstr] = [str(el)]

    with mp.Pool(mp.cpu_count()) as pool:
        arr = pool.map(getMpFileHash, files)
        for path, hashstr in arr:
            if hashstr in hashmap:
                duplicatesExist = True
                hashmap.get(hashstr).append(path)
            else:
                hashmap[hashstr] = [path]

    return hashmap, duplicatesExist

if __name__ == "__main__":
    # Parse cmd line args
    parser = argparse.ArgumentParser(description="Find duplicate files.")
    parser.add_argument(
            "path",
            default="",
            nargs="?",
            type=str,
            help="path"
    )
    parser.add_argument(
            "-v", "--verbose",
            default=0,
            action="count",
            help="increases verbosity level by 1 (default is 0)"
    )
    parser.add_argument(
            "-x", "--exclude",
            action="extend",
            nargs="+",
            type=str,
            default=[],
            help="exclude file extension"
    )

    args = parser.parse_args()
    if args.verbose:
        VERBOSITY_LEVEL = args.verbose

    # Ask for path
    if not args.path:
        path = input("Insert a path (leave empty to start from the current directory): ")
    else:
        path = args.path
    while True:
        if Path(path).is_dir(): break
        if len(path) == 0:
            path = "."
            break
        path = input("Input not a directory, insert valid input: ")

    # Run
    t1 = time.time()
    hashmap, duplicatesExist = addFileHashesIterative(Path(path), args.exclude)
    t2 = time.time()

    # Show results
    if not duplicatesExist:
        print("\n\nNo duplicate files found.\n")
        exit()
    print("\n\nDuplicate files found:\n")
    for key in hashmap.keys():
        lista = hashmap[key]
        if not len(lista) == 1:
            print("=================")
            print(lista)
            print("=================")
    print("time: ", t2 - t1)

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

def addFileHashesRecursive(path: Path, extensions=[]) -> Union[dict,bool]:
    #init function
    if VERBOSITY_LEVEL > 0:
        print("Searching in " + str(path))
    hashmap = dict()
    dirs = list()
    duplicatesExist = False
    files = []

    #check if element is file or directory
    for el in path.iterdir():
        if VERBOSITY_LEVEL > 1:
            print(el)
        if el.is_dir():
            if el.parts[-1] in extensions: continue
            dirs.append(el)
        else:
            if el.suffix in extensions: continue
            #add hash at dictionary
            hashstr = getFileHash(el)
            if hashstr in hashmap:
                duplicatesExist = True
                hashmap.get(hashstr).append(str(el))
            else:
                hashmap[hashstr] = [str(el)]

    #call function recursively on subdirectories
    for subdir in dirs:
        h, de = addFileHashesRecursive(subdir, extensions)
        duplicatesExist = de or duplicatesExist
        for hashstr in h.keys():
            if hashstr in hashmap:
                duplicatesExist = True
                hashmap.get(hashstr).append(h.get(hashstr))
            else:
                hashmap[hashstr] = h.get(hashstr)
    return hashmap, duplicatesExist

def addFileHashesIterative(path: Path, extensions=[]) -> Union[dict,bool]:
    hashmap = dict()
    dirs = [path]
    duplicatesExist = False
    files = []

    while dirs:
        path = dirs.pop()
        if VERBOSITY_LEVEL > 0:
            print("Searching in " + str(path))
        for el in path.iterdir():
            if VERBOSITY_LEVEL > 1:
                print(el)
            if el.is_dir():
                if el.parts[-1] in extensions: continue
                dirs.append(el)
            else:
                if el.suffix in extensions: continue
                files.append(el)

    with mp.Pool(NUM_THREADS) as pool:
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
    parser.add_argument( #TODO mandatory
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
            "-r", "--recursive",
            default=False,
            action="store_true",
            help="use recorsion on the directories instead"
    )
    parser.add_argument(
            "-x", "--exclude",
            action="extend",
            nargs="+",
            type=str,
            default=[],
            help="exclude file extension"
    )
    parser.add_argument(
            "-t", "--threads",
            default=1,
            type=int,
            action="store",
            help="set number of processes - if more than cpu core, is set to cpu_count()"
    )

    # Set global values
    args = parser.parse_args()
    if args.verbose:
        VERBOSITY_LEVEL = args.verbose

    NUM_THREADS = min(args.threads, mp.cpu_count())

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
    if args.recursive:
        hashmap, duplicatesExist = addFileHashesRecursive(Path(path), args.exclude)
    else:
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

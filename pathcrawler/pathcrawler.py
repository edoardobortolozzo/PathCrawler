from pathlib import Path
from typing import Union
import argparse
import multiprocessing as mp
import time
import alessandria as lib

# Verbosity Levels:
#   0 -> non-verbose
#   1 -> verbose
#   2 -> very verbose
global VERBOSITY_LEVEL
VERBOSITY_LEVEL = 0

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
            files.append(el)

    #TODO FIXME chiamata funzione lib.updateHashmap()
    with mp.Pool(NUM_THREADS) as pool:
        arr = pool.map(lib.getMpFileHash, files)
        for path, hashstr in arr:
            if hashstr in hashmap:
                duplicatesExist = True
                hashmap.get(hashstr).append(path)
            else:
                hashmap[hashstr] = [path]

    #call function recursively on subdirectories
    for subdir in dirs:
        h, de = addFileHashesRecursive(subdir, extensions)
        duplicatesExist = de or duplicatesExist
        for hashstr in h.keys():
            path = h.get(hashstr)
            if hashstr in hashmap:
                duplicatesExist = True
                hashmap.get(hashstr).append(path)
            else:
                hashmap[hashstr] = path
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

    hashmap, duplicatesExist = lib.updateHashmap(hashmap, files)
    
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

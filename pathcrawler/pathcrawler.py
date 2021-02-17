from pathlib import Path
from hashlib import blake2b
from typing import Union
import argparse

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

    #check if element is file or directory
    for el in path.iterdir():
        if VERBOSITY_LEVEL > 1:
            print(el)
        if el.is_dir():
            dirs.append(el)
        else:
            if el.suffix in extensions: continue
            #add hash at dictionary
            with open(str(el),"rb") as f:
                bytes = f.read()
                hashstr = blake2b(bytes).hexdigest()
                if hashstr in hashmap:
                    duplicatesExist = True
                    hashmap.get(hashstr).append(str(el))
                else:
                    hashmap[hashstr] = [str(el)]
            f.close()
    #call function recursively on subdirectories
    for subdir in dirs:
        h, de = addFileHashesRecursive(subdir)
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

    while dirs:
        if VERBOSITY_LEVEL > 0:
            print("Searching in " + str(path))
        path = dirs.pop()
        for el in path.iterdir():
            if VERBOSITY_LEVEL > 1:
                print(el)
            if el.is_dir():
                dirs.append(el)
            else:
                if el.suffix in extensions: continue
                with open(str(el),"rb") as f:
                    bytes = f.read()
                    hashstr = blake2b(bytes).hexdigest()
                    if hashstr in hashmap:
                        duplicatesExist = True
                        hashmap.get(hashstr).append(str(el))
                    else:
                        hashmap[hashstr] = [str(el)]
                f.close()
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
    if args.recursive:
        hashmap, duplicatesExist = addFileHashesRecursive(Path(path), args.exclude)
    else:
        hashmap, duplicatesExist = addFileHashesIterative(Path(path), args.exclude)

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

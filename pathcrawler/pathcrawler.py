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

def addFileHashesRecursive(path: Path) -> Union[dict,bool]:
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

def addFileHashesIterative(path: Path) -> Union[dict,bool]:
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
            "-v", "--verbose",
            default=False,
            action="store_true",
            help="set verbosity level to 1 (default is 0)"
    )
    parser.add_argument(
            "-vv", "--veryverbose",
            default=False,
            action="store_true",
            help="set verbosity level to 2 (default is 0)"
    )
    parser.add_argument(
            "-r", "--recursive",
            default=False,
            action="store_true",
            help="use recorsion on the directories instead"
    )
    
    args = parser.parse_args()
    if args.verbose and args.veryverbose:
        print("Error: cannot use both `--verbose` and `--veryverbose`")
        exit(1)
    if args.verbose:
        VERBOSITY_LEVEL = 1
    elif args.veryverbose:
        VERBOSITY_LEVEL = 2

    # Ask for path
    path = input("Insert a path (leave empty to start from the current directory): ")
    while True:
        if Path(path).is_dir(): break
        if len(path) == 0:
            path = "."
            break
        path = input("Input not a directory, insert valid input: ")

    # Run
    if args.recursive:
        hashmap, duplicatesExist = addFileHashesRecursive(Path(path))
    else:
        hashmap, duplicatesExist = addFileHashesIterative(Path(path))

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

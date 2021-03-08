from pathlib import Path
import time
import global_settings as gs
from core import addFileHashesRecursive
from core import addFileHashesIterative
from arg_parser import parser

if __name__ == "__main__":
    # Set global values
    args = parser.parse_args()
    if args.verbose:
        gs.VERBOSITY_LEVEL = args.verbose

    if args.threads > 1:
        gs.setThreads(args.threads)

    if args.debug:
        gs.DEBUG = True

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
    if gs.DEBUG: t1 = time.time()
    if args.recursive:
        hashmap, duplicatesExist = addFileHashesRecursive(Path(path), args.exclude)
    else:
        hashmap, duplicatesExist = addFileHashesIterative(Path(path), args.exclude)
    if gs.DEBUG: t2 = time.time()

    # Show results
    if not duplicatesExist:
        print("\nNo duplicate files found.\n")
        exit()
    print("\nDuplicate files found:\n")
    for key in hashmap.keys():
        lista = hashmap[key]
        if not len(lista) == 1:
            print("=================")
            print(lista)
            print("=================")
    if gs.DEBUG: print("time: ", t2 - t1)

from pathlib import Path
from hashlib import blake2b

def addFileHashes(path: Path) -> dict:
    print("searching in " + str(path))
    hashmap = dict()
    dirs = list()
    for el in path.iterdir():
        print(el)
        if el.is_dir():
            dirs.append(el)
        else:
            with open(str(el),"rb") as f:
                bytes = f.read()
                hashstr = blake2b(bytes).hexdigest()
                if hashstr in hashmap:
                    hashmap.get(hashstr).append(str(el))
                else:
                    hashmap[hashstr] = [str(el)]
            f.close()
    for subdir in dirs:
        hashmap.update(addFileHashes(subdir))
    return hashmap

if __name__ == "__main__":
    path = input("insert path or nothing to start in the current subdirectory")
    if len(path) == 0:
        path = "."
    hashmap = addFileHashes(Path(path))
    print("\n\ncopies found:\n")
    for key in hashmap.keys():
        lista = hashmap[key]
        if not len(lista) == 1:
            print("=================")
            print(lista)
            print("=================")

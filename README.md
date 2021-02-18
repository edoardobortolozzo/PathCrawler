# PathCrawler

Given a path, the crawler explores every subdirectory and calculate the files'
hashes.
The hashes with the relative paths are saved in a dictionary in the form of
`[hash, list of paths with same data]`.
When ran as `__main__`, the script returns a list of paths where the duplicate
data is stored.

## Library functions
addFileHashes(path: Path, extensions=[]) -> Union[dict,bool]

getFileHash(element: Path) -> str

## Example
You can try the program with 

```shell
$ py pathcrawler [directory]
```

Or you can learn more on how to use the command with 
```shell
$ py pathcrawler -h
```

## Developing and installation
Unfortunatly the library ins't aviable on pip yet.
The plan at the moment is to publish it at version 2.0.

## Donations
If you like the project and you'd like to support the development, you can
buy a coffe to fuel the machines behind it.

[buy a coffe](https://www.buymeacoffee.com/safesintesi)
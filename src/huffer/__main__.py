from argparse import ArgumentParser
from sys import stdin
from os.path import exists, isfile

def get_character_frequency(string:str):
    counter = {}
    for char in string:
        counter[char] = counter.get(char, 0) + 1
    return counter

def get_stdin_character_frequency():
    try:
        return sorted([(k, v) for k,v in get_character_frequency(stdin.read()).items()], key=lambda x: x[1], reverse=True)
    except Exception:
        return []

def get_file_character_frequency(path:str):
    counter = {}
    with open(path, "r") as file:
        for line in file:
            line_counter = get_character_frequency(line)
            for k in line_counter.keys():
                counter[k] = counter.get(k, 0) + line_counter[k]
    return sorted([(k, v) for k,v in counter.items()], key=lambda x: x[1], reverse=True)

def get_file_details(path:str):
    res = {
        "exists": exists(path),
        "is_file": False
    }

    if res["exists"]:
        res["is_file"] = isfile(path)
    
    return res

def main():
    parser = ArgumentParser("huffer", description="A huffman encoder/decoder written in python")
    parser.add_argument("FILE", type=str, nargs="*", help="the FILE(s) to be processed, if FILE is not provided or is - STDIN is used")
    
    args = parser.parse_args()

    if not args.FILE:
        char_freq = get_stdin_character_frequency()
        print(char_freq)
    else:
        char_freq = None
        for f in args.FILE:
            if f == "-":
                char_freq = get_stdin_character_frequency()
            else:
                file_details = get_file_details(f)
                if not file_details["exists"]:
                    print(f"{parser.prog}: {f}: No such file or directory")
                    continue
                if not file_details["is_file"]:
                    print(f"{parser.prog}: {f}: Is a directory")
                    continue

                char_freq = get_file_character_frequency(f)
            print(char_freq)
            

if __name__ == "__main__":
    main()

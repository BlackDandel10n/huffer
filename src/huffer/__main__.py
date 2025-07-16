from argparse import ArgumentParser
from sys import stdin
from os.path import exists, isfile
from os import access as os_access, R_OK, W_OK


class HuffNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right
   

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
        "is_file": False,
        "can_read": False,
        "can_write": False
    }

    if res["exists"]:
        res["is_file"] = isfile(path)
        res["can_read"] = os_access(path, R_OK)
        res["can_write"] = os_access(path, W_OK)
    
    return res


def get_huff_freq_node(left=None, right=None):
    left_freq = left[1] if left else 0
    left = left[0] if left else left
    right_freq = right[1] if right else 0
    right = right[0] if right else right
    return (HuffNode(left, right), right_freq + left_freq)


def get_huff_tree(char_freq_list):
    if len(char_freq_list) == 0:
        return None
    
    char_freq_list = char_freq_list[:]
    if len(char_freq_list) == 1:
        return HuffNode(None, char_freq_list.pop()[0])
    
    while len(char_freq_list) > 1:
        right = char_freq_list.pop()
        left = char_freq_list.pop()
        char_freq_list.append(get_huff_freq_node(left, right))
        char_freq_list.sort(key=lambda x: x[1], reverse=True)

    return char_freq_list.pop()[0]


def main():
    parser = ArgumentParser("huffer", description="A huffman encoder/decoder written in python")
    parser.add_argument("FILE", type=str, nargs="*", help="the FILE(s) to be processed, if FILE is not provided or is - STDIN is used")
    
    args = parser.parse_args()

    if not args.FILE:
        char_freq = get_stdin_character_frequency()
        huff_tree = get_huff_tree(char_freq)
        print(huff_tree)
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
                if not file_details["can_read"]:
                    print(f"{parser.prog}: {f}: Permission denied")
                    continue

                char_freq = get_file_character_frequency(f)
            
            huff_tree = get_huff_tree(char_freq)
            print(huff_tree)
            

if __name__ == "__main__":
    main()

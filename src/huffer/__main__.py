def get_character_frequency(string:str):
    counter = {}
    for char in string:
        counter[char] = counter.get(char, 0) + 1
    return counter

def get_file_character_frequency(path:str):
    counter = {}
    with open(path, "r") as file:
        for line in file:
            line_counter = get_character_frequency(line)
            for k in line_counter.keys():
                counter[k] = counter.get(k, 0) + line_counter[k]
    return counter

import os

def dfsfilepath(the_path):
    all_file_path = []
    arr = os.listdir(the_path)
    for el in arr:
        if(os.path.isdir(os.path.join(the_path, el))):
            all_file_path.extend(dfsfilepath(os.path.join(the_path, el)))
        elif(os.path.isfile(os.path.join(the_path, el))):
            if el[-4:] == ".php":
                all_file_path.append(os.path.join(the_path, el))
    return all_file_path
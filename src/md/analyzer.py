import re

from mdp.ClassLibrary import PHPClass

def readFile(filename:str) -> str:
    with open(filename, "r") as f:
        source_code = f.read()
    return source_code

def removeComment(txt:str) -> str:
    txt = re.sub(re.compile("/\*.\*/", re.DOTALL), "", txt)
    txt = re.sub(re.compile("//.*?\n"), "", txt)
    return txt


def getClassName(source_code:str) -> str:
    pattr = r"[cC][lL][aA][sS][sS]"
    matchs = re.finditer(pattr, source_code)
    buff = ""
    for mtch in matchs:
        idx = mtch.start()
        while(re.match(r"[cClLaAsS]", source_code[idx])):
            idx += 1
        while not (re.match(r"[a-zA-Z0-9_]", source_code[idx])):
            idx += 1
        while (re.match(r"[a-zA-Z0-9_]", source_code[idx])):
            buff += source_code[idx]
            idx += 1
        break
    
    if len(buff) < 1:
        buff = ""
        pattr = r"[iI][nN][tT][eE][rR][fF][aA][cC][eE]"
        matchs = re.finditer(pattr, source_code)
        buff = ""
        for mtch in matchs:
            idx = mtch.start()
            while(re.match(r"[iInNtTeErRfFaAcCeE]", source_code[idx])):
                idx += 1
            while not (re.match(r"[a-zA-Z0-9_]", source_code[idx])):
                idx += 1
            while (re.match(r"[a-zA-Z0-9_]", source_code[idx])):
                buff += source_code[idx]
                idx += 1
            break

    if len(buff) < 1:
        buff = ""
        pattr = r"[tT][rR][aA][iI][tT]"
        matchs = re.finditer(pattr, source_code)
        buff = ""
        for mtch in matchs:
            idx = mtch.start()
            if idx - 1 > 0 and source_code[idx-1] == "\\":
                continue
            while(re.match(r"[tTrRaAiItT]", source_code[idx])):
                idx += 1
            while not (re.match(r"[a-zA-Z0-9_]", source_code[idx])):
                idx += 1
            while (re.match(r"[a-zA-Z0-9_]", source_code[idx])):
                buff += source_code[idx]
                idx += 1
            break

    return buff

def getNamespace(source_code:str) -> str:
    pattr = r"[nN][aA][mM][eE][sS][pP][aA][cC][eE]"
    matchs = re.finditer(pattr, source_code)
    buff = ""
    for mtch in matchs:
        idx = mtch.start()
        while(re.match(r"[namespaceNAMESPACE]", source_code[idx])):
            idx += 1
        while not (re.match(r"[a-zA-Z0-9_\\]", source_code[idx])):
            idx += 1
        while (re.match(r"[a-zA-Z0-9_\\]", source_code[idx])):
            buff += source_code[idx]
            idx += 1
        break
    return buff

def getReferences(source_code:str) -> list:
    pattr = r"[uU][sS][eE]\b"
    matchs = re.finditer(pattr, source_code)
    references = []
    for mtch in matchs:
        buff = ""
        idx = mtch.start()
        while(re.match(r"[useUSE]", source_code[idx])):
            idx += 1
        while (re.match(r"\s", source_code[idx])):
            idx += 1
        while (re.match(r"[a-zA-Z0-9_\\]", source_code[idx])):
            buff += source_code[idx]
            idx += 1
        if len(buff) > 0:
            buff = re.sub(r'\\', '#', buff)
            references.append(buff)
    return references        


def extractClassFromFile(filename:str) -> PHPClass:
    sc = readFile(filename)
    sc = removeComment(sc)
    class_name = getClassName(sc)
    namespace = getNamespace(sc)
    references = getReferences(sc)
    php_class = PHPClass(class_name, namespace, references)

    for r in references:
        temp = r + ';'
        pattr = r"\\*([a-zA-Z0-9_]+)[;]"
        search_reg = re.search(pattr, temp)
        keyword = search_reg.group(1)
        pattr = r"\b" + keyword + r"\b"
        number_of_occurences = len(list(re.finditer(pattr, sc)))
        php_class.reference_occurrences[r] = number_of_occurences

    return php_class

########################################################################################
# ref_dict = {}

# for r in references:
#     temp = r + ';'
#     pattr = r"\\*([a-zA-Z0-9_]+)[;]"
#     search_reg = re.search(pattr, temp)
#     keyword = search_reg.group(1)
#     pattr = r"\b" + keyword + r"\b"
#     number_of_occurences = len(list(re.finditer(pattr, sc)))
#     ref_dict[keyword] = number_of_occurences

# for r in ref_dict:
#     print(r, ref_dict[r])
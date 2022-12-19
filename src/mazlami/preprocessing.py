import re

PHP_reserved_words = ['const', 'and', '$argv', '$argc', 'break', 'case', 'class', 'Class', 'CLASS', 'continue', 'default', 'do', 'die()', 'echo()', 'else', 'elseif', 'empty()', 'endfor', 'endforeach', 'endif', 'endswitch', 'endwhile', 'E_ALL', 'E_PARSE', 'E_ERROR', 'E_WARNING', 'exit()', 'extends', 'FALSE', 'for', 'foreach', 'function', '$HTTP_COOKIE_VARS', '$HTTP_GET_VARS', '$HTTP_POST_VARS', '$$HTTP_POST_FILES', '$HTTP_ENV_VARS', '$HTTP_SERVER_VARS', 'if', 'include()', 'include_once()', 'global', 'list()', 'new', 'not', 'NULL', 'or', 'parent', 'PHP_OS', '$PHP_SELF', 'PHP_VERSION', 'print()', 'require()', 'require_once()', 'return', 'static', 'switch', 'stdClass', '$this', 'TRUE', 'var', 'xor', 'virtual()', 'while', '__FILE__', '__LINE__', '__sleep', '__wakeup', 'try', 'public', 'private', 'protected', 'catch', 'use', 'namespace']

def unusedLaravelFunction():
    unusedLaravelFunction = [
        '$this#belongsTo',
        '$this#hasMany',
        'number_format',
        '$this#hasone',
        '$this#hasOne',
        '$this#getKeyName',
        '$this#getAttribute',
        '#where',
        '#where',
        '#orwhere',
        '#orwhere',
        '#orWhere',
        '#orWhere',
        'auth',
        'Auth#',
        'compact',
        'view',
        '#with',
        '#with',
        'redirect',
        'count',
        'DB#',
        '#save',
        '#save',
        '#delete',
        '#delete',
        '#findorfail',
        '#findorfail',
        '#findOrFail',
        '#create',
        '#update',
        '#update',
        '#updateOrCreate',
        '#updateOrCreate',
        '#find',
        '#find',
        '#input',
        'collect',
        'distinct',
        '#json',
        '#file',
        '#file',
        "#has",
        '#orWhere',
        "SELECTCOUNT",
        "GETDATE",
        "DATEDIFF",
        'config',
        '#all',
        '#all',
        'dd',
        '#sum',
        '#sum',
        '#hasFile',
        '#isEmpty',
        '#ajax',
        '#upload',
        'session',
        '#user',
        'route',
        '#exists',
        '#unique',
        '#is',
        '#select',
        "Exception",
        "#authorize",
        "whereIn",
        'request',
        "#get",
        "\\Log#error",
        "\\Exception",
        "Auth#login",
        "Auth#logout"

    ]
    return unusedLaravelFunction


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
    buff = buff.replace("\\", '#')
    return buff

def removeComment(txt:str) -> str:
    txt = re.sub(re.compile("/\*.\*/", re.DOTALL), "", txt)
    txt = re.sub(re.compile("//.*?\n"), "", txt)
    return txt


def readFile(file_name:str) -> str:
    txt = ""
    with open(file_name, "r") as f:
        txt = f.read()
    return txt

def cleanSourceCode(src: str) -> str:

    src = removeComment(src)

    pattr = '[cC][Ll][aA][sS][sS]'
    mtchs = re.finditer(pattr, src)
    for mtch in mtchs:
        idx = mtch.start()
        src = src[mtch.start():]
        break
    # print(src)

    for word in PHP_reserved_words:
        pat = re.compile(r'(\b)' + word + r'(\b)')
        src = pat.sub(r"\1\2", src)

    src = re.sub(r"::", "#", src)
    src = re.sub(r"->", "#", src)

    src = re.sub(r"[\(\)]", " ", src)

    unused_laravel_funct = unusedLaravelFunction()

    src = " " + src + " "

    for word in unused_laravel_funct:
        word = " " + word + " "
        src = src.replace(word, " ")

    src = re.sub(r"[\:\;\+\&\-\$\%\^\&\*\(\)\<\>\?\/\=\{\[\}\]\!\.\,\|\'\"\#]", " ", src)
    src = re.sub(r"\s\s+", r" ", src)
    src = src.upper()

    return src


class PHPClass:
    def __init__(self) -> None:
        self.name = None
        self.definition = None

# src1 = readFile("AdminController.php")
# src1 = cleanSourceCode(src1)

# src2 = readFile("Mahasiswa.php")
# src2 = cleanSourceCode(src2)

# vectorizer = TfidfVectorizer()
# vectors = vectorizer.fit_transform([src1, src2])
# # featur

def extract(filename:str) -> str:
    src = readFile(filename)
    class_name = getClassName(src)
    namespace = getNamespace(src)
    src = cleanSourceCode(src)
    return [namespace + "#" + class_name, src]





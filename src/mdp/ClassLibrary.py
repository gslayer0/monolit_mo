import re

class PHPClass:
    def __init__(self, name:str, namespace:str, references:list) -> None:
        if len(name) < 1:
            pass
        self.name = name
        if len(namespace) < 1:
            self.fullname = name
            self.namespace = None
        else:
            self.fullname = namespace + "\\" + name
            self.namespace = namespace
        self.references = references
        self.reference_occurrences = {}
        self.fullname = re.sub(r'\\',"#", self.fullname)
    
    def getRO(self) -> dict:
        return self.reference_occurrences


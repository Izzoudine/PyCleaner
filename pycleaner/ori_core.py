
def clean_imports(file):
    unused_imports = get_unused_imports(file)
    if unused_imports is None:
        return "Your imports are already clean!!!"
    
def get_unused_imports(file):
    content = read(file)
    unused_imports = {}
    index = 0
    for line in content:
        if 'import' in line:
            modules = next_word('import',line)
            if modules:
                for module in modules:
                    mutiple_modules(module, unused_imports, content, index)
                    
        index += 1
    return unused_imports    
                
def read(file):
    with open(file, "r") as f:
        content = f.read()
    return content

def next_word(word = 'word', line = 'Find a word'):
    start = line.find(word)    
    after_target = line[start + len(word):].strip()
    return after_target.split() if after_target else None


def mutiple_modules(module, unused_imports,content , index):
    if is_used(module, content) == False:
        unused_imports.append({"index" : index, "module" : module})

def is_used(module, content):
    usages = 0
    for line in content:
        if usages > 1:
            return True    
        if module in line:
            usages += 1
    return False        





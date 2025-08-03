from pathlib import Path
import re
CURRENT_DIRECTORY = Path(__file__).resolve().parent

file = CURRENT_DIRECTORY / "database.py"



def clean_import(file):
    clean_ = get_clean_import(file)
    write(file,clean_)
    

def get_clean_import(file):
    content = read(file)
    filtered_content = []
    in_multiline = False
    buffer = []
    for line in content:
        stripped = line.strip()
        if stripped.startswith('import ') and ' as ' not in stripped:
            modules = next_words('import',line)
            print(modules)
            kept = [m.strip() for m in modules if(is_used(m.strip(), content))]   
            if kept:  
                filtered_content.append('import '+ ', '.join(kept))     
        elif stripped.startswith('from ') and ' as ' not in stripped:
            parts = stripped.split('import')
            module = parts[0].replace("from",'').strip()
            modules = [m.strip() for m in parts[1].split(',')]
            kept = [m for m in modules if(is_used(m, content))]
            if kept:
                filtered_content.append(f'from {module}' + ' import '+', '.join(kept))

        elif stripped.startswith('from ') and '(' in stripped:
             in_multiline = True
             buffer = [line]
             continue
        elif in_multiline:
             buffer.append(line)
             if ')' in stripped:
                 in_multiline = False
                 full_import = "\n".join(buffer)
                 cleaned = clean_multiline_import(full_import, content)
                 if cleaned:
                     filtered_content.append(cleaned)
                 buffer = []    
             continue
                  
        elif ' as ' in stripped:
            parts = stripped.split(' as ')

            module = next_word(' as ', line)
            if(is_used(module, content)):
                filtered_content.append(parts[0].strip() + ' as ' + module)
        else:   
            filtered_content.append(line)
    return filtered_content

def clean_multiline_import(import_block, content):
    lines = import_block.splitlines()

    head = lines[0]
    tail = lines[1:-1]
    end = lines[-1]     

    used_imports = []

    for line in tail:
        module = line.strip().rstrip(',')
        if is_used(module, content):
            used_imports.append(f"    {module},")

    if not used_imports:
        return ''
    return '\n'.join([head] + used_imports + [end])        


def write(file, filtered_content):
    with open (file, 'w') as f:
        f.writelines(line + '\n' for line in filtered_content)  
                
def read(file):
    with open(file, "r") as f:
        content = f.read().splitlines()
    return content

def next_words(word, line):
    start = line.find(word)    
    after_target = line[start + len(word):].strip()
    return after_target.split(',')
def next_word(word, line):
    start = line.find(word)    
    after_target = line[start + len(word):].strip()
    return after_target if after_target else None


def is_used(module, content):
    pattern = r'\b' + re.escape(module) + r'\b'
    for line in content:
        if 'import' in line:
            continue
        if re.search(pattern, line):
            return True
    return False    


clean_import(file)


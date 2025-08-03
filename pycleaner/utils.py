import re
import logging
logger = logging.getLogger(__name__)


def get_clean_import(file):
    content = read(file)
    filtered_content = []
    in_multiline = False
    buffer = []
    for line in content:
        stripped = line.strip()

        if in_multiline:
             
            buffer.append(line)
            if ')' in stripped:
                 
                 in_multiline = False
                 full_import = "\n".join(buffer)
                 cleaned = clean_multiline_import(full_import, content)

                 if cleaned:
                     filtered_content.append(cleaned)
                 buffer = []    
            continue
        
        if ' as ' in stripped:
            parts = stripped.split(' as ')

            module = next_word(' as ', line)
            if(is_used(module, content)):
                filtered_content.append(parts[0].strip() + ' as ' + module)
            continue    


        if stripped.startswith('import '):
            modules = next_words('import',line)
            print(modules)
            kept = [m.strip() for m in modules if(is_used(m.strip(), content))]   
            if kept:  
                filtered_content.append('import '+ ', '.join(kept)) 
            continue

        if stripped.startswith('from '):
            if '(' in stripped:
                in_multiline = True
                buffer = [line]
                continue
            parts = stripped.split('import')
            if len(parts) < 2:
                continue
            module = parts[0].replace("from",'').strip()
            modules = [m.strip() for m in parts[1].split(',')]
            kept = [m for m in modules if(is_used(m, content))]
            if kept:
                filtered_content.append(f'from {module}' + ' import '+', '.join(kept))
            continue                             
    
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
    in_multiline_import = False
    logger.debug(f"Checking usage of: {module}")

    for line in content:
        stripped = line.strip()

        if 'import' in stripped and '(' in stripped:
            in_multiline_import = True
            continue

        if in_multiline_import:
            if ')' in stripped:
                in_multiline_import = False
            continue

        if 'import' in stripped:
            continue

        if re.search(pattern, stripped):
            logger.debug(f"✔ {module} is used in: {line.strip()}")
            return True
    logger.debug(f"✘ {module} is NOT used")
    return False



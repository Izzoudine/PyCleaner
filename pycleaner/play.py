
text = "The quick brown fox jumps, over the lazy dog"
target = "fox"
import re

   

def m3():
    start = text.find(target)
    if start != -1:
        after_target = text[start + len(target):].strip()
        next_word = after_target.split()[0] if after_target else None
        print(next_word) 

def is_used(module, content):
    pattern = r'\b' + re.escape(module) + r'\b'
    for line in content:
        if 'import' in line:
            continue
        if re.search(pattern, line):
            return True
    return False


content = [
    "import numpy as np",
    "import pandas as pd",
    "data = np.array([1, 2, 3])",
    "print(data)"
]

print(is_used('np', content))  # True
print(is_used('pd', content))  # False (pandas was imported but never used)



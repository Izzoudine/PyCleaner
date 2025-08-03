
text = "The quick brown fox jumps, over the lazy dog"
target = "fox"

   

def m3():
    start = text.find(target)
    if start != -1:
        after_target = text[start + len(target):].strip()
        next_word = after_target.split()[0] if after_target else None
        print(next_word) 

m3()        

if target in text:
    print("It's in")
text.replace(target, " ")
print(text)


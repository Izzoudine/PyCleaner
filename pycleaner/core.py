from .utils import get_clean_import,write

def clean_import(file):
    clean_ = get_clean_import(file)
    write(file,clean_)
    


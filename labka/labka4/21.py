import importlib

def process_query(module_path, attribute):
    try:
        module = importlib.import_module(module_path)
    except:
        return "MODULE_NOT_FOUND"
    
    if not hasattr(module, attribute):
        return "ATTRIBUTE_NOT_FOUND"
    
    attr = getattr(module, attribute)
    
    if callable(attr):
        return "CALLABLE"
    else:
        return "VALUE"

q = int(input())
for _ in range(q):
    parts = input().split()
    module_path = parts[0]
    attribute = parts[1]
    print(process_query(module_path, attribute))
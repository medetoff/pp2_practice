import json

def deep_diff(obj1, obj2, path=""):
    differences = []
    
    if isinstance(obj1, dict) and isinstance(obj2, dict):
        all_keys = set(obj1.keys()) | set(obj2.keys())
        
        for key in all_keys:
            new_path = f"{path}.{key}" if path else key
            
            if key not in obj1:
                val2 = json.dumps(obj2[key], separators=(',', ':'))
                differences.append((new_path, "<missing>", val2))
            elif key not in obj2:
                val1 = json.dumps(obj1[key], separators=(',', ':'))
                differences.append((new_path, val1, "<missing>"))
            else:
                differences.extend(deep_diff(obj1[key], obj2[key], new_path))
    else:
        if obj1 != obj2:
            val1 = json.dumps(obj1, separators=(',', ':'))
            val2 = json.dumps(obj2, separators=(',', ':'))
            differences.append((path, val1, val2))
    
    return differences

obj1 = json.loads(input())
obj2 = json.loads(input())

diffs = deep_diff(obj1, obj2)

if not diffs:
    print("No differences")
else:
    diffs.sort(key=lambda x: x[0])
    for path, old_val, new_val in diffs:
        print(f"{path} : {old_val} -> {new_val}")
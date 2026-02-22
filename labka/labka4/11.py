import json

def apply_patch(source, patch):

    if not isinstance(source, dict):
        source = {}
    
    result = dict(source)
    
    for key, patch_value in patch.items():
        if patch_value is None:
            if key in result:
                del result[key]
        elif key in result and isinstance(result[key], dict) and isinstance(patch_value, dict):

            result[key] = apply_patch(result[key], patch_value)
        else:
            result[key] = patch_value
    
    return result

def sort_json(obj):
    if isinstance(obj, dict):
        return {k: sort_json(v) for k, v in sorted(obj.items())}
    elif isinstance(obj, list):
        return [sort_json(item) for item in obj]
    else:
        return obj

source = json.loads(input())
patch = json.loads(input())

result = apply_patch(source, patch)
sorted_result = sort_json(result)
print(json.dumps(sorted_result, separators=(',', ':')))
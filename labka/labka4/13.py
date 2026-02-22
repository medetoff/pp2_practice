import json

def parse_query(query):
    tokens = []
    i = 0
    while i < len(query):
        if query[i] == '.':
            i += 1
        elif query[i] == '[':
            j = i + 1
            while j < len(query) and query[j] != ']':
                j += 1
            index = int(query[i+1:j])
            tokens.append(('index', index))
            i = j + 1
        else:
            j = i
            while j < len(query) and query[j] not in '.[]':
                j += 1
            if j > i:
                tokens.append(('key', query[i:j]))
            i = j
    return tokens

def resolve_query(data, query):
    if not query:
        return (True, data)
    
    tokens = parse_query(query)
    current = data
    
    for token_type, token_value in tokens:
        try:
            if token_type == 'key':
                if isinstance(current, dict) and token_value in current:
                    current = current[token_value]
                else:
                    return (False, None)
            elif token_type == 'index':
                if isinstance(current, list) and 0 <= token_value < len(current):
                    current = current[token_value]
                else:
                    return (False, None)
        except:
            return (False, None)
    
    return (True, current)

data = json.loads(input())
n = int(input())

for _ in range(n):
    query = input().strip()
    found, result = resolve_query(data, query)
    
    if not found:
        print("NOT_FOUND")
    else:
        print(json.dumps(result, separators=(',', ':')))
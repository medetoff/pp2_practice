import json
import os

def load_json(filename, default):
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        save_json(filename, default)
        return default
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Добавляем отсутствующие ключи
            for key, value in default.items():
                if key not in data:
                    data[key] = value
            return data
    except Exception:
        print(f"⚠️ Ошибка чтения {filename}. Создаём новый файл.")
        save_json(filename, default)
        return default


def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
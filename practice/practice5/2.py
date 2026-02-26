import re
import json
import os

def parse_receipt(content):
    result = {
        "store": re.search(r'Филиал\s+(.+)', content).group(1).strip(),
        "BIN": re.search(r'БИН\s+(\d+)', content).group(1),
        "receipt_number": re.search(r'Чек\s*№(\d+)', content).group(1),
        "date": re.search(r'Время:\s*(\d{2}\.\d{2}\.\d{4})', content).group(1),
        "time": re.search(r'\d{2}\.\d{2}\.\d{4}\s+(\d{2}:\d{2}:\d{2})', content).group(1),
        "payment_method": "Банковская карта" if "Банковская карта" in content else "Наличные",
        "total": float(re.search(r'ИТОГО:\s*\n?([\d\s]+)', content).group(1).replace(' ', '')),
        "products": []
    }
    
    products = re.findall(r'(\d+)\.\s*\n?(.+?)\n([\d,]+)\s*x\s*([\d\s,]+)\n([\d\s,]+)', content)
    for p in products:
        result["products"].append({
            "name": p[1].strip(),
            "qty": float(p[2].replace(',', '.')),
            "price": float(p[4].replace(' ', '').replace(',', '.'))
        })
    
    result["all_prices"] = [p["price"] for p in result["products"]]
    result["calculated_total"] = sum(result["all_prices"])
    
    return result

# Получаем путь к директории скрипта
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'raw.txt')

# Проверяем существование файла
if not os.path.exists(file_path):
    print(f"Файл не найден: {file_path}")
    print(f"Создайте файл raw.txt в папке: {script_dir}")
    exit(1)

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

data = parse_receipt(content)

print(f"Магазин: {data['store']}")
print(f"Дата: {data['date']} {data['time']}")
print(f"Оплата: {data['payment_method']}")
print(f"\nТовары ({len(data['products'])} шт.):")
for p in data["products"]:
    print(f"  - {p['name'][:40]}: {p['price']:.2f}")
print(f"\nВсе цены: {data['all_prices']}")
print(f"Итого: {data['total']:.2f}")
print(f"\nJSON:\n{json.dumps(data, ensure_ascii=False, indent=2)}")
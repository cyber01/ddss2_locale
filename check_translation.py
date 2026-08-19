"""
  Данный скрипт создан для того, чтобы упростить задачу проверки перевода,
  он сверяет ключи в файле английской и русской локализаций,
  возвращая список отсутствующих и лишних ключей,
  так же он сортирует файл русской локализации в
  соответсвии с английской (лишние ключи отправляет в конец)
"""

import json
import re
from collections import OrderedDict

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def find_duplicates(keys):
    from collections import Counter
    counter = Counter(keys)
    return [k for k, count in counter.items() if count > 1]

def main():
    en_file = 'en_us.json'
    ru_file = 'ru_ru.json'
    output_ordered = 'ru_ru_ordered.json'

    # Проверка дублей в ru_ru.json
    with open(ru_file, 'r', encoding='utf-8') as f:
        ru_text = f.read()
    key_pattern = r'"([^"\\]+)"\s*:'
    raw_keys = re.findall(key_pattern, ru_text)
    duplicates = find_duplicates(raw_keys)
    if duplicates:
        print(f"Обнаружены дублирующиеся ключи: {len(set(duplicates))}")
        print("Список дублирующихся ключей:")
        for k in set(duplicates):
            print(f"  {k}")
        print("Автоматически удалены дубли (оставлено последнее значение).")

    ru = load_json(ru_file)
    en = load_json(en_file)

    en_keys = list(en.keys())
    ru_keys = set(ru.keys())

    # 1. Отсутствующие ключи (нет в ru)
    absent = []
    for k in en_keys:
        if k not in ru_keys:
            absent.append(k)

    # 2. Пустые ключи (есть в ru, но значение пустое или None)
    empty = []
    for k in en_keys:
        if k in ru_keys:
            val = ru.get(k)
            if val is None or val == '':
                empty.append(k)

    # 3. Лишние ключи (есть в ru, нет в en)
    extra = [k for k in ru_keys if k not in en]

    print(f"\nВсего ключей в оригинале: {len(en_keys)}")
    print(f"Всего ключей в переводе: {len(ru_keys)}")
    print(f"Отсутствующих ключей (нет в переводе): {len(absent)}")
    if absent:
        print("\n--- Отсутствующие ключи (нужно добавить) ---")
        for k in absent:
            print(k)
    else:
        print("✅ Все ключи присутствуют!")

    print(f"\nПустых значений (есть ключ, но нет перевода): {len(empty)}")
    if empty:
        print("--- Ключи с пустым значением (требуют перевода) ---")
        for k in empty:
            print(k)
    else:
        print("✅ Нет пустых значений.")

    if extra:
        print(f"\n--- Лишние ключи (есть в переводе, нет в оригинале): {len(extra)} ---")
        for k in extra:
            print(k)
    else:
        print("✅ Нет лишних ключей.")

    # Упорядочивание
    ordered_ru = OrderedDict()
    for k in en_keys:
        ordered_ru[k] = ru.get(k, '')
    for k in extra:
        ordered_ru[k] = ru.get(k, '')

    save_json(output_ordered, ordered_ru)
    print(f"\n✅ Упорядоченный перевод сохранён в {output_ordered}")

if __name__ == '__main__':
    main()
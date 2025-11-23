from bs4 import BeautifulSoup

with open("page.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file.read(), 'html.parser')

print("Парсинг лотов...")

lots = []

# Ищем все элементы с ценами
for price_elem in soup.find_all(string=lambda text: text and 'руб.' in text):
    # Находим родительскую строку таблицы
    row = price_elem.find_parent('tr')
    
    if row:
        cells = row.find_all('td')
        
        if len(cells) >= 4:
            try:
                # НАЗВАНИЕ - из текста ссылки
                link_tag = row.find('a')
                if link_tag and link_tag.text.strip():
                    name = link_tag.text.strip()
                else:
                    name = "Неизвестный лот"
                
                # Цена
                price_text = price_elem.strip()
                price = float(price_text.replace(' руб.', '').replace(' ', '').replace(',', '.'))
                
                # Ссылка
                link = link_tag['href'] if link_tag and link_tag.get('href') else "Нет ссылки"
                if link.startswith('/') or link.startswith('?'):
                    link = "https://torgi.org/" + link
                
                lots.append({'name': name, 'price': price, 'link': link})
                print(f"Найден: {name[:50]}... - {price:,.0f} руб.")
                
            except Exception as e:
                continue

print(f"\nНайдено лотов: {len(lots)}")

if lots:
    # Сортировка от дорогого к дешёвому
    lots.sort(key=lambda x: x['price'], reverse=True)
    
    # Вывод всех лотов
    print("\n" + "="*50)
    print("ВСЕ ЛОТЫ (от самого дорогого к самому дешёвому):")
    print("="*50)
    for i, lot in enumerate(lots, 1):
        print(f"{i}. {lot['name']}")
        print(f"   Цена: {lot['price']:,.2f} руб.")
        print(f"   Ссылка: {lot['link']}\n")
    
    # Фильтрация по цене
    print("="*50)
    print("ФИЛЬТРАЦИЯ ПО ЦЕНЕ")
    print("="*50)
    try:
        min_price = float(input("Введите минимальную цену: ") or 0)
        max_price = float(input("Введите максимальную цену: ") or 999999999)
        
        filtered_lots = [lot for lot in lots if min_price <= lot['price'] <= max_price]
        
        print(f"\nНайдено лотов в диапазоне {min_price:,.2f} - {max_price:,.2f} руб.: {len(filtered_lots)}")
        print("-" * 50)
        
        for i, lot in enumerate(filtered_lots, 1):
            print(f"{i}. {lot['name']}")
            print(f"   Цена: {lot['price']:,.2f} руб.")
            print(f"   Ссылка: {lot['link']}\n")
            
    except ValueError:
        print("Ошибка ввода цены!")
else:
    print("Лоты не найдены")
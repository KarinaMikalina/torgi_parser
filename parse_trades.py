from bs4 import BeautifulSoup
import sys

def main():
    print("🎯 Парсер торгов запущен!")
    
    try:
        # Читаем файл
        with open('page.html', 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        print(f" Файл прочитан: {len(html_content)} символов")
        
        # Парсим HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Ищем все контейнеры с лотами
        lot_containers = soup.find_all('div', class_='lot-item')
        print(f"🔍 Найдено контейнеров: {len(lot_containers)}")
        
        lots = []
        
        for container in lot_containers:
            # Название
            name_tag = container.find('a', class_='lot-title')
            name = name_tag.get_text(strip=True) if name_tag else 'Без названия'
            
            # Цена
            price_tag = container.find('div', class_='lot-price')
            price_text = price_tag.get_text(strip=True) if price_tag else '0'
            
            # Очищаем цену
            price_clean = price_text.replace(' ', '').replace('₽', '').replace(',', '.')
            try:
                price = float(price_clean)
            except ValueError:
                price = 0.0
            
            # Ссылка
            link_tag = container.find('a', class_='lot-title')
            relative_link = link_tag.get('href') if link_tag else '#'
            link = f"https://torgi.gov.ru{relative_link}" if relative_link.startswith('/') else relative_link
            
            lots.append({
                'name': name,
                'price': price,
                'link': link
            })
            
            print(f" Лот: {name} - {price:,.0f} руб.")
        
        # Сортируем
        sorted_lots = sorted(lots, key=lambda x: x['price'], reverse=True)
        
        print(f"\n📊 ВСЕГО ЛОТОВ: {len(sorted_lots)}")
        print("🏆 ТОП-3 самых дорогих:")
        for i, lot in enumerate(sorted_lots[:3], 1):
            print(f"  {i}. {lot['name']} - {lot['price']:,.0f} руб.")
        
        # Фильтрация
        print("\n ФИЛЬТР ПО ЦЕНЕ")
        try:
            min_price = float(input("Введите МИНИМАЛЬНУЮ цену: "))
            max_price = float(input("Введите МАКСИМАЛЬНУЮ цену: "))
            
            filtered = [lot for lot in sorted_lots if min_price <= lot['price'] <= max_price]
            
            print(f"\n✅ Найдено {len(filtered)} лотов в диапазоне {min_price:,.0f} - {max_price:,.0f} руб.:")
            for i, lot in enumerate(filtered, 1):
                print(f"  {i}. {lot['name']} - {lot['price']:,.0f} руб.")
                
        except ValueError:
            print("❌ Ошибка! Вводите только числа.")
            
    except FileNotFoundError:
        print("❌ ОШИБКА: Файл page.html не найден!")
        print(" Убедитесь что файл находится в той же папке")
    except Exception as e:
        print(f"❌ ОШИБКА: {e}")

if __name__ == "__main__":
    main()
    print("\n✨ Программа завершена")
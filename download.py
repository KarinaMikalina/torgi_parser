import requests

def download_page():
    url = "https://torgi.gov.ru/opendata/7858571484-okn/data-20250301T0100-structure-20150713T0000.xml"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        with open('page.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print("✅ Страница успешно скачана!")
        print(f"📏 Размер: {len(response.text)} символов")
        
        # Быстрая проверка содержимого
        if 'лот' in response.text.lower() or 'auction' in response.text.lower():
            print("✅ Найдены данные о лотах")
        else:
            print("❌ Возможно, скачалась не та страница")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    download_page()
    
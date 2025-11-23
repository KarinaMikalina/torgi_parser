import requests

url = "https://torgi.org/index.php?class=Auction&action=List&mod=Open&AuctionType=All"
html = requests.get(url).text

with open("page.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Реальная страница сохранена!")
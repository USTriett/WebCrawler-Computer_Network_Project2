import requests

headers = {
  'Content-Type': 'application/json',

}
data = {
    "Url": "https://www.sosanhgia.com/r/redirect.php?pm_id=120529783",
    "Name": "Ổ cứng SSD Lexar NQ100 2.5 SATA (6Gb/s) - Hàng Chính Hãng - 240GB",
    "Price": 469000,
    "OriginalPrice": 469000,
    "NameCategory": "Ổ cứng SSD Lexar NQ100 2.5” SATA (6Gb/s) - Hàng Chính Hãng",
    "Imgs": [
        "https://img.sosanhgia.com/images/200x200/cb0af44f1f0e433aab9927ba3eead1ad/o-cung-ssd-lexar-nq100-25-sata-(6gb/s)-hang-chinh-hang-240gb.jpeg"
    ]
}
res = requests.post(url='http://127.0.0.1:5000/updateProduct', headers=headers, json=data)
print(res.text)
import requests

url = 'http://127.0.0.1:8000/books/'  

data = [
    {
        'title': f'Book Title {i}',
        'isbn': f'ISBN-{i}',
        'publication_date': '2024-01-01',
        'pages': 200 + i,
        'price': 10.00 + i,
        'image': 'C:/Users/Electro Ragragui/Desktop/book_manager/media/books_images/images_Dl1KZ6e.jpeg' 
    }
    for i in range(1, 1000)
]

def send_post_request(item_data):
    with open(item_data['image'], 'rb') as image_file:
        files = {'image': image_file}
        response = requests.post(url, data=item_data, files=files)
        return response

for item in data:
    response = send_post_request(item)
    if response.ok:
        print(f"Successfully created item: {response.json()}")
    else:
        print(f"Failed to create item: {response.text}")

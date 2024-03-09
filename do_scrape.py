import numpy as np
import requests

from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image, ImageEnhance, ImageFont, ImageDraw

# all columns then page url and image url
def scrape():
    url = 'https://traderjoesprices.com/'
    response = requests.get(url)
    webpage = response.content

    soup = BeautifulSoup(webpage, 'html.parser')
    table = soup.find('table')

    entries = []
    for row in table.find_all('tr')[1:]:  # Skipping the header row
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        a = row.find_all('a')
        if a:
            cols.append(a[0]['href'])
            response = requests.get(a[0]['href'])
            soup = BeautifulSoup(response.content, 'html.parser')
            image = soup.find_all('meta', attrs={'property': 'og:image'})
            if image:
                image = image[0]['content']
            cols.append(image)
        entries.append(cols)    

    return entries

def get_silly_image(url, text):
    if url:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
    else:
        img = Image.open('stinky.jpg')

    draw = ImageDraw.Draw(img)
    # windows
    # font = ImageFont.truetype("arial.ttf", 50)
    # linux
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 50)
    draw.text((10, 10), text, (255, 255, 255), font=font)

    # Play with this later, the problem here is that it's a transparent png
    # so adding noise like this completely blows out the image

    # img_array = np.array(img)
    # noise = np.random.randint(0, 3, img_array.shape, dtype='uint8')
    # img_array = np.clip(img_array + noise, 0, 255)
    # # Convert back to PIL image
    # img = Image.fromarray(img_array)

    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.15)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(2)
    img.save('out.png', 'PNG', quality=1)
    return 'out.png'

if __name__ == '__main__':
    print(scrape())
    get_silly_image('https://www.traderjoes.com/content/dam/trjo/products/m20701/strawberries.png', '🍓🍓🍓 HOT DIGGITY DOG! 🍓🍓🍓')
    # get_silly_image(None, '🍓🍓🍓 HOT DIGGITY DOG! 🍓🍓🍓')
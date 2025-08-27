import requests
from bs4 import BeautifulSoup
import csv

URL = "https://www.olx.in/items/q-car-cover"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

OUTPUT_FILE = "olx_car_cover_results.csv"

def scrape_olx_results():
    print(f"Fetching data from: {URL}")

    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f"Error: Could not fetch the webpage. {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    ads_list = soup.find('ul', {'data-aut-id': 'itemsList'})

    if not ads_list:
        print("Could not find the main list of ads. The website structure may have changed.")
        return

    ads = ads_list.find_all('li', {'data-aut-id': 'itemBox'})
    
    if not ads:
        print("No ads found on the page. The page might be empty or the structure has changed.")
        return

    print(f"Found {len(ads)} ads. Preparing to write to {OUTPUT_FILE}...")

    with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        writer.writerow(['Title', 'Price', 'Location', 'URL'])

        for ad in ads:
            try:
                title_element = ad.find('span', {'data-aut-id': 'itemTitle'})
                price_element = ad.find('span', {'data-aut-id': 'itemPrice'})
                location_element = ad.find('span', {'data-aut-id': 'item-location'})
                url_element = ad.find('a', href=True)

                title = title_element.text.strip() if title_element else 'N/A'
                price = price_element.text.strip() if price_element else 'N/A'
                location = location_element.text.strip() if location_element else 'N/A'
                ad_url = "https://www.olx.in" + url_element['href'] if url_element else 'N/A'
                
                writer.writerow([title, price, location, ad_url])

            except Exception as e:
                print(f"Could not process an ad: {e}")
    
    print(f"✅ Success! Data has been saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape_olx_results()

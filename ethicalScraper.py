import requests
from bs4 import BeautifulSoup
import time
import re

def extract_asin_from_url(url):
    match = re.search(r'/([A-Z0-9]{10})(?:[/?]|$)', url)
    return match.group(1) if match else None

def fetch_amazon_product_details(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
    }

    print("Fetching data from:", url)
    time.sleep(2)  # Ethical delay

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page. Status code: {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')

    # Title
    title_tag = soup.find(id="productTitle")
    title = title_tag.get_text(strip=True) if title_tag else "No title found"

    # Features / Description
    features = []

    # Try feature bullets
    bullet_points = soup.select('#feature-bullets ul li span')
    if bullet_points:
        features = [bp.get_text(strip=True) for bp in bullet_points if bp.get_text(strip=True)]

    # Fallback: Try product description
    if not features:
        desc_div = soup.find("div", {"id": "productDescription"})
        if desc_div:
            features = [desc_div.get_text(strip=True)]

    # Fallback: Try technical details block
    if not features:
        tech_bullets = soup.select("#productDetails_techSpec_section_1 tr")
        for row in tech_bullets:
            label = row.find("th").get_text(strip=True) # type: ignore
            value = row.find("td").get_text(strip=True) # type: ignore
            features.append(f"{label}: {value}")

    description = ' '.join(features)

    # Main Image
    image_tag = soup.find("img", {"id": "landingImage"})
    if not image_tag:
        og_image = soup.find("meta", {"property": "og:image"})
        image_url = og_image["content"] if og_image else None # type: ignore
    else:
        image_url = image_tag["src"] # type: ignore

    return {
        "title": title,
        "description": description,
        "image": image_url,
        "alt_text": f"{title}",
        "link": url
    }

def format_as_pinterest_pin(data):
    print("\n📌 Pinterest Pin Format:\n")
    print("Title:", data["title"][:100])
    print("\nDescription:", data["description"])
    print("\nAlt Text:", data["alt_text"])
    print("\nImage URL:", data["image"])

# Example Usage
# url = "https://www.amazon.in/SKMEI-Stainless-Pedometer-Stopwatch-Wristwatch/dp/B0D1VK4JTZ"
# asin = extract_asin_from_url(url)

# try:
    # product_data = fetch_amazon_product_details(url)
    # format_as_pinterest_pin(product_data)
    # except Exception as e:
    #     print("❌ Error:", e)

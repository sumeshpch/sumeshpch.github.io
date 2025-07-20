# main.py

import sys
from ethicalScraper import fetch_amazon_product_details
from postToPinterest import post_pin_to_pinterest

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❗ Usage: python main.py <amazon_product_url>")
        sys.exit(1)

    url = sys.argv[1]
    try:
        product = fetch_amazon_product_details(url)
        print("🎯 Product fetched successfully!")
        print("📌 Title:", product["title"])
        print("🖼️ Image:", product["image"])
        print("📝 Description:", product["description"])
        print("\n🚀 Posting to Pinterest...\n")
        post_pin_to_pinterest(product)
    except Exception as e:
        print("❌ Error:", e)

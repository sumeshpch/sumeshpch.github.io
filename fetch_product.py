import os
import datetime
import hashlib
import hmac
import requests
import re
from dotenv import load_dotenv
from urllib.parse import quote, urlencode

load_dotenv()

ACCESS_KEY = os.getenv("AMAZON_ACCESS_KEY")
SECRET_KEY = os.getenv("AMAZON_SECRET_KEY")
ASSOCIATE_TAG = os.getenv("AMAZON_ASSOCIATE_TAG")
REGION = os.getenv("AMAZON_REGION")
HOST = os.getenv("AMAZON_HOST")
SERVICE = "ProductAdvertisingAPI"
ENDPOINT = f"https://{HOST}/paapi5/getitems"

def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

def get_signature_key(key, date_stamp, region, service):
    k_date = sign(("AWS4" + key).encode("utf-8"), date_stamp)
    k_region = sign(k_date, region)
    k_service = sign(k_region, service)
    k_signing = sign(k_service, "aws4_request")
    return k_signing

def create_signed_headers(payload):
    t = datetime.datetime.utcnow()
    amz_date = t.strftime('%Y%m%dT%H%M%SZ')
    date_stamp = t.strftime('%Y%m%d')

    canonical_uri = "/paapi5/getitems"
    canonical_querystring = ""
    canonical_headers = f"content-encoding:utf-8\ncontent-type:application/json;\nhost:{HOST}\nx-amz-date:{amz_date}\n"
    signed_headers = "content-encoding;content-type;host;x-amz-date"
    payload_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()

    canonical_request = f"POST\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{payload_hash}"
    algorithm = "AWS4-HMAC-SHA256"
    credential_scope = f"{date_stamp}/{REGION}/{SERVICE}/aws4_request"
    string_to_sign = f"{algorithm}\n{amz_date}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"

    signing_key = get_signature_key(SECRET_KEY, date_stamp, REGION, SERVICE)
    signature = hmac.new(signing_key, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

    authorization_header = (
        f"{algorithm} Credential={ACCESS_KEY}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, Signature={signature}"
    )

    headers = {
        "Content-Encoding": "utf-8",
        "Content-Type": "application/json;",
        "Host": HOST,
        "X-Amz-Date": amz_date,
        "Authorization": authorization_header
    }

    return headers

def get_amazon_product_details(asin):
    payload = {
        "ItemIds": [asin],
        "Resources": [
            "ItemInfo.Title",
            "ItemInfo.Features",
            "Images.Primary.Large"
        ],
        "PartnerTag": ASSOCIATE_TAG,
        "PartnerType": "Associates",
        "Marketplace": "www.amazon.in"
    }

    import json
    payload_json = json.dumps(payload)
    headers = create_signed_headers(payload_json)

    response = requests.post(ENDPOINT, headers=headers, data=payload_json)
    data = response.json()

    try:
        item = data['ItemsResult']['Items'][0]
        title = item['ItemInfo']['Title']['DisplayValue']
        features = item['ItemInfo']['Features']['DisplayValues']
        image = item['Images']['Primary']['Large']['URL']

        description = " ".join(features)

        # Format for Pinterest
        pinterest = {
            "title": title[:100],
            "description": description[:500],
            "alt_text": f"{title} - main product image",
            "image": image
        }
        return pinterest

    except Exception as e:
        print("Error parsing Amazon response:", e)
        print("Full response:", data)
        return None

def extract_asin(url):
    match = re.search(r'/([A-Z0-9]{10})(?:[/?]|$)', url)
    return match.group(1) if match else None


# Example ASIN from your URL
asin = extract_asin("https://amzn.to/4kMraXC")
pin_data = get_amazon_product_details(asin)

if pin_data:
    print("📌 Pinterest Pin Format\n")
    print("Title:", pin_data["title"])
    print("\nDescription:", pin_data["description"])
    print("\nAlt Text:", pin_data["alt_text"])
    print("\nImage URL:", pin_data["image"])

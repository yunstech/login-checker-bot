from playwright.sync_api import sync_playwright
import requests
from dotenv import load_dotenv
import os
from typing import Dict, Any
load_dotenv()

WEB_APP_API = os.getenv("WEB_APP_API")
WEB_TOKEN_API = os.getenv("WEB_TOKEN_API")

PRODUCT_CONFIG = {
    "edlink": {
        "url": "https://edlink.id/login",
        "selectors": {
            "username": 'input[type="email"]',
            "password": 'input[type="password"]',
            "submit": 'button[type="submit"]'
        },
        "success_check": lambda url: "login" not in url
    },
    "siakadcloud": {
        "url": None,
        "selectors": {
            "username": 'input[name="email"]',
            "password": 'input[name="password"]',
            "submit": 'button[data-type="login"]'
        },
        "success_check": lambda url: "/gate/login" not in url
    },
    "gofeedercloud": {
        "url": None,
        "selectors": {
            "username": 'input[name="username"]',
            "password": 'input[name="password"]',
            "submit": 'button[type="submit"]'
        },
        "success_check": lambda url: "/index.php/home" in url
    }
}

def update_credential_status(username: str, product: str, status: str, url: str) -> Dict[str, Any]:
    request = requests.post(
        f"{WEB_APP_API}/api/update-credential-status",
        json={"username": username, "product": product, "status": status, "url": url},
        headers={"X-API-KEY": f"{WEB_TOKEN_API}"}
    )
    return request.json()

def check_login(username: str, password: str, product: str, endpoint: str) -> Dict[str, Any]:
    config = PRODUCT_CONFIG.get(product.lower())
    if not config:
        return {"status": "error", "reason": f"Unknown product: {product}"}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        try:
            login_url = config["url"] or endpoint
            page.goto(login_url)
            
            page.fill(config["selectors"]["username"], username)
            page.fill(config["selectors"]["password"], password)
            page.click(config["selectors"]["submit"])
            page.wait_for_load_state("networkidle")
            
            is_success = config["success_check"](page.url)
            
            if is_success:
                print("Login successful, proceeding to dashboard.")
                result = update_credential_status(username, product, "Belum Direset", endpoint)
                print(result)
                return {"status": "success"}
            else:
                browser.close()
                result = update_credential_status(username, product, "Sudah Direset", endpoint)
                print(result)
                return {"status": "failure", "reason": "Invalid credentials"}
        except Exception as e:
            browser.close()
            return {"status": "error", "reason": str(e)}

loginCheck = check_login
edlinkCheck = lambda u, p, e: check_login(u, p, "edlink", e)
siakadcloudCheck = lambda u, p, e: check_login(u, p, "siakadcloud", e)
gofeederCheck = lambda u, p, e: check_login(u, p, "gofeedercloud", e)
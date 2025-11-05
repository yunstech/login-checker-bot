from playwright.sync_api import sync_playwright
import requests
from dotenv import load_dotenv
import os
load_dotenv()

WEB_APP_API = os.getenv("WEB_APP_API")
WEB_TOKEN_API = os.getenv("WEB_TOKEN_API")

def loginCheck(username: str, password: str, product: str, endpoint: str):
    if product == "edlink":
        return edlinkCheck(username, password, endpoint)
    elif product == "siakadcloud":
        return siakadcloudCheck(username, password, endpoint)

def edlinkCheck(username: str, password: str, endpoint: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto("https://edlink.id/login")
            page.fill('input[type="email"]', username)
            page.fill('input[type="password"]', password)
            page.click('button[type="submit"]')
            page.wait_for_load_state("networkidle")
            if "login" not in page.url:
                print("Login successful, proceeding to dashboard.")
                request = requests.post(f"{WEB_APP_API}/api/update-credential-status",
                    json={"username": username, "product": "edlink", "status": "Belum Direset", "url": endpoint},
                    headers={"X-API-KEY": f"{WEB_TOKEN_API}"}
                )
                print(request.json())
                return {"status": "success"}
            else:
                browser.close()
                request = requests.post(f"{WEB_APP_API}/api/update-credential-status",
                    json={"username": username, "product": "edlink", "status": "Sudah Direset", "url": endpoint},
                    headers={"X-API-KEY": f"{WEB_TOKEN_API}"}
                )
                print(request.json())
                return {"status": "failure", "reason": "Invalid credentials"}
        except Exception as e:
            browser.close()
            return {"status": "error", "reason": str(e)}

def siakadcloudCheck(username: str, password: str, endpoint: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto(endpoint)
            page.fill('input[name="email"]', username)
            page.fill('input[name="password"]', password)
            page.click('button[data-type="login"]')
            page.wait_for_load_state("networkidle")
            if "/gate/login" not in page.url:
                request = requests.post(f"{WEB_APP_API}/api/update-credential-status",
                    json={"username": username, "product": "siakadcloud", "status": "Belum Direset", "url": endpoint},
                    headers={"X-API-KEY": f"{WEB_TOKEN_API}"}
                )
                print(request.json())
                print("Login successful, proceeding to dashboard.")
            else:
                request = requests.post(f"{WEB_APP_API}/api/update-credential-status",
                    json={"username": username, "product": "siakadcloud", "status": "Sudah Direset", "url": endpoint},
                    headers={"X-API-KEY": f"{WEB_TOKEN_API}"}
                )
                print(request.json())
                browser.close()
                print("Login failed, check credentials.")
                return {"status": "failure", "reason": "Invalid credentials"}
        except Exception as e:
            browser.close()
            return {"status": "error", "reason": str(e)}
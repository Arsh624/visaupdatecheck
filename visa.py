from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import smtplib
import ssl

# === Email Config ===
EMAIL = "architshukla546@gmail.com"
PASSWORD = "thmohgkdiptwvrzu"  # Gmail app password, NOT your normal password
TO_EMAIL = "arsh9532@colorado.edu"

def send_email(subject, body):
    message = f"Subject: {subject}\n\n{body}"
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, TO_EMAIL, message)

# === Chrome Setup ===
options = Options()
options.headless = True
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

seen_updates = set()

while True:
    try:
        driver.get("https://www.visaslots.info/")
        time.sleep(5)

        rows = driver.find_elements("xpath", "//table//tr")
        print(f"\n✅ Found {len(rows)} rows at {time.strftime('%H:%M:%S')}\n")

        for row in rows:
            text = row.text.strip()

            if "NEW DELHI" in text and ("B2" in text or "B1/B2" in text):
                print("🔎 NEW DELHI Slot:", text)

            if ("NEW DELHI" in text and
                ("B2" in text or "B1/B2" in text) and
                "2025" in text and
                text not in seen_updates):

                subject = "[Visa Alert] NEW DELHI Slot for 2025"
                body = f"Slot found:\n\n{text}\n\nCheck: https://www.visaslots.info/"
                send_email(subject, body)
                print("📬 Email sent for:", text)
                seen_updates.add(text)

        time.sleep(60)

    except Exception as e:
        print("⚠️ Error:", e)
        time.sleep(60)

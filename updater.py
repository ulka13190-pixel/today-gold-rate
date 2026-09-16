import os
import json
import datetime
import urllib.request
from google import genai

today_date = datetime.date.today().strftime("%d %B %Y")

# 1. Fetch Live Rates
api_key = os.environ["GOLD_API_KEY"]
url = f"https://api.metalpriceapi.com/v1/latest?api_key={api_key}&base=INR&currencies=XAU,XAG"

req = urllib.request.urlopen(url)
api_res = json.loads(req.read().decode("utf-8"))

# 2. Ask Gemini to write clean HTML table & article
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

prompt = f"""
Today's Date: {today_date}
API Data: {api_res}

Write a clean, SEO-optimized HTML snippet for today's gold rate in India.
Include:
1. An <h2> tag with title: "Gold Rate Today ({today_date}): 22K & 24K Prices"
2. A clean HTML <table> comparing 22K (10g) and 24K (10g) in Delhi, Mumbai, Ludhiana, Kolkata, Chennai, Jaipur.
3. A short 3-bullet explanation of today's market trend.
4. Return ONLY valid HTML inside a <div> container. Do NOT wrap in ```html codeblocks.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)
generated_html = response.text.replace("```html", "").replace("```", "").strip()

# 3. Read index.html and update the main section
with open("index.html", "r", encoding="utf-8") as f:
    full_html = f.read()

# Replace content inside <main id="content">
start_tag = '<main id="content">'
end_tag = '</main>'
new_content = f"{start_tag}\n<div class='post-card'>\n{generated_html}\n</div>\n{end_tag}"

parts = full_html.split(start_tag)
after_parts = parts[1].split(end_tag)

updated_page = parts[0] + new_content + after_parts[1]

with open("index.html", "w", encoding="utf-8") as f:
    f.write(updated_page)

print("Website updated successfully for:", today_date)

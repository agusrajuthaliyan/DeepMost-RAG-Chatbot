import os
from firecrawl import Firecrawl
from dotenv import load_dotenv

load_dotenv()

FC_API = os.getenv("FC_API")

app = Firecrawl(api_key = FC_API)

result = app.scrape(
    url = "https://www.deepmostai.com/",
    formats = ['markdown']
)

filename = "deepmost_data.md"
output_path = os.path.join("data","raw")
filepath = os.path.join(output_path,filename)

with open(filepath, "w", encoding = "utf-8") as f:
    f.write(result.markdown)

print("Data Fetched and saved successfully!")
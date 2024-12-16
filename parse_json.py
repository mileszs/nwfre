"""Parse JSON data and create visualizations"""

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import Template

# File data is from https://www.estately.com/IN/North_Willow_Farms,_Indianapolis/sold
FILE_PATH = "data/properties.json"
OUTPUT_DIR = "visualizations"

# Read JSON data from the file
with open(FILE_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract properties
properties = data.get("properties", [])

# Parse and print prop details
# for prop in properties:
#     unit = prop.get("unit", {})
#     address = prop.get("address", "N/A")
#     beds = unit.get("bedrooms", "N/A")
#     baths = unit.get("bathrooms", "N/A")
#     sqft = unit.get("sqf", "N/A")
#     lot_size = unit.get("lot_sqft", "N/A")
#     price = unit.get("price", "N/A")
#     sold_date = unit.get("sale_date", "N/A")

#     print(f"Address: {address}")
#     print(f"Beds: {beds}")
#     print(f"Baths: {baths}")
#     print(f"Square Footage: {sqft}")
#     print(f"Lot Size: {lot_size} sqft")
#     print(f"Price When Sold: ${price}")
#     print(f"Date Sold: {sold_date}")
#     print("-" * 50)

# print("Total properties:", len(properties))

# Prepare data for analysis
df = pd.DataFrame([
    {
        "Address": prop["address"],
        "Beds": prop["unit"].get("bedrooms", None),
        "Baths": prop["unit"].get("bathrooms", None),
        "Sqft": int(prop["unit"].get("sqf", "0").replace(",", "")) if "sqf" in prop["unit"] else None,
        "Lot Size": prop["unit"].get("lot_sqft", None),
        "Price": prop["unit"].get("price", None),
        "Date Sold": pd.to_datetime(prop["unit"].get("sale_date", None)),
    }
    for prop in properties if "unit" in prop
])

# Create an output directory for images
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Visualization 1: Price Distribution
plt.figure(figsize=(10, 6))
sns.histplot(df["Price"], kde=True, bins=20)
plt.title("Price Distribution")
plt.xlabel("Price ($)")
plt.ylabel("Number of Properties")
plt.savefig(f"{OUTPUT_DIR}/price_distribution.png")
plt.close()

# Price Distribution since 2020
df_sold_since_2020 = df[df["Date Sold"] >= "2020-01-01"]
plt.figure(figsize=(10, 6))
sns.histplot(df_sold_since_2020["Price"], kde=True, bins=20)
plt.title("Price Distribution")
plt.xlabel("Price ($)")
plt.ylabel("Number of Properties")
plt.savefig(f"{OUTPUT_DIR}/price_distribution_2020.png")
plt.close()

# Visualization 2: Beds vs Price
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="Beds", y="Price")
plt.title("Number of Beds vs Price")
plt.xlabel("Number of Beds")
plt.ylabel("Price ($)")
plt.savefig(f"{OUTPUT_DIR}/beds_vs_price.png")
plt.close()

# Visualization 3: Sqft vs Price
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="Sqft", y="Price")
plt.title("Square Footage vs Price")
plt.xlabel("Square Footage")
plt.ylabel("Price ($)")
plt.savefig(f"{OUTPUT_DIR}/sqft_vs_price.png")
plt.close()

# Visualization 4: Lot Size Distribution
plt.figure(figsize=(10, 6))
sns.histplot(df["Lot Size"], kde=True, bins=20)
plt.title("Lot Size Distribution")
plt.xlabel("Lot Size (sqft)")
plt.ylabel("Number of Properties")
plt.savefig(f"{OUTPUT_DIR}/lot_size_distribution.png")
plt.close()

# Visualization 5: Sale Trends Over Time
plt.figure(figsize=(10, 6))
df_sorted = df.sort_values("Date Sold")
sns.lineplot(data=df_sorted, x="Date Sold", y="Price")
plt.title("Sale Price Trends Over Time")
plt.xlabel("Date Sold")
plt.ylabel("Price ($)")
plt.savefig(f"{OUTPUT_DIR}/sale_trends.png")
plt.close()

# Visualization 6: Correlation Matrix
plt.figure(figsize=(10, 6))
corr = df[["Beds", "Baths", "Sqft", "Lot Size", "Price"]].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Correlation Matrix")
plt.savefig(f"{OUTPUT_DIR}/correlation_matrix.png")
plt.close()

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>North Willow Farms Sold Homes Analysis</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">
    <style>
        img { max-width: 100%; height: auto; }
        .visualization { margin-bottom: 50px; }
    </style>
</head>
<body>
    <main class="container">
        <h1>North Willow Farms Sold Homes Analysis</h1>
        <h2>2008-2024</h2>
        <p>Total properties analyzed: {{ total_properties }}</p>
        <div class="visualization">
            <h3>1. Price Distribution since June 2008</h3>
            <img src="price_distribution.png" alt="Price Distribution">
        </div>
        <div class="visualization">
            <h3>2. Price Distribution since January 2020</h3>
            <img src="price_distribution_2020.png" alt="Price Distribution">
        </div>
        <div class="visualization">
            <h3>3. Number of Beds vs Price</h3>
            <img src="beds_vs_price.png" alt="Number of Beds vs Price">
        </div>
        <div class="visualization">
            <h3>4. Square Footage vs Price</h3>
            <img src="sqft_vs_price.png" alt="Square Footage vs Price">
        </div>
        <div class="visualization">
            <h3>5. Lot Size Distribution</h3>
            <img src="lot_size_distribution.png" alt="Lot Size Distribution">
        </div>
        <div class="visualization">
            <h3>6. Sale Price Trends Over Time</h3>
            <img src="sale_trends.png" alt="Sale Price Trends Over Time">
        </div>
        <div class="visualization">
            <h3>7. Correlation Matrix</h3>
            <img src="correlation_matrix.png" alt="Correlation Matrix">
        </div>
    </main>
</body>
</html>
"""

template = Template(HTML_TEMPLATE)
html_content = template.render(total_properties=len(properties))

# Save the HTML file
html_path = os.path.join(OUTPUT_DIR, "analysis.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Visualizations saved to {OUTPUT_DIR}")
print(f"Open {html_path} in your browser to view the analysis.")

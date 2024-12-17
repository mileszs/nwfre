"""Parse JSON data and create visualizations"""

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import Template

FILE_PATH = "data/properties.json"
OUTPUT_DIR = "docs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(FILE_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)

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

df = pd.DataFrame([
    {
        "Address": prop["address"],
        "Beds": prop["unit"].get("bedrooms", None),
        "Baths": prop["unit"].get("bathrooms", None),
        "Sqft": int(prop["unit"].get("sqf", "0").replace(",", "")) if "sqf" in prop["unit"] else None,
        "Lot Size": prop["unit"].get("lot_sqft", None),
        "Price": prop["unit"].get("price", None),
        "Date Sold": pd.to_datetime(prop["unit"].get("sale_date", None), format="%m/%d/%Y", errors="coerce"),
    }
    for prop in properties if "unit" in prop
])

# Remove non-numeric characters and convert to float
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
df["Date Sold Ordinal"] = (df["Date Sold"] - pd.Timestamp("1970-01-01")) // pd.Timedelta("1D")

sns.set_theme()

# Price Distribution
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

# Beds vs Price
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="Beds", y="Price")
plt.title("Number of Beds vs Price")
plt.xlabel("Number of Beds")
plt.ylabel("Price ($)")
plt.savefig(f"{OUTPUT_DIR}/beds_vs_price.png")
plt.close()

# Sqft vs Price
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="Sqft", y="Price")
plt.title("Square Footage vs Price")
plt.xlabel("Square Footage")
plt.ylabel("Price ($)")
plt.savefig(f"{OUTPUT_DIR}/sqft_vs_price.png")
plt.close()

# Lot Size Distribution
plt.figure(figsize=(10, 6))
sns.histplot(df["Lot Size"], kde=True, bins=20)
plt.title("Lot Size Distribution")
plt.xlabel("Lot Size (sqft)")
plt.ylabel("Number of Properties")
plt.savefig(f"{OUTPUT_DIR}/lot_size_distribution.png")
plt.close()

# Sale Trends Over Time
plt.figure(figsize=(10, 6))
df_sorted = df.sort_values("Date Sold")
sns.regplot(
    data=df_sorted,
    x="Date Sold Ordinal",
    y="Price",
    scatter_kws={"s": 50, "alpha": 0.5},  # Scatter point style
    line_kws={"color": "red"},            # Line style
    ci=None  # Disable confidence interval for cleaner trend line
)
# Customize the x-axis to show human-readable dates
date_labels = [pd.to_datetime(ordinal, origin="unix", unit="D").strftime("%Y-%m-%d") for ordinal in df_sorted["Date Sold Ordinal"].unique()]
plt.xticks(ticks=df_sorted["Date Sold Ordinal"].unique()[::10], labels=date_labels[::10], rotation=45)
plt.title("Sale Price Trends Over Time")
plt.xlabel("Date Sold")
plt.ylabel("Price ($)")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/sale_trends.png")
plt.close()

# Correlation Matrix
plt.figure(figsize=(10, 6))
corr = df[["Beds", "Baths", "Sqft", "Lot Size", "Price"]].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Correlation Matrix")
plt.savefig(f"{OUTPUT_DIR}/correlation_matrix.png")
plt.close()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>North Willow Farms Sold Homes Analysis</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">
</head>
<body>
    <main class="container">
        <h1>North Willow Farms Sold Homes Analysis</h1>
        <h2>2008-2024</h2>
        <p>Total properties analyzed: {{ total_properties }}</p>
        <details class="visualization">
            <summary role="button" class="outline">Price Distribution since June 2008</summary>
            <img src="price_distribution.png" alt="Price Distribution">
        </details>
        <details class="visualization">
            <summary role="button" class="outline">Price Distribution since January 2020</summary>
            <img src="price_distribution_2020.png" alt="Price Distribution">
        </details>
        <details class="visualization">
            <summary role="button" class="outline">Sale Price Trends Over Time</summary>
            <img src="sale_trends.png" alt="Sale Price Trends Over Time">
        </details>
        <details class="visualization">
            <summary role="button" class="outline">Number of Beds vs Price</summary>
            <img src="beds_vs_price.png" alt="Number of Beds vs Price">
        </details>
        <details class="visualization">
            <summary role="button" class="outline">Square Footage vs Price</summary>
            <img src="sqft_vs_price.png" alt="Square Footage vs Price">
        </details>
        <details class="visualization">
            <summary role="button" class="outline">Lot Size Distribution</summary>
            <img src="lot_size_distribution.png" alt="Lot Size Distribution">
        </details>
        <details class="visualization">
            <summary role="button" class="outline">Correlation Matrix</summary>
            <img src="correlation_matrix.png" alt="Correlation Matrix">
        </details>
    </main>
</body>
</html>
"""

template = Template(HTML_TEMPLATE)
html_content = template.render(total_properties=len(properties))

html_path = os.path.join(OUTPUT_DIR, "index.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Visualizations saved to {OUTPUT_DIR}")
print(f"Open {html_path} in your browser to view the analysis.")

"""Parse JSON data and create visualizations"""

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.io as pio
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
price_distribution_fig = px.histogram(df, x="Price", title="Price Distribution since June 2008")
price_distribution_fig.update_layout(bargap=0.1)
price_distribution_html = pio.to_html(price_distribution_fig, full_html=False)

# Price Distribution since 2020
df_sold_since_2020 = df[df["Date Sold"] >= "2020-01-01"]
price_distribution_2020_fig = px.histogram(
    df_sold_since_2020,
    x="Price",
    title="Price Distribution since January 2020")
price_distribution_2020_fig.update_layout(bargap=0.1)
price_distribution_2020_html = pio.to_html(price_distribution_2020_fig, full_html=False)

# Sale Trends Over Time
sale_trends_fig = px.scatter(
    df, x="Date Sold", y="Price", title="Sale Price Trends Over Time", trendline="ols", hover_data=["Address"]
)
sale_trends_html = pio.to_html(sale_trends_fig, full_html=False)

beds_vs_price_fig = px.scatter(df, x="Beds", y="Price", title="Number of Beds vs Price")
beds_vs_price_html = pio.to_html(beds_vs_price_fig, full_html=False)

sqft_vs_price_fig = px.scatter(df, x="Sqft", y="Price", title="Square Footage vs Price")
sqft_vs_price_html = pio.to_html(sqft_vs_price_fig, full_html=False)

lot_size_vs_price_fig = px.scatter(df, x="Lot Size", y="Price", title="Lot Size vs Price")
lot_size_vs_price_html = pio.to_html(lot_size_vs_price_fig, full_html=False)

lot_size_distribution_fig = px.histogram(df, x="Lot Size", title="Lot Size Distribution")
lot_size_distribution_fig.update_layout(bargap=0.1)
lot_size_distribution_html = pio.to_html(lot_size_distribution_fig, full_html=False)

correlation_matrix = df[["Beds", "Baths", "Sqft", "Lot Size", "Price"]].corr()
correlation_matrix_fig = px.imshow(correlation_matrix, title="Correlation Matrix", text_auto=True)
correlation_matrix_html = pio.to_html(correlation_matrix_fig, full_html=False)

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
        <figure>
          <img
            src="nwf-rainbow.png"
            alt="Rainbow over North Willow Farms"
          />
          <figcaption>
            Photo from Eric White
          </figcaption>
        </figure>
        <h1>North Willow Farms Sold Homes Analysis</h1>
        <h2>2008-2024</h2>
        <p>Total properties analyzed: {{ total_properties }}</p>
        <details class="visualization">
            <summary role="button" class="outline">Price Distribution since June 2008</summary>
            {{ price_distribution_html | safe }}
        </details>
        <details class="visualization">
            <summary role="button" class="outline">Price Distribution since January 2020</summary>
            {{ price_distribution_2020_html | safe }}
        </details>
        <details class="visualization">
            <summary role="button" class="outline">Sale Price Trends Over Time</summary>
            {{ sale_trends_html | safe }}
        </details>
        <details class="visualization">
            <summary role="button" class="outline">Number of Beds vs Price</summary>
            {{ beds_vs_price_html | safe }}
        </details>
        <details class="visualization">
            <summary role="button" class="outline">Square Footage vs Price</summary>
            {{ sqft_vs_price_html | safe }}
        </details>
        <details class="visualization">
            <summary role="button" class="outline">Lot Size vs Price</summary>
            {{ lot_size_vs_price_html | safe }}
        </details>
        <details class="visualization">
            <summary role="button" class="outline">Lot Size Distribution</summary>
            {{ lot_size_distribution_html | safe }}
        </details>
        <details class="visualization">
            <summary role="button" class="outline">Correlation Matrix</summary>
            {{ correlation_matrix_html | safe }}
        </details>
    </main>
</body>
</html>
"""

template = Template(HTML_TEMPLATE)
html_content = template.render(
    total_properties=len(properties),
    price_distribution_html=price_distribution_html,
    price_distribution_2020_html=price_distribution_2020_html,
    sale_trends_html=sale_trends_html,
    beds_vs_price_html=beds_vs_price_html,
    sqft_vs_price_html=sqft_vs_price_html,
    lot_size_vs_price_html=lot_size_vs_price_html,
    lot_size_distribution_html=lot_size_distribution_html,
    correlation_matrix_html=correlation_matrix_html)

html_path = os.path.join(OUTPUT_DIR, "index.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Visualizations saved to {OUTPUT_DIR}")
print(f"Open {html_path} in your browser to view the analysis.")

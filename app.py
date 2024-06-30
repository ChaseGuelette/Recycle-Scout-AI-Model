from flask import Flask, render_template, request
import folium
import pandas as pd
import os


#os.system('python generate.py')

app = Flask(__name__)

# Route for displaying the map
@app.route("/", methods=["GET", "POST"])
def display_map():
    # Default selection
    user_selection = "Transportation Index"
    
    if request.method == "POST":
        user_selection = request.form.get("user_selection")
    
    # Load data and create map
    eco_footprints = pd.read_csv("test/data.csv")
    max_eco_footprint = eco_footprints[user_selection].max()
    political_countries_url = (
        "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
    )

    m = folium.Map(location=(30, 10), zoom_start=3, tiles="cartodb positron")

    folium.Choropleth(
        geo_data=political_countries_url,
        data=eco_footprints,
        columns=["Country Name", user_selection],
        key_on="feature.properties.name",
        fill_color="RdYlGn_r",
        fill_opacity=0.6,
        line_opacity=0.3,
        nan_fill_color="white",
        legend_name=f"{user_selection} per capita",
        name="Countries by {user_selection}",
    ).add_to(m)
    folium.LayerControl().add_to(m)

    # Save map to HTML string
    map_html = m._repr_html_()

    return render_template("index.html", map_html=map_html, user_selection=user_selection)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

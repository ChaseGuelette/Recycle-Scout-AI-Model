from flask import Flask, render_template, request
import folium
import pandas as pd

app = Flask(__name__)

# Route for displaying the map
@app.route("/", methods=["GET"])
def display_map():
    # Load data and create map
    eco_footprints = pd.read_csv("footprint.csv")
    max_eco_footprint = eco_footprints["Carbon"].max()
    political_countries_url = (
        "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
    )

    m = folium.Map(location=(30, 10), zoom_start=3, tiles="cartodb positron")

    folium.Choropleth(
        geo_data=political_countries_url,
        data=eco_footprints,
        columns=["Country Name", "Carbon"],
        key_on="feature.properties.name",
        bins=[0, 1000000, 10000000, 30000000, 50000000, 100000000, 500000000, 1000000000, 10000000000, max_eco_footprint],
        fill_color="RdYlGn_r",
        fill_opacity=0.8,
        line_opacity=0.3,
        nan_fill_color="white",
        legend_name="Carbon footprint per capita",
        name="Countries by ecological footprint per capita",
    ).add_to(m)
    folium.LayerControl().add_to(m)

    # Save map to HTML string
    map_html = m._repr_html_()

    return render_template("index.html", map_html=map_html)

# Route for handling the form submission
@app.route("/submit", methods=["POST"])
def handle_form():
    # Get data from the dropdown form
    user_selection = request.form.get("user_selection")
    
    # Store the selected value in a variable
    stored_data = user_selection
    
    return render_template("result.html", stored_data=stored_data)

if __name__ == "__main__":
    app.run(debug=True)

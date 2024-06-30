from flask import Flask, request, render_template
import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import folium
from markupsafe import Markup

app = Flask(__name__)

key = "414e0c5e150043c09d1d4f082fabe461"
geocoder_service = OpenCageGeocode(key)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        number = request.form['phone_number']
        try:
            new_number = phonenumbers.parse(number)
            location = geocoder.description_for_number(new_number, "en")
            service_name = carrier.name_for_number(new_number, "en")
            query = str(location)
            result = geocoder_service.geocode(query)
            lat = result[0]['geometry']['lat']
            lng = result[0]['geometry']['lng']

            # Generate the map with Folium
            my_map = folium.Map(location=[lat, lng], zoom_start=9)
            folium.Marker([lat, lng], popup=location).add_to(my_map)
            map_html = my_map._repr_html_()

            print("Map HTML:", map_html)  # Debug output

            return render_template('result.html', location=location, service_name=service_name, map_html=Markup(map_html))
        except Exception as e:
            return render_template('index.html', error=str(e))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

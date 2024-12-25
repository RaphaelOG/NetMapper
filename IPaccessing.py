#write the psuedocode for the code and write what you are trying to do at the top of the code 


from bs4 import BeautifulSoup  # For parsing HTML data
import requests  # For making HTTP requests
import re 
import geocoder  # For geocoding IP addresses
import folium  # For creating interactive maps
import plotly.express as px  # For creating visualizations
from branca.element import Template, MacroElement  # For adding custom elements to Folium maps
import time  # For adding delays
import webbrowser  # For opening web pages


# URL of the log file containing IP addresses
url = "http://192.168.1.254/cgi-bin/logs.ha"#you would need to put your gateways ip log here

# Default map location and settings
default_location = [30, 0]
map = folium.Map(location=default_location, zoom_start=3, tiles="cartodb positron")



# Function to fetch and parse IP addresses from the log file
def get_ip_addresses():
    result = requests.get(url)  # Fetch the log file
    doc = BeautifulSoup(result.text, "html.parser") 
    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')  # Pattern to match IP addresses
    ip_addresses = set()  # Set to store unique IP addresses
    
    # Find and add IP addresses to the set
    for element in doc.find_all(text=True):
        if ip_pattern.search(element):
            ip_addresses.add(ip_pattern.search(element).group())
    
    return ip_addresses

ip_count = 0  # Initialize the IP address counter

while True:
    ip_addresses = get_ip_addresses()  # Get IP addresses from the log file
    
    for ip in ip_addresses:
        print("Source IP: " + ip) 
        ip_l = geocoder.ip(ip)  # Get location info for the IP address
        if ip_l.latlng:
            print(ip_l.city) 
            print(ip_l.latlng)  
            #adding marker on the map
            folium.CircleMarker(location=ip_l.latlng, radius=10, color="red").add_to(map) 
            folium.Marker(location=ip_l.latlng, popup=f"{ip}\n{ip_l.city}").add_to(map) 

    ip_count += len(ip_addresses)  # Increment the IP address counter by the number of unique IPs found
    

  
    # Save the updated map to an HTML file and open it in the web browser
    map.save("map.html")
    webbrowser.open("map.html")
    time.sleep(60)#makes it refresh every 60 seconds

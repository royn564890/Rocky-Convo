from flask import Flask, send_file
import os
import threading
import time
import requests
import prem

app = Flask(__name__)

@app.route('/')
def index():
    return send_file(os.path.join(os.path.dirname(__file__), "public", "index.html"))


app.run(host='0.0.0.0', port=81)


# Serve static files from the "public" directory
app.static_folder = 'public'

# Start the Flask server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(port=port, debug=True)

# Function to ping the server
def ping_server():
    sleep_time = 10 * 60  # 10 minutes
    while True:
        time.sleep(sleep_time)
        try:
            response = requests.get('past_webserver.url', timeout=10)
            print(f"Pinged server with response: {response.status_code}")
        except requests.RequestException as e:
            if isinstance(e, requests.Timeout):
                print("Couldn't connect to the site URL..!")
            else:
                print(e)

# Start the ping function in a separate thread
ping_thread = threading.Thread(target=ping_server)
ping_thread.start()

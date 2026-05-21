import socket

def send_request(host, port, request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(request)

        response = b""
        while True:
            data = s.recv(4096)
            if not data:
                break
            response += data

    return response.decode(errors='ignore')


def upload_file(host, port, filename):
    with open(filename, 'rb') as file:
        file_data = file.read()
        content_length = len(file_data)

        request = (
            f"POST /upload HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            f"Content-Length: {content_length}\r\n"
            f"Content-Type: text/plain\r\n"
            f"\r\n"
        ).encode() + file_data

        response = send_request(host, port, request)

    return response


def download_file(host, port, filename):
    request = (
        f"GET /{filename} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"\r\n"
    ).encode()

    response = send_request(host, port, request)

    if '\r\n\r\n' in response:
        file_content = response.split('\r\n\r\n', 1)[1]

        with open("downloaded_" + filename, 'w') as file:
            file.write(file_content)

        print("File downloaded successfully.")
    else:
        print("Invalid response received.")


if __name__ == "__main__":

    # Local server
    host = 'localhost'
    port = 8080

    # Upload file
    upload_response = upload_file(host, port, 'example.txt')
    print("Upload response:\n", upload_response)

    # Download file
    download_file(host, port, 'example.txt')
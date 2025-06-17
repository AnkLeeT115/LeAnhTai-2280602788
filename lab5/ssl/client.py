import socket
import ssl
import threading

# Thông tin server
server_address = ('localhost', 12345)

def receive_data(ssl_socket):
    try:
        while True:
            data = ssl_socket.recv(1024)
            if not data:
                break
            print("Nhận:", data.decode('utf-8'))
    except:
        pass
    finally:
        ssl_socket.close()
        print("Kết nối đã đóng.")

# Tạo socket client TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Tạo SSL context dùng cho client
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)  # ✅ Sửa ở đây
context.check_hostname = False  # ⚠️ Tùy theo việc bạn có dùng tên miền không
context.verify_mode = ssl.CERT_NONE  # ⚠️ Không xác minh chứng chỉ (chỉ dùng cho demo/testing)

# Bọc SSL cho socket
ssl_socket = context.wrap_socket(client_socket, server_hostname='localhost')

# Kết nối tới server
ssl_socket.connect(server_address)

# Tạo luồng nhận dữ liệu từ server
receive_thread = threading.Thread(target=receive_data, args=(ssl_socket,))
receive_thread.start()

# Gửi dữ liệu tới server
try:
    while True:
        message = input("Nhập tin nhắn: ")
        ssl_socket.send(message.encode('utf-8'))
except KeyboardInterrupt:
    print("\nNgắt kết nối.")
finally:
    ssl_socket.close()

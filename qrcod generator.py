import tkinter as tk
import base64
import secrets
import random
import qrcode
from PIL import Image, ImageTk

def generate_wireguard_config(num_peers, config_name):
    # Create a new configuration file
    config_file = f"{config_name}.conf"

    # Generate a random private key
    private_key_bytes = secrets.token_bytes(32)
    private_key_base64 = base64.b64encode(private_key_bytes).decode()

    # Write the configuration file
    with open(config_file, "w") as f:
        # Write the interface section
        f.write("[Interface]\n")
        random_address = random.randint(1, 200)
        f.write(f"Address = 10.0.{random_address}/24\n")
        f.write("ListenPort = 51820\n")
        f.write(f"PrivateKey = {private_key_base64}\n")
        f.write("MTU = 1500\n")
        f.write("KeepAlive = 60\n")
        f.write("DNS = 203.0.209.1, 78.157.42.100, fd12:3456:789a:aa30::db5e, fd12:3456:789a:cd97::a30\n\n")

        # Write the peer sections
        for i in range(num_peers):
            f.write("[Peer]\n")
            f.write(f"PublicKey = {private_key_base64}\n\n")
            random_port = random.randint(1, 300)
            f.write(f"Endpoint = 192.168.1.{random_port}:25400\n")
            f.write("AllowedIPs = 10.202.10.11\n")
            f.write("PersistentKeepalive = 60\n")

    return config_file, private_key_base64, random_address, random_port

def generate_qr_code(config_file):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"wg://{config_file}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qrcode.png")
    return ImageTk.PhotoImage(Image.open("qrcode.png"))

def generate_config():
    config_name = "vip"
    num_peers = 1
    config_file, private_key_base64, random_address, random_port = generate_wireguard_config(num_peers, config_name)
    qr_image = generate_qr_code(config_file)

    # نمایش اطلاعات کانفینگ
    config_info = f"Endpoint: 192.168.1.{random_port}:25400\n"
    config_info += f"DNS: 203.0.209.1, 78.157.42.100, fd12:3456:789a:aa30::db5e, fd12:3456:789a:cd97::a30\n"
    config_info += f"AllowedIPs: 10.202.10.11\n"
    config_info += f"PersistentKeepalive: 60\n"

    # نمایش QR Code
    qr_label.config(image=qr_image)
    qr_label.image = qr_image

    # نمایش اطلاعات کانفینگ
    config_label.config(text=config_info)

def save_qr():
    print("QR Code saved as qrcode.png")

root = tk.Tk()
root.title("WireGuard Config Generator")
root.configure(bg="black")

# دکمه Generate Config
generate_button = tk.Button(root, text="Generate Config", command=generate_config, bg="orange", fg="white", borderwidth=5, relief="ridge")
generate_button.pack(pady=20)

# دکمه Save QR
save_button = tk.Button(root, text="Save QR", command=save_qr, bg="orange", fg="white", borderwidth=5, relief="ridge")
save_button.pack(pady=10)

# نمایش QR Code
qr_label = tk.Label(root, image=None, bg="black")
qr_label.pack(pady=20)

# نمایش اطلاعات کانفینگ
config_label = tk.Label(root, text="", bg="black", fg="pink")
config_label.pack(pady=10)

root.mainloop()
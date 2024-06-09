import qrcode
import os

# Ensure the directory for QR codes exists
os.makedirs("qrcodes", exist_ok=True)

# URL to encode in the QR codes
url = "www.udemy.com/course/langchain"

# Generate and save QR codes
for i in range(1, 16):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"qrcodes/qr_{i}.png")

print("QR codes generated and saved successfully.")
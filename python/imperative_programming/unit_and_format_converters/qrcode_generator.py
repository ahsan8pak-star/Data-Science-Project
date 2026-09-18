import os
import sys

import qrcode


def make_qr_code(data, output_dir=None, output_file="qrcode.png"):
    if output_dir is None:
        output_dir = os.getcwd()

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_file)

    qrcode.make(data).save(output_path)
    return output_path


def generate_qrcode():
    if len(sys.argv) > 1:
        data = sys.argv[1]
    else:
        data = input("Enter the URL to encode into a QR code PNG: ").strip()

    if not data:
        print("Nothing to encode; please provide a URL or link.")
        return

    output_path = make_qr_code(data)
    print(f"QR code image saved to: {output_path}")


if __name__ == "__main__":
    generate_qrcode()



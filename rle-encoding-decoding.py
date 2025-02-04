import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np
import pickle

def compress_image():
    # Resmi seç
    image_path = filedialog.askopenfilename()
    if image_path:
        img = Image.open(image_path)
        img_gray = img.convert('L')
        img_gray.show()

        def rle_encode(img):
            data = np.array(img)
            pixels = data.flatten()
            results = []
            last_pixel = pixels[0]
            count = 1

            for pixel in pixels[1:]:
                if pixel == last_pixel:
                    count += 1
                else:
                    results.append((last_pixel, count))
                    last_pixel = pixel
                    count = 1
            results.append((last_pixel, count))
            return results

        encoded_data = rle_encode(img_gray)

        # Sıkıştırılmış verileri ve resmin boyutlarını kaydet
        compressed_data = {
            'encoded': encoded_data,
            'shape': img_gray.size,  # Resmin boyutlarını sakla
            'original_size': len(pickle.dumps(img_gray))  # Orijinal resmin boyutunu sakla
        }

        with open('compressed_data.pkl', 'wb') as f:
            pickle.dump(compressed_data, f)
        messagebox.showinfo("Success", "Image has been compressed and saved!")

def decompress_image():
    try:
        with open('compressed_data.pkl', 'rb') as f:
            compressed_data = pickle.load(f)

        encoded_data = compressed_data['encoded']
        shape = compressed_data['shape']  # Kaydedilen boyutları kullan
        original_size = compressed_data['original_size']
        compressed_size = len(pickle.dumps(compressed_data['encoded']))

        def rle_decode(encoded_data, shape):
            decoded_image = np.zeros(shape[0] * shape[1], dtype=np.uint8)
            index = 0
            for value, count in encoded_data:
                decoded_image[index:index + count] = value
                index += count
            return decoded_image.reshape(shape)

        # Sıkıştırılmış verileri aç
        decoded_image = rle_decode(encoded_data, shape)

        # Decode edilmiş resmi göster
        img_decoded = Image.fromarray(decoded_image)
        img_decoded.show()

        # Sıkıştırma oranını hesapla
        ratio = original_size / compressed_size
        messagebox.showinfo("Compression Info", f"Compressed image has been decompressed!\nCompression Ratio: {ratio:.2f}")
    except FileNotFoundError:
        messagebox.showerror("Error", "Compressed data file not found!")

root = tk.Tk()
root.title("Image Compression Project")

compress_button = tk.Button(root, text="Compress Image", command=compress_image)
compress_button.pack()

decompress_button = tk.Button(root, text="Decompress Image", command=decompress_image)
decompress_button.pack()

root.mainloop()

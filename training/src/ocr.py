import easyocr

class OCRProcessor:
    def __init__(self, langs=['id', 'en'], use_gpu=True):
        print(f"Initializing EasyOCR for languages: {langs}...")
        self.reader = easyocr.Reader(langs, gpu=use_gpu)

    def process_image(self, image_path):
        """
        Melakukan OCR pada sebuah gambar.
        Mengembalikan teks lengkap yang digabung dengan spasi.
        """
        results = self.reader.readtext(image_path, detail=0, paragraph=True)
        # result is a list of strings
        full_text = " ".join(results)
        return full_text

if __name__ == '__main__':
    print("This module is meant to be imported and used within a pipeline.")

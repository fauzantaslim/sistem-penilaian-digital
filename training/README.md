# Digital Scoring Pipeline - Faster R-CNN & OCR

Folder ini berisi seluruh pipeline untuk melatih model object detection (Faster R-CNN) dan melakukan inferensi penuh mulai dari gambar hingga skor akhir.

## 1. Persiapan Environment
Pastikan Anda menggunakan environment Python yang memiliki dukungan PyTorch.
`ash
pip install -r requirements.txt
`

## 2. Struktur Folder Dataset
Dataset harus berada di folder datasets/skripsi ameng.v2i.coco/ di root project.
Di dalamnya harus ada:
- 	rain/_annotations.coco.json
- alid/_annotations.coco.json
- 	est/_annotations.coco.json

## 3. Melatih Model Faster R-CNN
Untuk melatih model pendeteksi area jawaban, jalankan:
`ash
cd training
python train.py
`
Checkpoints akan disimpan di folder checkpoints/.

## 4. Evaluasi Model
Untuk menghitung mAP pada test set:
`ash
cd training/src
python evaluate.py
`

## 5. Menjalankan Pipeline Lengkap
Untuk menguji pipeline dari gambar mentah hingga mendapat nilai akhir:
`ash
cd training/src
python pipeline.py --image "../../datasets/skripsi ameng.v2i.coco/test/WhatsApp-Image-2026-09-23-at-15-00-05_jpeg.rf.3e7ebdd83e24e220de46340c7fbc106f.jpg"
`
Pipeline ini akan:
1. Mendeteksi area jawaban dengan Faster R-CNN
2. Mengurutkan area jawaban dari atas ke bawah
3. Melakukan crop area
4. Membaca teks dengan EasyOCR
5. Menghitung similarity dengan TF-IDF + Cosine Similarity
6. Mengubah similarity menjadi skor.

Hasil visualisasi dan log penilaian akan disimpan di 	raining/outputs/.

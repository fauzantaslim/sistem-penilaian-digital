import os
import argparse
import json
import torch
from inference import run_inference
from crop import crop_answers
from ocr import OCRProcessor
from scoring import calculate_similarity, convert_similarity_to_score

def run_pipeline(image_path, model_path, kunci_jawaban_list, output_dir="../outputs"):
    print("=== PIPELINE PENILAIAN DIGITAL ===")
    print(f"Input Image: {image_path}")
    
    # 1. Deteksi Area Jawaban (Faster R-CNN)
    print("\n1. Menjalankan Deteksi Faster R-CNN...")
    det_out_dir = os.path.join(output_dir, "detections")
    sorted_boxes, img = run_inference(image_path, model_path, det_out_dir, conf_threshold=0.5)
    
    if len(sorted_boxes) == 0:
        print("Tidak ada area jawaban yang terdeteksi.")
        return
        
    # 2. Crop Area Jawaban
    print("\n2. Melakukan Crop Area Jawaban...")
    crop_out_dir = os.path.join(output_dir, "crops")
    base_name = os.path.basename(image_path).split('.')[0]
    crop_paths = crop_answers(img, sorted_boxes, crop_out_dir, base_name)
    
    # 3. Inisialisasi OCR
    print("\n3. Memulai OCR...")
    ocr_processor = OCRProcessor(use_gpu=torch.cuda.is_available())
    
    # 4 & 5. Ekstraksi Teks dan Penilaian
    print("\n4 & 5. Ekstraksi Teks & Penilaian Cosine Similarity...")
    hasil_penilaian = []
    total_skor = 0.0
    
    for i, crop_path in enumerate(crop_paths):
        print(f"\nMemproses Jawaban {i+1}:")
        # Ekstrak teks
        student_text = ocr_processor.process_image(crop_path)
        print(f"Teks OCR: '{student_text}'")
        
        # Ambil kunci jawaban (jika ada)
        if i < len(kunci_jawaban_list):
            kunci = kunci_jawaban_list[i]
            correct_text = kunci['jawaban']
            bobot = kunci['bobot']
            
            # Hitung kemiripan
            sim = calculate_similarity(student_text, correct_text)
            skor = convert_similarity_to_score(sim, bobot)
            
            print(f"Kunci Jawaban: '{correct_text}'")
            print(f"Similarity: {sim:.4f}")
            print(f"Skor: {skor}/{bobot}")
            
            hasil_penilaian.append({
                "nomor": i+1,
                "teks_siswa": student_text,
                "kunci_jawaban": correct_text,
                "similarity": sim,
                "skor": skor,
                "bobot": bobot
            })
            total_skor += skor
        else:
            print("Tidak ada kunci jawaban untuk soal ini.")
            hasil_penilaian.append({
                "nomor": i+1,
                "teks_siswa": student_text,
                "kunci_jawaban": None,
                "similarity": 0.0,
                "skor": 0.0,
                "bobot": 0.0
            })
            
    print(f"\n=====================================")
    print(f"TOTAL SKOR AKHIR: {total_skor:.2f}")
    print(f"=====================================")
    
    # Simpan hasil ke JSON
    ocr_out_dir = os.path.join(output_dir, "ocr")
    os.makedirs(ocr_out_dir, exist_ok=True)
    json_path = os.path.join(ocr_out_dir, f"{base_name}_hasil.json")
    with open(json_path, 'w') as f:
        json.dump(hasil_penilaian, f, indent=4)
    print(f"Hasil disimpan di {json_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, required=True, help='Path ke gambar lembar jawaban')
    parser.add_argument('--model', type=str, default='../checkpoints/best_model.pth', help='Path ke checkpoint Faster R-CNN')
    
    args = parser.parse_args()
    
    # Simulasi kunci jawaban
    dummy_kunci = [
        {'jawaban': 'Fotosintesis adalah proses pembuatan makanan oleh tumbuhan menggunakan cahaya matahari menghasilkan oksigen', 'bobot': 5.0},
        {'jawaban': 'Gaya tarik bumi disebut gravitasi yang menyebabkan benda jatuh ke bawah', 'bobot': 5.0},
        {'jawaban': 'Ekosistem terdiri dari komponen biotik dan abiotik yang saling berinteraksi membentuk keseimbangan', 'bobot': 5.0}
    ]
    
    run_pipeline(args.image, args.model, dummy_kunci)

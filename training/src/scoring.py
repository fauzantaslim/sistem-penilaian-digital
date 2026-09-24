from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def clean_text(text):
    """
    Membersihkan teks: huruf kecil, hapus karakter non-alfanumerik.
    """
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text.strip()

def calculate_similarity(student_answer, correct_answer):
    """
    Menghitung cosine similarity menggunakan TF-IDF antara jawaban siswa dan kunci jawaban.
    """
    student_clean = clean_text(student_answer)
    correct_clean = clean_text(correct_answer)
    
    if not student_clean or not correct_clean:
        return 0.0
        
    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform([student_clean, correct_clean])
        # tfidf_matrix[0] is student, [1] is correct
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(similarity)
    except ValueError:
        # Happens if vocab is empty (e.g., only stop words or single characters depending on vectorizer settings)
        return 0.0

def convert_similarity_to_score(similarity, max_score=10.0):
    """
    Mengubah nilai similarity (0.0 - 1.0) menjadi nilai akhir.
    Aturan bisa disesuaikan, misalnya:
    Jika similarity > 0.8, skor penuh.
    Jika < 0.2, skor 0.
    """
    # Simple linear scaling for now
    score = similarity * max_score
    return round(score, 2)

if __name__ == '__main__':
    # Test
    kunci = "Fotosintesis adalah proses pembuatan makanan oleh tumbuhan menggunakan cahaya matahari menghasilkan oksigen"
    jawaban1 = "tumbuhan buat makanan pakai matahari dan hasilkan oksigen lewat fotosintesis"
    jawaban2 = "kucing makan ikan di pasar"
    
    sim1 = calculate_similarity(jawaban1, kunci)
    sim2 = calculate_similarity(jawaban2, kunci)
    
    print(f"Jawaban 1 Similarity: {sim1:.4f} -> Score (max 4): {convert_similarity_to_score(sim1, 4.0)}")
    print(f"Jawaban 2 Similarity: {sim2:.4f} -> Score (max 4): {convert_similarity_to_score(sim2, 4.0)}")

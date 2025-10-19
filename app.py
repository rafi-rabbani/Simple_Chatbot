import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

# --- Konfigurasi ---
# Cara aman: Simpan API Key di environment variable
# Untuk sekarang, bisa langsung masukkan di sini (tapi JANGAN bagikan kode ini)
# GANTI DENGAN API KEY KAMU YANG SEBENARNYA:
API_KEY = "AIzaSyBWDSiNQsKQt8PY1qdFBIU1vesf-GgInU8"

genai.configure(api_key = API_KEY)

# --- Inisialisasi Aplikasi Flask & Model Gemini ---
app = Flask(__name__)

# Pilih model Gemini yang ingin digunakan
model = genai.GenerativeModel('gemini-2.0-flash')

# --- Routes ---
@app.route("/")
def index(): 
  """Menampilkan halaman utama (index.html)."""
  return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
  """Menerima pesan, mengirim ke Gemini, mengembalikan respons."""
  try:
    # Ambil pesan dari request JSON
    user_message = request.json.get("message")

    if not user_message:
      return jsonify({"error": "Pesan tidak boleh kosong."}), 400

    # Kirim pesan ke model Gemini
    response = model.generate_content(user_message)

    # Ambil teks respons dari Gemini
    # Perhatikan: Akses teks mungkin berbeda sedikit tergantung versi library
    # Coba cek 'response.text' atau 'response.parts[0].text' jika ini error
    bot_response = response.text

    return jsonify({"response": bot_response})

  except Exception as e:
    # Tangani jika ada error saat komunikasi dengan Gemini
    print(f"Error: {e}") # Tampilkan error di terminal backend
    return jsonify({"response": "Maaf, terjadi kesalahan saat menghubungi AI."}), 500

# --- Menjalankan Aplikasi ---
# mencegah agar aplikasi tidak berjalan saat diimpor
if __name__ == "__main__":
  # debug=True agar perubahan kode otomatis terdeteksi saat disimpan
  app.run(debug=True)
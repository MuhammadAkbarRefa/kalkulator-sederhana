# Import library yang dibutuhkan
from flask import Flask, render_template, request
from datetime import datetime

# Membuat instance aplikasi Flask
app = Flask(__name__)

# Fungsi untuk menangani evaluasi yang aman
def safe_eval(expression):
    """
    Mengevaluasi ekspresi matematika dengan aman.
    Hanya mengizinkan karakter dan fungsi matematika dasar.
    """
    # Daftar karakter yang diizinkan
    allowed_chars = "0123456789.+-*/() "
    
    # Periksa apakah ada karakter yang tidak diizinkan dalam ekspresi
    if any(char not in allowed_chars for char in expression):
        raise ValueError("Karakter tidak valid terdeteksi")

    # eval() bisa berbahaya jika digunakan dengan input sembarangan.
    # Untuk kalkulator sederhana ini, dengan validasi di atas, risikonya minimal.
    # Namun, untuk aplikasi production yang lebih kompleks, pertimbangkan library lain.
    return eval(expression)

# Mendefinisikan rute utama untuk website
@app.route('/', methods=['GET', 'POST'])
def calculator():
    result = None
    expression = ''
    error = None
    
    # Jika ada permintaan POST (saat form disubmit)
    if request.method == 'POST':
        expression = request.form.get('expression', '')
        
        try:
            # Jika ekspresi tidak kosong, coba hitung
            if expression:
                result = safe_eval(expression)
            else:
                result = '' # Jika kosong, tampilkan hasil kosong
        except ZeroDivisionError:
            error = "Error: Tidak bisa dibagi dengan nol!"
        except (SyntaxError, NameError):
            error = "Error: Ekspresi matematika tidak valid!"
        except ValueError as e:
            error = f"Error: {e}"
        except Exception:
            error = "Error: Terjadi kesalahan perhitungan!"
    
    # Dapatkan tahun saat ini
    current_year = datetime.now().year # <-- TAMBAHKAN INI

    # Menampilkan halaman web (index.html) dan mengirimkan variabel
    return render_template('index.html', result=result, expression=expression, error=error)

# Menjalankan aplikasi jika file ini dieksekusi secara langsung
if __name__ == '__main__':
    app.run(debug=True) # debug=True agar mudah saat development
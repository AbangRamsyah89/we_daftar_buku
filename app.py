from flask import Flask, render_template, request, redirect, send_file
import json
import os
import openpyxl

app = Flask(__name__)
DATA_FILE = 'books.json'
def load_books():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_books(books):
    with open(DATA_FILE, 'w') as f:
        json.dump(books, f, indent=2)


# 🔄 Load dan Simpan Buku
def load_books():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_books(books):
    with open(DATA_FILE, 'w') as f:
        json.dump(books, f, indent=4)

# 🏠 Halaman Utama
@app.route('/')
def index():
    books = load_books()
    return render_template('index.html', books=books)
# 🔍 Pencarian Buku
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    books = load_books()

    # Filter buku berdasarkan judul atau penulis
    filtered = [book for book in books if query in book['title'].lower() or query in book['author'].lower()]

    return render_template('index.html', books=filtered, query=query)

# ➕ Tambah Buku
@app.route('/add', methods=['POST'])
def add_book():
    books = load_books()
    new_book = {
        'title': request.form['title'],
        'author': request.form['author'],
        'year': request.form['year'],
        'copies': request.form['copies'],
        'class': request.form['class'],
        'provider': request.form['provider'],
        'budget': request.form['budget'],
        'notes': request.form['notes']
    }
    books.append(new_book)
    save_books(books)
    return redirect('/')


# 📝 Edit Buku
@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_book(index):
    books = load_books()
    if request.method == 'POST':
        books[index]['title'] = request.form['title']
        books[index]['author'] = request.form['author']
        books[index]['jumlah'] = request.form['jumlah']
        books[index]['kelas'] = request.form['kelas']
        save_books(books)
        return redirect('/')
    return render_template('edit.html', book=books[index], index=index)

# ❌ Hapus Buku
@app.route('/delete/<int:index>')
def delete_book(index):
    books = load_books()
    if 0 <= index < len(books):
        books.pop(index)
        save_books(books)
    return redirect('/')

# 📤 Export ke Excel

@app.route('/export')
def export_excel():
    books = load_books()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Daftar Buku"

    # ✅ Header Lengkap
    ws.append(["Judul", "Penulis", "Tahun", "Jumlah Eks", "Kelas", "Penyedia", "Anggaran", "Catatan"])

    # ✅ Isi Data Lengkap
    for book in books:
        ws.append([
            book.get('title', ''),
            book.get('author', ''),
            book.get('year', ''),
            book.get('copies', ''),
            book.get('class', ''),
            book.get('provider', ''),
            book.get('budget', ''),
            book.get('notes', '')
        ])

    filename = "daftar_buku.xlsx"
    wb.save(filename)

    return send_file(filename, as_attachment=True)


# 🚀 Jalankan Flask
if __name__ == '__main__':
    app.run(debug=True)

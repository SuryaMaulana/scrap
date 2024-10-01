import requests  # Library untuk melakukan permintaan HTTP
import csv  # Library untuk mengelola operasi file CSV
from bs4 import BeautifulSoup  # Library untuk memparsing dokumen HTML dan XML

def crawl_kaskus(keyword):
    # Membuat URL untuk endpoint API pencarian Kaskus dengan kata kunci yang diberikan
    url = f"https://www.kaskus.co.id/api/search/threads?sort=lastpost&page=1&searchterm={keyword}&order=desc&content_safety=unsafe&limit=20"
    
    # Mengatur header User-Agent untuk meniru permintaan dari browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }

    try:
        # Mengirim permintaan GET ke API
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Menghasilkan error untuk respons yang buruk (4xx atau 5xx)

        # Memparsing respons JSON dari API
        data = response.json()

        # Memeriksa apakah kunci 'data' ada dalam respons
        if 'data' in data:
            # Membuka file CSV untuk menulis data yang diekstrak
            with open(f"{keyword}_threads.csv", mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Menulis baris header untuk file CSV
                writer.writerow(['Judul Thread', 'URL Thread', 'Tanggal Postingan Terakhir', 'Konten'])

                # Mengiterasi setiap thread dalam data
                for thread in data['data']:
                    title = thread.get('title', '')  # Mengambil judul thread
                    thread_url = thread.get('url', '')  # Mengambil URL thread
                    last_post_date = thread.get('last_post_date', '')  # Mengambil tanggal postingan terakhir
                    content_html = thread.get('content', {}).get('html', '')  # Mengambil konten HTML

                    # Membersihkan konten HTML menggunakan BeautifulSoup
                    soup = BeautifulSoup(content_html, 'html.parser')
                    cleaned_content = soup.get_text(strip=True)  # Mengambil teks bersih dari HTML

                    # Menulis data thread ke dalam file CSV
                    writer.writerow([title, thread_url, last_post_date, cleaned_content])

            print(f"Data disimpan dalam {keyword}_threads.csv")
        else:
            print("Tidak ada data thread ditemukan.")

    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan saat melakukan permintaan: {e}")

if __name__ == "__main__":
    keyword = input("Masukkan kata kunci pencarian: ")  # Meminta input kata kunci dari pengguna
    crawl_kaskus(keyword)  # Memanggil fungsi crawl_kaskus dengan kata kunci yang diberikan

import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import requests

# Load .env
load_dotenv()
WP_API_URL = os.getenv("WP_API_URL")
WP_USER = os.getenv("WP_USER")
WP_PASS = os.getenv("WP_PASS")

def ambil_tabel_cambodia():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            url = "http://146.190.92.226/data-keluaran-cambodia/"

            # Tambahkan retry maksimal 3x
            for attempt in range(3):
                try:
                    print(f"🌐 Akses ke {url} (percobaan {attempt + 1})")
                    page.goto(url, timeout=90000, wait_until="load")
                    page.wait_for_selector("table.baru", timeout=10000)
                    break  # sukses, keluar dari loop
                except Exception as e:
                    print(f"🔁 Gagal buka halaman (percobaan {attempt + 1}): {e}")
                    if attempt == 2:
                        raise  # kalau 3x gagal, lempar error

            html = page.content()
            browser.close()

            soup = BeautifulSoup(html, "html.parser")
            tabel_list = soup.find_all("table", class_="baru")

            if not tabel_list:
                print("❌ Tidak ada tabel ditemukan.")
                return None

            hasil = []

            for table in tabel_list:
                heading = table.find_previous(["h2", "h3", "h4"])
                if heading:
                    hasil.append(f"<{heading.name}>{heading.text.strip()}</{heading.name}>")

                # Ubah warna lama ke warna baru
                table_html = str(table).replace("#68a225", "#29bfe5").replace("#265c00", "#30257d")
                hasil.append(table_html)

            print(f"✅ Ditemukan {len(tabel_list)} tabel + judul.")
            return "\n".join(hasil)

    except Exception as e:
        print(f"❌ Error ambil data: {e}")
        return None


def gabungkan_ke_template(tabel_html):
    try:
        bagian_atas = """
<article id="post-4794" class="single-view post-4794 post type-post status-publish format-standard hentry category-data-cambodia tag-data-cambodia tag-keluaran-cambodia tag-paito-cambodia tag-pengeluaran-kamboja" itemprop="blogPost" itemscope="" itemtype="http://schema.org/BlogPosting">
<header class="entry-header cf">
<h1 class="entry-title" itemprop="headline"><a href="./">Data Keluaran Cambodia 2025</a></h1>
</header>
<div class="entry-byline cf"></div>
<div class="entry-content cf" itemprop="text">
<p><strong>Data Keluaran Cambodia 2025, Data Kamboja 2024, angka pengeluaran magnum cambodia terlengkap</strong></p>
<p>Rekap <strong>pengeluaran togel kamboja</strong> terbaru, Nomor result cambodia Tercepat Hari ini, keluaran kamboja tercepat, Live Cambodia prize 1st. Sebagian dari kalian ada yang mengalami kesulitan untuk melihat Data togel cambodia 2024, maka dari itu adanya situs togeli ini bisa membantu dan mempermudah sobat untuk melihat hasil keluaran cambodia 2025 dengan cepat dan akurat.</p>
<p><strong>Data Cambodia 2024-2025</strong> merupakan kumpulan dari keluaran togel kamboja setiap hari, hasil magnum cambodia ini tentunya di buat menjadi tabel sehingga mudah dalam menggunakannya.</p>
<div id="attachment_4612" style="width: 695px" class="wp-caption alignnone">
<p id="caption-attachment-4612" class="wp-caption-text">Data Keluaran Cambodia 2025, Data kamboja terbaru</p>
</div>
<table>
<tbody>
<tr>
<td>Keluaran togel kamboja aktif setiap hari, sedangkan untuk jam result pengeluaran cambodia berkisar pukul 11.50 WIB.</td>
</tr>
</tbody>
</table>
"""

        bagian_bawah = """
<p><span style="text-decoration: underline;"><strong>Data pengeluaran cambodia</strong></span> hanya selisih beberapa detik dari server resminya, Maka dari itu admin togel merekomendasikan bagi sobat untuk berlangganan di situs ini dengan cara bokmark halaman ini <a href="./"><span style="text-decoration: underline;"><strong>Data Cambodia 2025</strong></span></a> tercepat Hari ini.</p>
<blockquote>
<p>Kami tampilkan juga pada halaman ini <a href="https://result.gbg-coc.org/data-pengeluaran-sydney/"><strong>Data Keluaran Sydney 2025</strong></a></p>
</blockquote>
<p>Angka <strong>pengeluaran togel cambodia</strong> hari ini memang sangat banyak yang mencarinya, Data togel cambodia 2024 terbaru, hasil result kamboja terlengkap. <span style="text-decoration: underline;"><a href="./">Keluaran togel cambodia</a></span> ini kami update dari sumber resminya sehingga tidak perlu diragukan lagi keasliannya.</p>
<p>Sekianlah data keluaran cambodia 2025 yang bisa kami sampaikan, ikuti terus datakeluaran.org untuk mendapatkan hasil pengeluaran togel semua pasaran terutama pencari <em><strong>data kamboja 2025</strong></em> terbaru.</p>
<h4>Incoming search terms:</h4>
<ul>
<li>data kamboja</li>
<li>Data togel kamboja</li>
<li>data cambodia</li>
<li>Data cambodia 2024</li>
<li>Data pengeluaran kamboja</li>
<li>data togel cambodia</li>
<li>Data keluar kamboja 2024</li>
<li>Data togel kbj</li>
</ul></div>
<footer class="entry-footer cf">
</footer>
</article>
"""

        hasil_html = bagian_atas + tabel_html + bagian_bawah

        with open("result_cambodia.html", "w", encoding="utf-8") as f:
            f.write(hasil_html)

        print("✅ result_cambodia.html berhasil dibuat.")
        return hasil_html
    except Exception as e:
        print(f"❌ Error saat gabung template: {e}")
        return None

def post_ke_wordpress(html_content):
    if not WP_API_URL or not WP_USER or not WP_PASS:
        print("❌ Data .env tidak lengkap.")
        return

    headers = {"Content-Type": "application/json"}
    data = {
        "title": "",
        "content": html_content,
        "status": "publish"
    }

    try:
        r = requests.post(WP_API_URL, json=data, auth=(WP_USER, WP_PASS), headers=headers)
        if r.status_code in [200, 201]:
            print("✅ Berhasil posting ke WordPress.")
            print(f"🔗 Link: {r.json().get('link')}")
        else:
            print(f"❌ Gagal post: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"❌ Error saat post ke WordPress: {e}")

if __name__ == "__main__":
    tabel_html = ambil_tabel_cambodia()
    if tabel_html:
        full_html = gabungkan_ke_template(tabel_html)
        if full_html:
            post_ke_wordpress(full_html)

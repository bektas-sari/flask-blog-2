Bu proje, Flask tabanlı bir kişisel blog sitesidir. Kullanıcılar yazıları okuyabilir, sosyal medyada paylaşabilir, ancak yalnızca admin yeni yazılar ekleyebilir, düzenleyebilir ve silebilir.

🚀 Özellikler

* Flask Tabanlı: Hızlı ve hafif bir web framework kullanıldı.
* Admin Paneli: Yeni yazılar ekleme, düzenleme ve silme özellikleri var. Görsel ve çoklu kategori seçimi mümkün hale getirildi.
* Kategori Sistemi: Yazılar "Ben", "Sen", "O", "Sözcükler", "Ve", "Hepimiz" kategorilerine ayrılabilir şekilde düzenlendi.
* SEO Uyumlu: Dinamik meta etiketler.
* Mobil Uyumlu (Responsive): Bootstrap & CSS ile uyumlu tasarım.
* Görsel Destekli Yazılar: Yazılar, 1080x1350 px boyutunda görsellerle sunulur.
* Modern Animasyonlar: Navbar, kartlar ve yazılar için şık efektler.

📌 Kullanılan Teknolojiler
* Python 3.x
* Flask (Web Framework)
* Flask-SQLAlchemy (Veritabanı Yönetimi)
* Flask-WTF (Form Yönetimi)
* SQLite (Veritabanı)
* Jinja2 (Şablon Motoru)
* Bootstrap & Custom CSS (Tasarım)
* JavaScript (Vanilla JS) (Dinamik işlemler)
* Pillow (PIL) (Görsel oluşturma)

📂 Proje Yapısı

/flask_blog
├── /templates
│   ├── base.html (Ana şablon)
│   ├── index.html (Ana sayfa)
│   ├── post_detail.html (Detay sayfası)
│   ├── admin.html (Admin paneli)
│   ├── new_post.html (Yeni yazı ekleme)
├── /static
│   ├── /uploads (Yüklenen görseller)
│   ├── /shareables (Paylaşım görselleri)
│   ├── style.css (CSS dosyaları)
│   ├── script.js (JS dosyaları)
├── app.py (Ana Flask uygulaması)
├── config.py (Ayarlar)
├── database.db (Veritabanı)
├── requirements.txt (Bağımlılıklar)
├── README.md (Bu dosya)

🔧 Kurulum & Çalıştırma

1️⃣ Depoyu Klonla:
git clone https://github.com/kullaniciadi/flask_blog.git
cd flask_blog

2️⃣ Gerekli Paketleri Yükle:
pip install -r requirements.txt

3️⃣ Veritabanını Oluştur:
python
>>> from app import db, app
>>> with app.app_context():
>>>     db.create_all()
>>> exit()

4️⃣ Uygulamayı Başlat:
python app.py

🚀 Şimdi tarayıcından http://127.0.0.1:5000/ adresini ziyaret edebilirsin!

🎯 Geliştirici Notları

Görsellerin Doğru Yüklenmesi: Yüklenen görseller static/uploads/ dizinine kaydedilir.
* Veritabanı Güncellemeleri: Yeni bir alan eklemek için eski veritabanını silip tekrar oluşturabilirsin:

rm database.db
python app.py

📢 Katkıda Bulunma
* Projeye katkıda bulunmak için Pull Request gönderebilir veya hata bildirimi açabilirsin!

🔗 Repo: GitHub - bektas-sari/flask-blog-2

👨‍💻 Geliştirici: Bektas SARI

📜 Lisans
Bu proje, MIT Lisansı altında lisanslanmıştır. 


from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField  # BURAYA SelectField EKLENDİ!
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired
from wtforms import SelectMultipleField  # Çoklu kategori seçimi için
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash
from PIL import Image, ImageDraw, ImageFont
import os

def create_shareable_image(post):
    """Instagram hikayesi formatında bir görsel oluşturur"""
    width, height = 1080, 1920  # Instagram hikaye boyutu
    image = Image.new('RGB', (width, height), color=(255, 255, 255))  # Beyaz arka plan

    draw = ImageDraw.Draw(image)

    # Fontları tanımla (Eğer özel bir font kullanmak istiyorsan, fonts klasörüne koy)
    title_font = ImageFont.truetype("arial.ttf", 80)
    content_font = ImageFont.truetype("arial.ttf", 40)

    # Başlık
    title = post.title
    draw.text((50, 300), title, font=title_font, fill=(0, 0, 0))

    # İçerikten kısa bir alıntı
    preview_text = post.content[:200] + "..."  # İlk 200 karakteri al
    draw.text((50, 500), preview_text, font=content_font, fill=(50, 50, 50))

    # Görseli kaydet
    image_path = f"static/shareables/{post.id}.jpg"
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    image.save(image_path)

    return image_path

# Blog Yazısı Formu
class PostForm(FlaskForm):
    title = StringField('Başlık', validators=[DataRequired()])
    content = TextAreaField('İçerik', validators=[DataRequired()])
    image = FileField('Resim Yükle', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Sadece resim dosyaları yükleyebilirsiniz!')])

    # Güncellenmiş kategori listesi (Çoklu seçim)
    category = SelectMultipleField(
        'Kategoriler',
        choices=[
            ('Ben', 'Ben'),
            ('Sen', 'Sen'),
            ('O', 'O'),
            ('Sözcükler', 'Sözcükler'),
            ('Ve', 'Ve'),
            ('Hepimiz', 'Hepimiz')  # "Hepimiz" kategori listesinden de seçilebilir
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField('Kaydet')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '1234'  # Bunu güvenli bir şifre yap



UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Eğer "uploads" klasörü yoksa oluştur
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



db = SQLAlchemy(app)

# Blog Modeli (Veritabanı Yapısı)
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False, default="Hepimiz")  # Varsayılan olarak "Hepimiz"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)



# Admin Bilgileri
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

# Admin Giriş Formu
class LoginForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    submit = SubmitField('Giriş Yap')

# Blog Yazısı Formu
class PostForm(FlaskForm):
    title = StringField('Başlık', validators=[DataRequired()])
    content = TextAreaField('İçerik', validators=[DataRequired()])
    image = FileField('Resim Yükle', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Sadece resim dosyaları yükleyebilirsiniz!')])
    
    # Çoklu Kategori Seçimi
    category = SelectMultipleField(
        'Kategoriler', 
        choices=[('Ben', 'Ben'), ('Sen', 'Sen'), ('O', 'O'), ('Sözcükler', 'Sözcükler')],
        validators=[DataRequired()]
    )

    submit = SubmitField('Kaydet')

# Ana Sayfa
@app.route('/')
def index():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('index.html', posts=posts)

# Blog Detay Sayfası
@app.route('/post/<int:id>')
def post_detail(id):
    post = BlogPost.query.get_or_404(id)
    return render_template('post_detail.html', post=post)

# Beğeni İşlemi
@app.route('/like/<int:id>', methods=['POST'])
def like_post(id):
    post = BlogPost.query.get_or_404(id)
    post.likes += 1
    db.session.commit()
    return jsonify({'likes': post.likes})

# Admin Giriş
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == ADMIN_USERNAME and form.password.data == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_panel'))
    return render_template('admin_login.html', form=form)

# Admin Paneli
@app.route('/admin/panel')
def admin_panel():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('admin.html', posts=posts)

# Yeni Yazı Ekleme
@app.route('/admin/new', methods=['GET', 'POST'])
def new_post():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    form = PostForm()
    
    if form.validate_on_submit():
        image_file = form.image.data
        if image_file:
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
        else:
            filename = "default.jpg"  # Eğer resim yüklenmezse varsayılan bir resim kullan

        # Seçilen kategorileri liste olarak al ve "Hepimiz" kategorisini ekleyerek kaydet
        selected_categories = form.category.data
        if "Hepimiz" not in selected_categories:
            selected_categories.append("Hepimiz")  # Tüm yazılar otomatik olarak "Hepimiz" kategorisine girecek
        
        category_string = ", ".join(selected_categories)  # Kategorileri virgülle ayırarak saklıyoruz

        new_post = BlogPost(
            title=form.title.data,
            content=form.content.data,
            image=filename,
            category=category_string  # Kategorileri string olarak kaydediyoruz
        )
        db.session.add(new_post)
        db.session.commit()
        
        return redirect(url_for('admin_panel'))
    
    return render_template('new_post.html', form=form)



# Yazıyı Silme
@app.route('/admin/delete/<int:id>')
def delete_post(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('admin_panel'))

# Yazıyı Düzenleme Sayfası
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.category = ','.join(request.form.getlist('category'))  # Çoklu kategori desteği

        # Yeni bir görsel eklenmişse güncelle
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                image.save(image_path)
                post.image = image.filename

        db.session.commit()
        flash('Yazı başarıyla güncellendi!', 'success')
        return redirect(url_for('admin_panel'))

    return render_template('edit_post.html', post=post)


# kategori Filtresi 
@app.route('/category/<string:category>')
def category_filter(category):
    # "Hepimiz" kategorisi özel olduğu için, tüm yazıları gösterir
    if category == "Hepimiz":
        posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    else:
        # Veritabanında kategori sütununda geçen yazıları bul
        posts = BlogPost.query.filter(BlogPost.category.like(f"%{category}%")).order_by(BlogPost.created_at.desc()).all()
    
    return render_template('index.html', posts=posts, selected_category=category)


# Çıkış Yapma
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

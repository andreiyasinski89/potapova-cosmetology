"""Оптимізація матеріалів клієнта для сайту: python tools/build-assets.py <папка з оригіналами>
Оригінали (десятки МБ) у репозиторій не кладуться, тільки WebP/MP4 для сайту."""
import sys, os, subprocess
from PIL import Image, ImageOps
import fitz
SRC = sys.argv[1]; OUT = 'assets'
def img(src, dst, w, q=80, fmt='WEBP'):
    im = Image.open(os.path.join(SRC, src)); im = ImageOps.exif_transpose(im)
    im = im.convert('RGBA' if fmt == 'PNG' else 'RGB')
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(os.path.join(OUT, 'img', dst), fmt, **({'quality': q, 'method': 6} if fmt == 'WEBP' else {'optimize': True}))
IMGS = [
 ('IMG_5577.JPG','doctor.webp',1200),('IMG_5594.JPG','doctor-rejuran.webp',1000),('IMG_5667.JPG','doctor-rejuran2.webp',1000),
 ('IMG_5672.JPG','doctor-sit.webp',1000),('IMG_5583.JPG','doctor-shelf.webp',1000),('IMG_5584.JPG','shelf-back.webp',1000),('IMG_5587.JPG','shelf-image.webp',1000),
 ('IMG_5084.JPG','team.webp',1000),('IMG_5518.JPG','consult.webp',1200),('IMG_5078.JPG','decor.webp',1000),
 ('IMG_5471.JPG','shelf-hydraderm.webp',1000),('клац-1097321321321.jpg','originals-wide.webp',1600),('клац-1097.jpg','originals.webp',1000),
 ('DSC03191.JPG','dmk.webp',1000),('IMG_9908.JPG','dmk-cleanser.webp',900),('IMG_8720.JPG','image-peel.webp',900),('IMG_9782.JPG','image-iluma.webp',900),
 ('AgressiveAntiAgeingProgram.png','zo.webp',1000),('Thalgo.jpg','thalgo.webp',700),('guinot_kosmetyki_profesjonalne.jpg','guinot.webp',1000),
 ('Rejuran insta-02 (2).png','rejuran-poster.webp',1100),('4.png','rejuran-banner.webp',1400),
 ('IMG_5044.JPG','logo-wall.webp',1000),('IMG_5044234234.JPG','logo-wall-wide.webp',1600),('IMG_5044 лого.JPG','og.jpg',1200),
]
for s, d, w in IMGS: img(s, d, w, fmt='JPEG' if d.endswith('.jpg') else 'WEBP') if False else img(s, d, w)
Image.open(os.path.join(SRC,'IMG_5044 лого.JPG')).convert('RGB').resize((1200, round(1675*1200/2532))).save(f'{OUT}/img/og.jpg', quality=82)
img('Potapova.png', 'logo-white.png', 800, fmt='PNG')
fav = Image.open(os.path.join(SRC, 'Фавикон.jpg')).convert('RGB'); fav = fav.resize((128, 128)); fav.save(f'{OUT}/favicon.png')
# ведмідь і темний логотип з PDF
pg = fitz.open(os.path.join(SRC, 'Potapova.pdf'))[0]; r = pg.rect; z = 4
pix = pg.get_pixmap(matrix=fitz.Matrix(z, z)); pix.save('/tmp/logo_pdf.png') if False else pix.save(f'{OUT}/img/_pdf.png')
full = Image.open(f'{OUT}/img/_pdf.png').convert('RGB'); W, H = full.size
sx, sy = W / 909, H / 1286  # координати з перегляду PDF
full.crop((int(225*sx), int(135*sy), int(695*sx), int(335*sy))).save(f'{OUT}/img/logo-dark.webp', quality=90)
full.crop((int(385*sx), int(135*sy), int(555*sx), int(225*sy))).save(f'{OUT}/img/bear.webp', quality=90)
os.remove(f'{OUT}/img/_pdf.png')
# відео
def vid(src, dst, w, crf=28, t=None):
    p = os.path.join(SRC, src); o = f'{OUT}/video/{dst}.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-i',p,'-an','-vf',f'scale={w}:-2,fps=30','-c:v','libx264','-preset','slow','-crf',str(crf),'-pix_fmt','yuv420p','-movflags','+faststart',o],check=True)
    subprocess.run(['ffmpeg','-v','error','-y','-ss','1','-i',p,'-frames:v','1','-vf',f'scale={w}:-2',f'{OUT}/video/{dst}.jpg'],check=True)
vid('IMG_5360.MOV','hero',1080,30); vid('C2763.MP4','massage-1',720); vid('C2788.MP4','massage-2',720); vid('IMG_2704.MOV','rejuran',720)
for f in os.listdir(f'{OUT}/video'):
    if f.endswith('.jpg'):
        Image.open(f'{OUT}/video/{f}').save(f'{OUT}/video/{f[:-4]}.webp','WEBP',quality=78); os.remove(f'{OUT}/video/{f}')

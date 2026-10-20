# -*- coding: utf-8 -*-
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Hearth-Tanitim.pdf"
FONTS = Path(r"C:\Windows\Fonts")

pdfmetrics.registerFont(TTFont("Georgia", str(FONTS / "georgia.ttf")))
pdfmetrics.registerFont(TTFont("Georgia-Bold", str(FONTS / "georgiab.ttf")))
pdfmetrics.registerFont(TTFont("Georgia-Italic", str(FONTS / "georgiai.ttf")))
pdfmetrics.registerFont(TTFont("Segoe", str(FONTS / "segoeui.ttf")))
pdfmetrics.registerFont(TTFont("Segoe-Bold", str(FONTS / "segoeuib.ttf")))
pdfmetrics.registerFont(TTFont("Segoe-Italic", str(FONTS / "segoeuii.ttf")))

INK = HexColor("#2A241F")
MUTED = HexColor("#74695D")
ACCENT = HexColor("#C0562A")
SAGE = HexColor("#3D6B4F")
LINE = HexColor("#E4D9C8")
CREAM = HexColor("#F3EEE4")
SURFACE = HexColor("#FFFDF8")
SOFT = HexColor("#F6E1D4")


def styles():
    return {
        "kicker": ParagraphStyle(
            "kicker",
            fontName="Segoe-Bold",
            fontSize=9,
            textColor=ACCENT,
            letterSpacing=1.4,
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "cover": ParagraphStyle(
            "cover",
            fontName="Georgia-Bold",
            fontSize=36,
            leading=42,
            textColor=INK,
            alignment=TA_CENTER,
            spaceAfter=8,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub",
            fontName="Georgia-Italic",
            fontSize=13,
            leading=18,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "h1": ParagraphStyle(
            "h1",
            fontName="Georgia-Bold",
            fontSize=16,
            leading=22,
            textColor=INK,
            spaceBefore=12,
            spaceAfter=6,
        ),
        "h2": ParagraphStyle(
            "h2",
            fontName="Georgia-Bold",
            fontSize=13.5,
            leading=18,
            textColor=ACCENT,
            spaceBefore=12,
            spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "body",
            fontName="Segoe",
            fontSize=10.5,
            leading=16,
            textColor=INK,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            fontName="Segoe",
            fontSize=10.5,
            leading=15.5,
            textColor=INK,
            leftIndent=14,
            spaceAfter=4,
        ),
        "caption": ParagraphStyle(
            "caption",
            fontName="Segoe-Italic",
            fontSize=9,
            leading=13,
            textColor=MUTED,
            alignment=TA_CENTER,
        ),
        "footer": ParagraphStyle(
            "footer",
            fontName="Segoe",
            fontSize=8,
            textColor=MUTED,
            alignment=TA_CENTER,
        ),
        "cell_title": ParagraphStyle(
            "cell_title",
            fontName="Segoe-Bold",
            fontSize=10,
            leading=13,
            textColor=INK,
        ),
        "cell_body": ParagraphStyle(
            "cell_body",
            fontName="Segoe",
            fontSize=9,
            leading=13,
            textColor=INK,
        ),
        "nav_label": ParagraphStyle(
            "nav_label",
            fontName="Segoe-Bold",
            fontSize=10,
            leading=13,
            textColor=ACCENT,
        ),
    }


S = styles()


def rule():
    return HRFlowable(width="100%", thickness=0.7, color=LINE, spaceBefore=4, spaceAfter=10)


def heading(text):
    return KeepTogether([Paragraph(text, S["h1"]), rule()])


def bullets(items):
    return [Paragraph(f"•  {item}", S["bullet"]) for item in items]


def feature_table(rows):
    data = [[Paragraph("Özellik", S["cell_title"]), Paragraph("Ne işe yarar?", S["cell_title"])]]
    for title, body in rows:
        data.append([Paragraph(title, S["nav_label"]), Paragraph(body, S["cell_body"])])
    table = Table(data, colWidths=[42 * mm, 128 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), SOFT),
                ("BACKGROUND", (0, 1), (-1, -1), SURFACE),
                ("BOX", (0, 0), (-1, -1), 0.4, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return table


def decorate(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(CREAM)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setFillColor(ACCENT)
    canvas.rect(0, A4[1] - 7, A4[0], 7, fill=1, stroke=0)
    canvas.setFillColor(SAGE)
    canvas.rect(0, 0, A4[0], 5, fill=1, stroke=0)
    if doc.page > 1:
        canvas.setFillColor(MUTED)
        canvas.setFont("Segoe", 8)
        canvas.drawString(22 * mm, 11 * mm, "Hearth  ·  Tanıtım ve kullanım yazısı")
        canvas.drawRightString(A4[0] - 22 * mm, 11 * mm, f"{doc.page}")
    canvas.restoreState()


def build():
    story = []

    story.append(Spacer(1, 18 * mm))
    story.append(Paragraph("MASAÜSTÜ UYGULAMA TANITIMI", S["kicker"]))
    story.append(Paragraph("Hearth", S["cover"]))
    story.append(Paragraph("Yerel, sakin bir günlük çalışma alanı", S["cover_sub"]))
    story.append(Spacer(1, 4 * mm))
    story.append(rule())
    story.append(
        Paragraph(
            "Görevler, alışkanlıklar, günlük notları ve odak seansları tek pencerede. "
            "Hesap yok, bulut yok, reklam yok. Her şey bu bilgisayarda kalır.",
            S["cover_sub"],
        )
    )
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph("Eylül 2026  ·  Kullanıcı kılavuzu", S["caption"]))
    story.append(Spacer(1, 14 * mm))

    story.append(heading("1. Bu uygulama ne amacıyla kullanılır?"))
    story.append(
        Paragraph(
            "Hearth, günü parçalara ayırıp başka uygulamalara dağılmadan yönetmek isteyen "
            "tek kişi için yazılmış bir masaüstü çalışma alanıdır. Takım panosu değildir. "
            "Sosyal bir ajanda, hatırlatma yağmuru veya çevrimiçi bir verimlilik ürünü de "
            "değildir. Amacı daha sadedir: bugün ne yapılacak, hangi küçük alışkanlık "
            "tekrarlanacak, zihinde ne kaldı ve bir süre boyunca nasıl derin çalışılacak — "
            "bunların hepsini aynı pencerede, internete çıkmadan tutmak.",
            S["body"],
        )
    )
    story.append(
        Paragraph(
            "Uygulama özellikle şu durumlarda işe yarar. Öğrenci, ödev ve ders çalışma "
            "seanslarını bir arada görmek istediğinde. Yazılımcı veya serbest çalışan, "
            "günün kısa listesini yazıp Pomodoro tarzı odak turlarıyla ilerlemek "
            "istediğinde. Alışkanlık kurmaya çalışan biri, yedi günlük küçük işaretlerle "
            " ritmini kaybetmemek istediğinde. Dijital gürültüden yorulan biri, hesap "
            "açmadan, bildirim duvarı olmadan yalnızca kendi masasında kalmak istediğinde.",
            S["body"],
        )
    )
    story.append(
        Paragraph(
            "Hearth’in bilinçli olarak yapmadığı şeyler de vardır. Görevleri başka "
            "insanlarla paylaşmaz. Takviminle senkron olmaz. Telefonuna buluttan inmez. "
            "Bu bir eksik değil, seçimdir: uygulama tek kişilik bir masa köşesi olarak "
            "tasarlanmıştır. Veri dışarı çıkmadığı için günlük yazıları ve kişisel "
            "görevler de yalnızca bu makinede durur.",
            S["body"],
        )
    )

    story.append(heading("2. Nasıl bir gün için düşünüldü?"))
    story.append(
        Paragraph(
            "Tipik bir kullanım şöyle akar. Sabah uygulamayı açarsın; sol menüden "
            "<b>Bugün</b> seni karşılar. Saatine ve ayarlardaki adına göre bir selamlama "
            "görürsün. Orada bugüne ait açık işler ve haftanın kısa özeti durur. "
            "Yeni işleri <b>Görevler</b> sekmesine yazarsın. Çalışmaya oturunca "
            "<b>Odak</b> ile bir tur başlatırsın. Gün içinde su içmek, yürüyüş veya "
            "kitap gibi küçük tekrarları <b>Alışkanlıklar</b> ızgarasında işaretlersin. "
            "Akşam, aklında kalanı <b>Günlük</b> takvimine bırakırsın. Ertesi sabah "
            "yine Bugün ekranından devam edersin.",
            S["body"],
        )
    )

    story.append(heading("3. Sol menüdeki sekmeler"))
    story.append(
        Paragraph(
            "Pencerenin solunda altı sekme vardır. Her sekme ayrı bir iş içindir; "
            "birbirinin yerine geçmez, birlikte bir günü tamamlar. Aşağıda her sekmenin "
            "hangi özelliği taşıdığı ve o özelliğin ne işe yaradığı anlatılır.",
            S["body"],
        )
    )

    overview = [
        ["Bugün", "Günün özeti: selamlama, bugünkü işler, haftalık sayılar, günün notu."],
        ["Görevler", "İş listesini yazdığın, öncelik ve tarih verdiğin, tamamladığın yer."],
        ["Alışkanlıklar", "Son yedi günü işaretlediğin tekrar ızgarası ve seri sayacı."],
        ["Günlük", "Ay takviminden bir gün seçip o güne özel serbest yazı yazdığın yer."],
        ["Odak", "Odak ve mola zamanlayıcısı, bildirim ve son seans geçmişi."],
        ["Ayarlar", "Ad, süreler, tema, yedek alma ve örnek veriyi sıfırlama."],
    ]
    story.append(feature_table(overview))
    story.append(Spacer(1, 3 * mm))

    story.append(Paragraph("3.1  Bugün", S["h2"]))
    story.append(
        Paragraph(
            "Uygulama açılınca ilk durak burasıdır. Amaç, “şimdi neye bakmalıyım?” "
            "sorusunu tek ekranda cevaplamaktır. Bütün geçmişi veya bütün alışkanlık "
            "ızgarasını burada görmezsin; yalnızca bugüne ait olanı görürsün.",
            S["body"],
        )
    )
    story.append(
        feature_table(
            [
                (
                    "Saate göre selamlama",
                    "Sabah “Günaydın”, öğleden sonra “İyi günler”, akşam “İyi akşamlar” yazar. "
                    "Ayarlar’da bir ad girdiysen selamlama sana döner; girmediysen genel bir hitap kullanır. "
                    "Günün başlangıcını hatırlatır, yeni bir iş eklemez.",
                ),
                (
                    "Bugünün işleri",
                    "Tarihi bugün olan veya henüz tarihi olmayan, bitmemiş görevleri listeler. "
                    "Kutuyu işaretleyerek işi bitmiş sayabilir, sil tuşuyla listeden çıkarabilirsin. "
                    "Buradaki amaç, görev deposunun tamamını değil, bugün masada duran işi göstermektir.",
                ),
                (
                    "Haftalık özet",
                    "Üç sayı yan yana durur: son yedi günde biten görev sayısı, tamamlanan odak "
                    "dakikası ve bugün işaretlenen alışkanlık adedi. İlerlemeyi hissettirir; "
                    "ayrıntılı rapor üretmez.",
                ),
                (
                    "Günün notu",
                    "Günlük sekmesinde bugün için yazılmış metnin ilk bölümünü gösterir. "
                    "Sabah dünün veya bu sabahın cümlesine hızlıca bakmak içindir. "
                    "Notu düzenlemek için Günlük sekmesine geçmen gerekir.",
                ),
            ]
        )
    )

    story.append(Paragraph("3.2  Görevler", S["h2"]))
    story.append(
        Paragraph(
            "Asıl iş listesi buradadır. Hearth bir proje yönetim aracı değildir; "
            "sürükle-bırak panolar, etiket ormanları veya alt görev ağaçları yoktur. "
            "Bunun yerine kısa, öncelikli, tarihli bir kişisel liste sunar. Amaç, "
            "“ne üzerine çalışıyorum?” sorusunu net tutmaktır.",
            S["body"],
        )
    )
    story.append(
        feature_table(
            [
                (
                    "Görev ekleme",
                    "Başlık yazıp Kaydet veya üstteki Görev ekle ile yeni iş oluşturursun. "
                    "Liste en üste eklenir. Boş başlık kabul edilmez.",
                ),
                (
                    "Öncelik",
                    "Düşük, orta veya yüksek seçilir. Renkli bir etiket olarak görünür. "
                    "Hangi işin daha acil durduğunu gözle ayırmanı sağlar; otomatik sıralama yapmaz.",
                ),
                (
                    "Tarih",
                    "İşe bir gün bağlar. Varsayılan bugündür. Bugün sekmesi, tarihi bugün olan "
                    "açık işleri buradan çekerek gösterir.",
                ),
                (
                    "Açık / tamamlanan",
                    "Bitmemiş işler Açık altında, işaretlenenler Tamamlanan altındadır. "
                    "Kutu işaretlenince iş biter ve tamamlanma anı kaydedilir; bu bilgi haftalık özette kullanılır.",
                ),
                (
                    "Silme",
                    "İşi listeden tamamen çıkarır. Geri alma yoktur; yanlışlıkla silinen bir satır yeniden yazılır.",
                ),
            ]
        )
    )

    story.append(Paragraph("3.3  Alışkanlıklar", S["h2"]))
    story.append(
        Paragraph(
            "Bu sekme büyük hedefler için değil, her gün tekrarlanan küçük hareketler "
            "içindir: kitap, yürüyüş, su, dil çalışması gibi. Görevlerden farkı şudur: "
            "görev bir kez bitince kapanır, alışkanlık ise her gün yeniden işaretlenir.",
            S["body"],
        )
    )
    story.append(
        feature_table(
            [
                (
                    "Alışkanlık ekleme",
                    "İsim yazıp Ekle dersen yeni bir satır oluşur. İlk günden itibaren "
                    "yedi günlük ızgarada yerini alır.",
                ),
                (
                    "7 günlük ızgara",
                    "Her alışkanlığın yanında son yedi gün için kareler vardır. Kareye basınca "
                    "o gün işaretlenir veya işareti kalkar. Haftanın ritmini tek bakışta gösterir.",
                ),
                (
                    "Seri sayacı",
                    "Bugünden geriye doğru kesintisiz işaretlenen günleri sayar. "
                    "Zinciri kırmamak için küçük bir motivasyon ölçüsüdür; geçmişi silmez.",
                ),
                (
                    "Silme",
                    "Alışkanlığı ve onun işaret geçmişini kaldırır. Artık takip etmek "
                    "istemediğin bir tekrarı temizlemek içindir.",
                ),
            ]
        )
    )

    story.append(Paragraph("3.4  Günlük", S["h2"]))
    story.append(
        Paragraph(
            "Günlük, görev listesi değildir. Buraya yapılacak iş değil, günde kalan "
            "cümle yazılır: ne yorucu geldi, ne işe yaradı, yarın neyi denemek istiyorsun. "
            "Metin serbesttir; biçimlendirme veya etiket yoktur. Amaç, günün sonunda "
            "zihni boşaltmak ve ileride o güne geri bakabilmektir.",
            S["body"],
        )
    )
    story.append(
        feature_table(
            [
                (
                    "Ay takvimi",
                    "Solda bulunduğun ayın günleri durur. Bir güne basınca o günün yazısı açılır. "
                    "İçinde metin olan günler alt çizgiyle işaretlenir; boş günler sade kalır.",
                ),
                (
                    "Serbest yazı alanı",
                    "Seçilen güne ait not burada durur. Uzun tutulabilir. Kaydetmeden sayfa "
                    "değiştirirsen o anki yazım kaybolabilir; bu yüzden bitince Kaydet denir.",
                ),
                (
                    "Yerel saklama uyarısı",
                    "Ekranda “yalnızca bu bilgisayarda saklanır” yazısı vardır. Günlük "
                    "buluta gitmez, başka cihazda açılmaz.",
                ),
                (
                    "Bugün sekmesiyle bağ",
                    "Bugün ekranındaki “Günün notu”, takvimde bugünün tarihine yazılmış "
                    "metnin kısa bir önizlemesidir. Yazıyı orada değil, bu sekmede düzenlersin.",
                ),
            ]
        )
    )

    story.append(Paragraph("3.5  Odak", S["h2"]))
    story.append(
        Paragraph(
            "Odak sekmesi, listeyi daha da uzatmaz; var olan işin üzerine oturmanı sağlar. "
            "Klasik Pomodoro fikrine yakındır: bir süre dikkat, bir süre mola. "
            "Amaç, “biraz çalışayım”ı ölçülebilir bir tura çevirmektir.",
            S["body"],
        )
    )
    story.append(
        feature_table(
            [
                (
                    "Odak / mola modu",
                    "Tur odak olarak başlar. Süre dolunca otomatik olarak molaya geçer, "
                    "mola bitince yeniden odağa döner. Başlıkta “Derin iş” veya “Mola” yazısı bunu söyler.",
                ),
                (
                    "Başlat",
                    "Geri sayımı işler. Çalışırken düğme “Çalışıyor” olur. "
                    "Ayarlardaki odak veya mola dakikasına göre süre seçilir.",
                ),
                (
                    "Duraklat",
                    "Sayacı durdurur, kalan süreyi korur. Kısa bir kesinti için vardır; "
                    "turu iptal etmez.",
                ),
                (
                    "Sıfırla",
                    "O anki modun süresini başa alır ve sayacı durdurur. "
                    "Yarıda bozulan bir turu yeniden kurmak içindir.",
                ),
                (
                    "Masaüstü bildirimi",
                    "Süre bitince Windows bildirimi çıkar: odak bittiyse mola önerir, "
                    "mola bittiyse yeni tura çağırır. Uygulama arkadaysa da haberdar olursun.",
                ),
                (
                    "Son seanslar",
                    "Tamamlanan son altı turu, türü, bitiş zamanı ve dakika olarak listeler. "
                    "Bugün sekmesindeki “odak dk” sayısı da bu kayıtlardan, son yedi günden hesaplanır.",
                ),
            ]
        )
    )

    story.append(Paragraph("3.6  Ayarlar", S["h2"]))
    story.append(
        Paragraph(
            "Ayarlar, uygulamanın karakterini kişiselleştirdiğin yerdir. "
            "Görev üretmez; diğer sekmelerin nasıl davranacağını belirler.",
            S["body"],
        )
    )
    story.append(
        feature_table(
            [
                (
                    "Görünen ad",
                    "Bugün sekmesindeki selamlamada kullanılır. Boş bırakılırsa genel bir hitap görünür.",
                ),
                (
                    "Odak ve mola süresi",
                    "Varsayılan 25 ve 5 dakikadır. 1–90 ve 1–30 aralığında değiştirilebilir. "
                    "Kaydettikten sonra, zamanlayıcı çalışmıyorsa yeni süre bir sonraki tura uygulanır.",
                ),
                (
                    "Kaydet",
                    "Adı ve süreleri diske yazar. Yazılmazsa bir sonraki açılışta eski değerler gelir.",
                ),
                (
                    "Veriyi dışa aktar",
                    "Tüm görev, alışkanlık, günlük, seans ve ayarları hearth-backup.json olarak indirir. "
                    "Bilgisayar değişmeden önce veya yedek almak için kullanılır.",
                ),
                (
                    "Örnek veriyi sıfırla",
                    "Listeyi temizleyip ilk açılıştaki örnek görev, alışkanlık ve günlük cümlesini geri yükler. "
                    "Deneme verisini silip baştan başlamak içindir; gerçek işlerin varsa önce dışa aktar.",
                ),
                (
                    "Yerel dosya yolu",
                    "Verinin yazıldığı hearth-data.json konumunu gösterir. "
                    "Teknik bir bilgidir; günlük kullanımda dokunmana gerek yoktur.",
                ),
            ]
        )
    )

    story.append(heading("4. Sekmelere ait olmayan, her yerde duran özellikler"))
    story.append(
        feature_table(
            [
                (
                    "Tema düğmesi",
                    "Sol altta durur. Açık krem tema ile koyu mürekkep tema arasında geçer. "
                    "Tercih kaydedilir; bir sonraki açılışta aynı kalır.",
                ),
                (
                    "Tarih çipi",
                    "Sol menünün en altında bugünün uzun tarihi yazar. Hangi günde olduğunu "
                    "kaçırmamak içindir.",
                ),
                (
                    "Yerel kayıt",
                    "Yaptığın her kalıcı değişiklik bu bilgisayardaki bir JSON dosyasına yazılır. "
                    "İnternet kesilse de uygulama çalışır.",
                ),
                (
                    "İlk açılış örnekleri",
                    "İlk çalıştırmada üç örnek görev, üç alışkanlık ve kısa bir günlük cümlesi gelir. "
                    "Ekranın boş durmaması içindir; Ayarlar’dan sıfırlanır veya tek tek silinir.",
                ),
            ]
        )
    )

    story.append(heading("5. Ne değildir, ne içindir?"))
    story.append(
        Paragraph(
            "Hearth bir takvim uygulamasının yerini tutmaz. Toplantı daveti, "
            "paylaşımlı liste veya ofis hatırlatması bekleme. Trello, Notion veya "
            "telefon ajandası da değildir. Daha çok masanın kenarına bırakılmış bir "
            "defter ile bir mutfak zamanlayıcısının birleşimidir.",
            S["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>İçindir:</b> tek kişilik günlük düzen, derin çalışma turları, "
            "küçük alışkanlık takibi, akşam notu, gizlilik isteyen kişisel yazılar.",
            S["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>İçin değildir:</b> ekip iş bölümü, müşteri takibi, bulutta senkron "
            "ajanda, karmaşık proje hiyerarşisi, reklamlı “verimlilik” hizmeti.",
            S["body"],
        )
    )

    story.append(heading("6. Nasıl açılır?"))
    story.append(
        Paragraph(
            "Bilgisayarda Node.js 18 veya üzeri yeterlidir. Proje klasöründe önce "
            "bağımlılıklar kurulur, sonra uygulama başlatılır:",
            S["body"],
        )
    )
    story.append(Paragraph("npm install", S["bullet"]))
    story.append(Paragraph("npm start", S["bullet"]))
    story.append(
        Paragraph(
            "Pencere açılınca sol menüden sekmeler arasında geçersin. Menü çubuğu "
            "gizlidir; dikkat dağınıklığını azaltmak için sade bırakılmıştır.",
            S["body"],
        )
    )

    story.append(heading("7. Kısa kapanış"))
    story.append(
        Paragraph(
            "Hearth, günü yönetmek için yeni bir hayat sistemi vaat etmez. "
            "Daha mütevazı bir iş görür: yapılacakları yazar, tekrarları işaretler, "
            "bir süre boyunca çalışır, günün sonunda birkaç cümle bırakır. "
            "Hepsi aynı masada, aynı pencerede, bu bilgisayarın dışında kimseye gitmeden.",
            S["body"],
        )
    )
    story.append(Spacer(1, 2 * mm))
    story.append(rule())
    story.append(
        Paragraph(
            "Hearth  ·  Yerel masaüstü çalışma alanı  ·  MIT lisansı",
            S["caption"],
        )
    )

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=22 * mm,
        rightMargin=22 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="Hearth — Tanıtım ve kullanım yazısı",
        author="Hearth",
        subject="Hearth masaüstü uygulamasının amacı, sekmeleri ve özellikleri",
    )
    doc.build(story, onFirstPage=decorate, onLaterPages=decorate)
    print(OUT)


if __name__ == "__main__":
    build()

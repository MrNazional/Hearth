# Hearth

Yerel veri saklayan, sade bir masaüstü çalışma alanı. Görevler, alışkanlıklar, günlük notları ve Pomodoro tarzı odak seansları tek pencerede durur. İnternet hesabı, bulut veya takip yok.

A local-first desktop workspace for daily tasks, habits, journaling, and focus sessions. Everything stays on your machine.

## Neden bu proje?

Bir yazılımcının yaklaşık bir haftada bitirebileceği ölçüde tutuldu:

- Tek pencere, altı ekran, net bir veri modeli
- Hazır bir backend veya kullanıcı sistemi yok
- Electron + sade HTML/CSS/JS; derleme adımı yok
- GitHub’a konunca “çalışan ürün” gibi duracak kadar tamam, aşırı şişirilmemiş

## Özellikler

- **Bugün:** selamlama, bugünün görevleri, haftalık özet, günün notu
- **Görevler:** öncelik, tarih, tamamlama, silme
- **Alışkanlıklar:** 7 günlük işaret ızgarası ve seri sayacı
- **Günlük:** ay takvimi, güne özel serbest yazı
- **Odak:** odak / mola zamanlayıcı, bildirim, seans geçmişi
- **Ayarlar:** ad, süreler, açık/koyu tema, JSON dışa aktarma

Veriler Electron `userData` klasöründeki `hearth-data.json` dosyasına yazılır.

## Gereksinimler

- Node.js 18+
- Windows, macOS veya Linux

## Çalıştırma

```bash
npm install
npm start
```

## Teknik yapı

```text
electron/main.cjs      pencere, dosya kaydı, bildirimler
electron/preload.cjs   güvenli IPC köprüsü
renderer/index.html    kabuk arayüz
renderer/styles.css    açık/koyu tema
renderer/app.js        ekranlar ve durum yönetimi
```

Güvenlik için `contextIsolation` açık, `nodeIntegration` kapalı. Arayüz yalnızca preload üzerinden veri okur ve yazar.

## GitHub’a ekleme

```bash
git init
git add .
git commit -m "Add Hearth desktop workspace"
git branch -M main
git remote add origin https://github.com/KULLANICI/hearthdesk.git
git push -u origin main
```

İlk açılışta örnek görevler ve alışkanlıklar gelir. Ayarlar’dan sıfırlanabilir.

## Sonraki adımlar

Paketlemek için `electron-builder` eklenebilir. İstersen arama, etiketler veya yedek içe aktarma da bir sonraki haftaya bırakılabilir.

## Lisans

MIT

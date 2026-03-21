#!/usr/bin/env python3
"""
Fix Turkish character encoding in JSON files.
Uses whole-word matching with comprehensive suffix expansion.
"""

import json
import re
import sys
import os


# ─── WHOLE-WORD CORRECTIONS ─────────────────────────────────────────────
# These are exact whole-word matches (case-insensitive).
# Generated from roots + common Turkish suffixes.

def _expand_roots():
    """Generate word corrections from roots and suffixes."""
    corrections = {}

    # Each entry: (ascii_root, turkish_root, list_of_suffix_pairs)
    # suffix_pairs: (ascii_suffix, turkish_suffix)
    # Empty suffix means the root itself is a word

    # Common Turkish suffixes (ascii -> turkish)
    BASIC_SUFFIXES = [
        ("", ""),
        ("i", "i"),
        ("u", "u"),
        ("a", "a"),
        ("e", "e"),
        ("in", "in"),
        ("un", "un"),
        ("da", "da"),
        ("de", "de"),
        ("dan", "dan"),
        ("den", "den"),
        ("la", "la"),
        ("le", "le"),
        ("lar", "lar"),
        ("ler", "ler"),
        ("lari", "ları"),
        ("leri", "leri"),
        ("larin", "ların"),
        ("lerin", "lerin"),
        ("larini", "larını"),
        ("lerini", "lerini"),
        ("larinizi", "larınızı"),
        ("ni", "ni"),
        ("nu", "nu"),
        ("na", "na"),
        ("ne", "ne"),
        ("nin", "nin"),
        ("nun", "nun"),
        ("nda", "nda"),
        ("nde", "nde"),
        ("ndan", "ndan"),
        ("nden", "nden"),
        ("ya", "ya"),
        ("ye", "ye"),
        ("yi", "yi"),
        ("yu", "yu"),
        ("dir", "dir"),
        ("dur", "dur"),
        ("tir", "tir"),
        ("tur", "tur"),
        ("tan", "tan"),
        ("ten", "ten"),
        ("sal", "sal"),
        ("sel", "sel"),
        ("si", "sı"),
        ("su", "su"),
        ("ini", "ini"),
        ("unu", "unu"),
        ("ine", "ine"),
        ("une", "une"),
        ("ini", "ini"),
        ("inin", "inin"),
        ("unun", "unun"),
        ("inda", "ında"),
        ("inde", "inde"),
        ("indan", "ından"),
        ("inden", "inden"),
        ("sini", "sını"),
        ("sunu", "sunu"),
        ("sina", "sına"),
        ("sinda", "sında"),
        ("sinde", "sinde"),
        ("sindan", "sından"),
        ("sinin", "sının"),
        ("li", "li"),
        ("lu", "lu"),
        ("siz", "siz"),
        ("suz", "suz"),
        ("lik", "lik"),
        ("luk", "luk"),
        ("ligi", "liği"),
        ("lugu", "luğu"),
        ("ligini", "liğini"),
        ("liginin", "liğinin"),
        ("liginde", "liğinde"),
        ("ci", "ci"),
        ("cu", "cu"),
        ("cilik", "cilik"),
        ("cilar", "cılar"),
        ("cilari", "cıları"),
        ("nin", "nin"),
    ]

    # Root definitions: (ascii_form, turkish_form, extra_suffixed_forms)
    # extra_suffixed_forms is a list of (ascii_word, turkish_word) for irregular forms
    roots = [
        # ─── ç words ───
        ("calis", "çalış", [
            ("calisma", "çalışma"), ("calismasi", "çalışması"), ("calismasini", "çalışmasını"), ("calismak", "çalışmak"),
            ("calismada", "çalışmada"), ("calismanizi", "çalışmanızı"),
            ("calismaya", "çalışmaya"), ("calismayi", "çalışmayı"),
            ("calismalarini", "çalışmalarını"), ("calismadin", "çalışmadın"),
            ("calismiyor", "çalışmıyor"), ("calismay", "çalışmay"),
            ("calismsa", "çalışmsa"), ("calismayin", "çalışmayın"),
            ("calisan", "çalışan"), ("calisanlar", "çalışanlar"), ("calisanlari", "çalışanları"),
            ("calisir", "çalışır"), ("calisirken", "çalışırken"),
            ("calisabilir", "çalışabilir"), ("calisabilecek", "çalışabilecek"),
            ("calisalim", "çalışalım"), ("calisssin", "çalışsın"),
            ("calistigi", "çalıştığı"), ("calistigimi", "çalıştığımı"),
            ("calistiginda", "çalıştığında"), ("calistigini", "çalıştığını"),
            ("calistiginiz", "çalıştığınız"), ("calistigin", "çalıştığın"),
            ("calistir", "çalıştır"), ("calistirin", "çalıştırın"),
            ("calistirir", "çalıştırır"), ("calistirma", "çalıştırma"),
            ("calistirmak", "çalıştırmak"), ("calistirmayi", "çalıştırmayı"),
            ("calistirilabilecegi", "çalıştırılabileceği"),
            ("calistirilmasi", "çalıştırılması"), ("calistirilmasinda", "çalıştırılmasında"),
            ("calistirilmayan", "çalıştırılmayan"),
            ("calistirmadan", "çalıştırmadan"),
            ("calistiranlar", "çalıştıranlar"), ("calistirarak", "çalıştırarak"),
            ("calisti", "çalıştı"), ("calistim", "çalıştım"),
            ("calisin", "çalışın"), ("calisiyor", "çalışıyor"),
            ("calisiyorum", "çalışıyorum"), ("calisacagim", "çalışacağım"),
            ("calismma", "çalışma"),
        ]),
        ("cik", "çık", [
            ("cikti", "çıktı"), ("ciktisi", "çıktısı"), ("ciktisini", "çıktısını"),
            ("ciktilarini", "çıktılarını"), ("ciktiyi", "çıktıyı"),
            ("cikar", "çıkar"), ("cikarir", "çıkarır"), ("cikarmak", "çıkarmak"),
            ("cikarma", "çıkarma"), ("cikariyor", "çıkarıyor"),
            ("cikarilabilir", "çıkarılabilir"), ("cikmak", "çıkmak"),
            ("cikma", "çıkma"),
        ]),
        ("coz", "çöz", [
            ("cozum", "çözüm"), ("cozumu", "çözümü"), ("cozumun", "çözümün"),
            ("cozumunde", "çözümünde"), ("cozumler", "çözümler"),
            ("cozumleri", "çözümleri"), ("cozumlerin", "çözümlerin"),
            ("cozumlerle", "çözümlerle"), ("cozumlemek", "çözümlemek"),
            ("cozumleme", "çözümleme"), ("cozmek", "çözmek"),
            ("cozme", "çözme"), ("cozulmustur", "çözülmüştür"),
            ("cozume", "çözüme"), ("cozumlerindeki", "çözümlerindeki"),
            ("cozumlerini", "çözümlerini"), ("cozumunu", "çözümünü"),
            ("cozumunuzu", "çözümünüzü"),
        ]),
        ("cok", "çok", [("coklu", "çoklu"), ("cokluboyutlu", "çokluBoyutlu")]),
        ("cog", "çoğ", [
            ("cogu", "çoğu"), ("cogunluk", "çoğunluk"), ("cogaltma", "çoğaltma"),
        ]),
        ("cev", "çev", [
            ("ceviri", "çeviri"), ("cevirici", "çevirici"), ("cevirmek", "çevirmek"),
            ("cevirme", "çevirme"), ("cevre", "çevre"), ("cevresi", "çevresi"),
            ("cevresel", "çevresel"), ("cevrimici", "çevrimiçi"),
            ("cevrimdisi", "çevrimdışı"), ("cevirdi", "çevirdi"),
            ("cevirdim", "çevirdim"), ("ceviren", "çeviren"), ("cevirir", "çevirir"),
        ]),
        ("cerceve", "çerçeve", [
            ("cercevesi", "çerçevesi"), ("cercevesinde", "çerçevesinde"),
            ("cercevesidir", "çerçevesidir"),
        ]),
        ("cesit", "çeşit", [
            ("cesitli", "çeşitli"), ("cesitleri", "çeşitleri"),
        ]),
        ("cek", "çek", [
            ("cekmek", "çekmek"), ("cekme", "çekme"), ("ceker", "çeker"),
            ("cekici", "çekici"), ("cekilme", "çekilme"), ("cekin", "çekin"),
            ("cekinir", "çekinir"), ("cekti", "çekti"),
        ]),

        # ─── ğ words ───
        ("degis", "değiş", [
            ("degisken", "değişken"), ("degiskene", "değişkene"), ("degiskeni", "değişkeni"),
            ("degiskenin", "değişkenin"), ("degiskenleri", "değişkenleri"),
            ("degiskenler", "değişkenler"), ("degiskenlerle", "değişkenlerle"),
            ("degiskendir", "değişkendir"), ("degiskenlik", "değişkenlik"),
            ("degiskenlere", "değişkenlere"), ("degiskeninde", "değişkeninde"),
            ("degistir", "değiştir"), ("degistirme", "değiştirme"),
            ("degistirilmis", "değiştirilmiş"), ("degistirilmesi", "değiştirilmesi"),
            ("degistirmek", "değiştirmek"), ("degistirmeyi", "değiştirmeyi"),
            ("degistirir", "değiştirir"), ("degistirin", "değiştirin"),
            ("degistirirken", "değiştirirken"), ("degistirmede", "değiştirmede"),
            ("degistirmeden", "değiştirmeden"), ("degistirmekten", "değiştirmekten"),
            ("degistirmesini", "değiştirmesini"), ("degistirmeye", "değiştirmeye"),
            ("degistirmez", "değiştirmez"), ("degistirildi", "değiştirildi"),
            ("degistirilebilecegi", "değiştirilebileceği"),
            ("degistirilebilen", "değiştirilebilen"),
            ("degistirilebilir", "değiştirilebilir"),
            ("degistirilemeyen", "değiştirilemeylen"),
            ("degistirilemez", "değiştirilemez"), ("degistirilemezlik", "değiştirilemezlik"),
            ("degistirici", "değiştirici"), ("degistiginde", "değiştiğinde"),
            ("degistigini", "değiştiğini"), ("degistirildi", "değiştirildi"),
            ("degisiklik", "değişiklik"), ("degisikligi", "değişikliği"),
            ("degisikligin", "değişikliğin"), ("degisikliginde", "değişikliğinde"),
            ("degisiklikle", "değişiklikle"), ("degisikliklere", "değişikliklere"),
            ("degisiklikleri", "değişiklikleri"), ("degisiklikler", "değişiklikler"),
            ("degisikliklerle", "değişikliklerle"), ("degisikliklerin", "değişikliklerin"),
            ("degisikliklerinde", "değişikliklerinde"),
            ("degisikliklerine", "değişikliklerine"),
            ("degisikliklerini", "değişikliklerini"),
            ("degisikliklerinin", "değişikliklerinin"),
            ("degisikliklerinizi", "değişikliklerinizi"),
            ("degisiklikleriyle", "değişiklikleriyle"),
            ("degisiklige", "değişikliğe"),
            ("degisim", "değişim"), ("degisimleri", "değişimleri"),
            ("degisimi", "değişimi"),
            ("degisen", "değişen"), ("degisir", "değişir"), ("degisirse", "değişirse"),
            ("degisme", "değişme"), ("degismez", "değişmez"),
            ("degismezligi", "değişmezliği"), ("degismezlik", "değişmezlik"),
            ("degismemeli", "değişmemeli"), ("degismeyen", "değişmeyen"),
            ("degistigini", "değiştiğini"), ("degistirildi", "değiştirildi"),
            ("degistiginde", "değiştiğinde"), ("degisiklige", "değişikliğe"),
            ("degisikligin", "değişikliğin"),
            ("degistirememe", "değiştirememe"),
            ("degistirilmesini", "değiştirilmesini"),
            ("degistirildigini", "değiştirildiğini"),
        ]),
        ("deger", "değer", [
            ("degeri", "değeri"), ("degerin", "değerin"), ("degerini", "değerini"),
            ("degerinin", "değerinin"), ("degerlere", "değerlere"),
            ("degerler", "değerler"), ("degerleri", "değerleri"),
            ("degerlerini", "değerlerini"), ("degerli", "değerli"),
            ("degerlendirme", "değerlendirme"), ("degerlendirmek", "değerlendirmek"),
            ("degerlendirmesi", "değerlendirmesi"),
            ("degerlendirmesinde", "değerlendirmesinde"),
            ("degerlendirir", "değerlendirir"), ("degerlendirin", "değerlendirin"),
            ("degerlendirmede", "değerlendirmede"),
            ("degerlendirmem", "değerlendirmem"),
            ("degerlendirmez", "değerlendirmez"),
            ("degerlendir", "değerlendir"),
            ("degerlendirdiginiz", "değerlendirdiğiniz"),
            ("degerlendiren", "değerlendiren"),
            ("degerlendirinsin", "değerlendirsinler"),
            ("degerlendirirken", "değerlendirirken"),
            ("degerlendirirler", "değerlendirirler"),
        ]),
        ("degil", "değil", []),

        # ─── ş words ───
        ("basari", "başarı", [
            ("basarili", "başarılı"), ("basarilarini", "başarılarını"),
            ("basariyi", "başarıyı"), ("basarisiz", "başarısız"),
            ("basarisizlik", "başarısızlık"), ("basarisizligi", "başarısızlığı"),
            ("basarisizligin", "başarısızlığın"), ("basarisizligini", "başarısızlığını"),
            ("basarisizliklari", "başarısızlıkları"),
            ("basarilar", "başarılar"), ("basarilari", "başarıları"),
            ("basarilarinizi", "başarılarınızı"), ("basarilarla", "başarılarla"),
            ("basarisi", "başarısı"), ("basarisina", "başarısına"),
        ]),
        ("basla", "başla", [
            ("baslamak", "başlamak"), ("baslama", "başlama"), ("baslamadan", "başlamadan"),
            ("baslamasina", "başlamasına"), ("baslar", "başlar"),
            ("baslarken", "başlarken"), ("baslat", "başlat"),
            ("baslatma", "başlatma"), ("baslatmak", "başlatmak"),
            ("basladi", "başladı"), ("basladiginda", "başladığında"),
            ("baslayan", "başlayan"), ("baslayanlar", "başlayanlar"),
            ("baslayarak", "başlayarak"), ("basliyor", "başlıyor"),
        ]),
        ("baslangi", "başlangı", [
            ("baslangic", "başlangıç"), ("baslangicindan", "başlangıcından"),
            ("baslangiclari", "başlangıçları"),
            ("baslangici", "başlangıcı"), ("baslangicinda", "başlangıcında"),
        ]),
        ("baslik", "başlık", [
            ("basligi", "başlığı"), ("basliklari", "başlıkları"),
            ("basliklarini", "başlıklarını"),
        ]),
        ("baska", "başka", [("baskasi", "başkası")]),
        ("basvuru", "başvuru", [
            ("basvurusu", "başvurusu"), ("basvurularinizi", "başvurularınızı"),
            ("basvuruyor", "başvuruyor"), ("basvuruyorum", "başvuruyorum"),
            ("basvurulari", "başvuruları"), ("basvurular", "başvurular"),
            ("basvurulara", "başvurulara"), ("basvurularda", "başvurularda"),
            ("basvuruldu", "başvuruldu"), ("basvurumu", "başvurumu"),
            ("basvurusunda", "başvurusunda"), ("basvuruya", "başvuruya"),
            ("basvuruyu", "başvuruyu"), ("basvurudan", "başvurudan"),
        ]),
        ("bilesen", "bileşen", [
            ("bileseni", "bileşeni"), ("bilesenin", "bileşenin"),
            ("bilesenler", "bileşenler"), ("bilesenleri", "bileşenleri"),
            ("bilesenlere", "bileşenlere"), ("bilesende", "bileşende"),
            ("bilesenden", "bileşenden"), ("bilesene", "bileşene"),
            ("bilesenle", "bileşenle"),
        ]),
        ("birlestir", "birleştir", [
            ("birlestirme", "birleştirme"), ("birlestirmek", "birleştirmek"),
            ("birlestir", "birleştir"), ("birlesik", "birleşik"),
            ("birlesme", "birleşme"), ("birlestiren", "birleştiren"),
            ("birlestirilebilecegini", "birleştirilebileceğini"),
            ("birlestirilmis", "birleştirilmiş"), ("birlestirirken", "birleştirirken"),
            ("birlestiriyor", "birleştiriyor"), ("birlestirmede", "birleştirmede"),
            ("birlestirmeden", "birleştirmeden"), ("birlestirmekte", "birleştirmekte"),
            ("birlestirmesi", "birleştirmesi"), ("birlestirmesiydi", "birleştirmesiydi"),
            ("birlesmeden", "birleşmeden"),
        ]),
        ("bocek", "böcek", []),
        ("bolum", "bölüm", [
            ("bolumu", "bölümü"), ("bolumler", "bölümler"), ("bolumleri", "bölümleri"),
            ("bolunmus", "bölünmüş"), ("bolumine", "bölümine"),
            ("bolumlere", "bölümlere"), ("bolumunde", "bölümünde"),
            ("bolumune", "bölümüne"), ("bolumunu", "bölümünü"),
            ("bolumund", "bölümund"),
        ]),
        ("bosluk", "boşluk", [
            ("boslugu", "boşluğu"), ("boslugunu", "boşluğunu"), ("bosluktan", "boşluktan"),
        ]),
        ("buyuk", "büyük", [
            ("buyukluk", "büyüklük"), ("buyuklugu", "büyüklüğü"),
            ("buyuklugune", "büyüklüğüne"),
        ]),
        ("buyume", "büyüme", [("buyumesi", "büyümesi")]),
        ("butun", "bütün", [
            ("butunlesik", "bütünleşik"), ("butunlestirme", "bütünleştirme"),
        ]),
        ("dagitim", "dağıtım", [
            ("dagitimi", "dağıtımı"), ("dagitimini", "dağıtımını"),
            ("dagitan", "dağıtan"), ("dagitilan", "dağıtılan"),
            ("dagitik", "dağıtık"), ("dagitmak", "dağıtmak"),
            ("dagitiminda", "dağıtımında"), ("dagitimdan", "dağıtımdan"),
        ]),
        ("dagilim", "dağılım", []),
        ("dogrulama", "doğrulama", [
            ("dogrulamak", "doğrulamak"), ("dogrulamasi", "doğrulaması"),
            ("dogrulamada", "doğrulamada"), ("dogrulamadan", "doğrulamadan"),
            ("dogrulamasinda", "doğrulamasında"),
        ]),
        ("dogrula", "doğrula", []),
        ("dogrudan", "doğrudan", []),
        ("dogru", "doğru", [("dogrusu", "doğrusu"), ("dogruluk", "doğruluk")]),
        ("dokumantasyon", "dokümantasyon", [
            ("dokumantasyonu", "dokümantasyonu"),
            ("dokumantasyondan", "dokümantasyondan"),
            ("dokumantasyonunu", "dokümantasyonunu"),
            ("dokumantasyonunun", "dokümantasyonunun"),
        ]),
        ("dokumante", "dokümante", []),
        ("dokuman", "doküman", [
            ("dokumani", "dokümanı"), ("dokumanlar", "dokümanlar"),
            ("dokumanlari", "dokümanları"),
        ]),
        ("donem", "dönem", [
            ("donemi", "dönemi"), ("donemin", "dönemin"), ("donemim", "dönemim"),
            ("doneminde", "döneminde"), ("donemlerinde", "dönemlerinde"),
            ("donemeine", "dönemine"),
        ]),
        ("dongu", "döngü", [
            ("donguler", "döngüler"), ("donguleri", "döngüleri"),
            ("donguyu", "döngüyü"), ("donguye", "döngüye"),
            ("dongude", "döngüde"), ("dongunun", "döngünün"),
            ("donguden", "döngüden"), ("dongusu", "döngüsü"),
            ("dongusunde", "döngüsünde"), ("dongusunu", "döngüsünü"),
            ("dongutun", "döngütün"),
        ]),
        ("donus", "dönüş", [
            ("donusum", "dönüşüm"), ("donusumu", "dönüşümü"),
            ("donusturmek", "dönüştürmek"), ("donusturme", "dönüştürme"),
            ("donusturuyor", "dönüştürüyor"), ("donusturulur", "dönüştürülür"),
            ("donusu", "dönüşü"), ("donusturen", "dönüştüren"),
            ("donusturulebilir", "dönüştürülebilir"),
            ("donusturulmesi", "dönüştürülmesi"),
        ]),
        ("donuyor", "dönüyor", []),
        ("dun", "dün", []),
        ("dunya", "dünya", [
            ("dunyada", "dünyada"), ("dunyasi", "dünyası"),
            ("dunyasinda", "dünyasında"), ("dunyanin", "dünyanın"),
        ]),
        ("duzenleme", "düzenleme", [
            ("duzenlenmesi", "düzenlenmesi"), ("duzenlemek", "düzenlemek"),
            ("duzenlemede", "düzenlemede"),
        ]),
        ("duzenli", "düzenli", []),
        ("duzgun", "düzgün", []),
        ("duzey", "düzey", [
            ("duzeyde", "düzeyde"), ("duzeyi", "düzeyi"),
            ("duzeyinde", "düzeyinde"), ("duzeyini", "düzeyini"),
            ("duzeylerde", "düzeylerde"),
        ]),
        ("duzeltilecek", "düzeltilecek", []),
        ("dusun", "düşün", [
            ("dusunme", "düşünme"), ("dusunmek", "düşünmek"),
            ("dusunmeyi", "düşünmeyi"), ("dusunce", "düşünce"),
            ("dusuncesi", "düşüncesi"), ("dusuncelerini", "düşüncelerini"),
            ("dusundum", "düşündüm"), ("dusundunuz", "düşündünüz"),
            ("dusunebilen", "düşünebilen"), ("dusunebilir", "düşünebilir"),
            ("dusuneyim", "düşüneyim"), ("dusunmeden", "düşünmeden"),
            ("dusunmem", "düşünmem"), ("dusunmeme", "düşünmeme"),
            ("dusunmez", "düşünmez"), ("dusunmuyor", "düşünmüyor"),
            ("dusunulerek", "düşünülerek"), ("dusunun", "düşünün"),
            ("dusunur", "düşünür"), ("dusunursunuz", "düşünürsünüz"),
            ("dusunuyorsaniz", "düşünüyorsanız"), ("dusunuyorsun", "düşünüyorsun"),
            ("dusunuyorsunuz", "düşünüyorsunuz"), ("dusunuyorum", "düşünüyorum"),
        ]),
        ("dusuk", "düşük", []),
        ("dusurme", "düşürme", [("dusurur", "düşürür")]),
        ("dusuyor", "düşüyor", []),
        ("erisim", "erişim", [
            ("erisimi", "erişimi"), ("erisimini", "erişimini"),
            ("erisilebilir", "erişilebilir"), ("erisilebilirlik", "erişilebilirlik"),
            ("erisimde", "erişimde"), ("erisime", "erişime"),
            ("erisiminden", "erişiminden"),
        ]),
        ("etkilesim", "etkileşim", [
            ("etkilesimi", "etkileşimi"), ("etkilesimli", "etkileşimli"),
            ("etkilesimden", "etkileşimden"), ("etkilesime", "etkileşime"),
            ("etkilesimlerine", "etkileşimlerine"),
        ]),
        ("farkli", "farklı", [
            ("farkliliklari", "farklılıkları"), ("farklilik", "farklılık"),
            ("farklidir", "farklıdır"),
        ]),
        ("gecersiz", "geçersiz", [("gecersizse", "geçersizse")]),
        ("gecerli", "geçerli", [
            ("gecerliligi", "geçerliliği"), ("gecerlilik", "geçerlilik"),
        ]),
        ("gecis", "geçiş", [("gecisi", "geçişi")]),
        ("gecmis", "geçmiş", [
            ("gecmisi", "geçmişi"), ("gecmiste", "geçmişte"),
        ]),
        ("gecici", "geçici", []),
        ("gecirmek", "geçirmek", [("gecirdigim", "geçirdiğim")]),
        ("geciyor", "geçiyor", []),
        ("gecmiyor", "geçmiyor", []),
        ("gecmeyecek", "geçmeyecek", []),
        ("geciktirme", "geciktirme", []),  # already correct
        ("gelistir", "geliştir", [
            ("gelistirme", "geliştirme"), ("gelistirmek", "geliştirmek"),
            ("gelistirmede", "geliştirmede"), ("gelistirmesi", "geliştirmesi"),
            ("gelistirmeye", "geliştirmeye"), ("gelistirmeyi", "geliştirmeyi"),
            ("gelistirmesinde", "geliştirmesinde"),
            ("gelistirici", "geliştirici"), ("gelistiriciler", "geliştiriciler"),
            ("gelistiricileri", "geliştiricileri"),
            ("gelistiricilerin", "geliştiricilerin"),
            ("gelistiricinin", "geliştiricinin"),
            ("gelistiriciyle", "geliştiriciyle"),
            ("gelistir", "geliştir"), ("gelistirdigimiz", "geliştirdiğimiz"),
            ("gelistirdigim", "geliştirdiğim"), ("gelistirdim", "geliştirdim"),
            ("gelistirdin", "geliştirdin"), ("gelistirdi", "geliştirdi"),
            ("gelistirin", "geliştirin"), ("gelistirilmis", "geliştirilmiş"),
            ("gelistirilmistir", "geliştirilmiştir"),
            ("gelistiren", "geliştiren"), ("gelistirerek", "geliştirerek"),
            ("gelistirilebilecek", "geliştirilebilecek"),
            ("gelistirilen", "geliştirilen"),
            ("gelistirilmeye", "geliştirilmeye"),
            ("gelistirir", "geliştirir"), ("gelistirirken", "geliştirirken"),
            ("gelistiriyorum", "geliştiriyorum"),
            ("gelistirmeden", "geliştirmeden"),
            ("gelistirmesini", "geliştirmesini"),
            ("gelistirmez", "geliştirmez"),
            ("gelistirmis", "geliştirmiş"),
        ]),
        ("gelismis", "gelişmiş", []),
        ("gelisen", "gelişen", []),
        ("gelisim", "gelişim", [
            ("gelisimi", "gelişimi"), ("gelisimini", "gelişimini"),
            ("gelisimlerini", "gelişimlerini"),
        ]),
        ("genis", "geniş", [
            ("genislik", "genişlik"), ("genisligi", "genişliği"),
            ("genisletme", "genişletme"), ("genisletilebilir", "genişletilebilir"),
            ("genisletilmis", "genişletilmiş"),
            ("genislemeye", "genişlemeye"), ("genisleten", "genişleten"),
            ("genisletilebilecegi", "genişletilebileceği"),
            ("genisletin", "genişletin"), ("genisletmek", "genişletmek"),
        ]),
        ("gercek", "gerçek", [
            ("gercekten", "gerçekten"), ("gercekte", "gerçekte"),
            ("gercekci", "gerçekçi"), ("gercekleri", "gerçekleri"),
            ("gerceklestirmek", "gerçekleştirmek"),
            ("gerceklestirme", "gerçekleştirme"),
            ("gerceklestir", "gerçekleştir"),
            ("gerceklestirdim", "gerçekleştirdim"),
            ("gerceklestirilmek", "gerçekleştirilmek"),
            ("gerceklesiyor", "gerçekleşiyor"),
            ("gerceklesen", "gerçekleşen"),
            ("gerceklestiginde", "gerçekleştiğinde"),
        ]),
        ("giris", "giriş", [
            ("girisi", "girişi"), ("girisim", "girişim"), ("girisimci", "girişimci"),
            ("girisimler", "girişimler"), ("girisleri", "girişleri"),
        ]),
        ("gorsel", "görsel", [
            ("gorselleri", "görselleri"), ("gorseli", "görseli"),
            ("gorselestirmek", "görselleştirmek"), ("gorseller", "görseller"),
        ]),
        ("gorunum", "görünüm", [
            ("gorunumu", "görünümü"), ("gorunumunu", "görünümünü"),
        ]),
        ("gorunur", "görünür", [
            ("gorunurluk", "görünürlük"), ("gorunurlugu", "görünürlüğü"),
        ]),
        ("goruntulemek", "görüntülemek", []),
        ("goruntuleme", "görüntüleme", [("goruntulenmesi", "görüntülenmesi")]),
        ("gorus", "görüş", [
            ("gorusme", "görüşme"), ("gorusmeleri", "görüşmeleri"),
        ]),
        ("gorev", "görev", [
            ("gorevi", "görevi"), ("gorevleri", "görevleri"),
            ("gorevlerini", "görevlerini"),
        ]),
        ("gosterge", "gösterge", [
            ("gostergesi", "göstergesi"), ("gostergeleri", "göstergeleri"),
        ]),
        ("goster", "göster", [
            ("gostermek", "göstermek"), ("gosterir", "gösterir"),
            ("gosterici", "gösterici"), ("gostericisini", "göstericisini"),
            ("gostericisinin", "göstericisinin"),
            ("gosterilir", "gösterilir"), ("gosterilen", "gösterilen"),
            ("gosteriyor", "gösteriyor"), ("gosterecek", "gösterecek"),
            ("gosterilebilir", "gösterilebilir"),
            ("gosterimleri", "gösterimleri"), ("gosterimi", "gösterimi"),
            ("gosterim", "gösterim"), ("gosterin", "gösterin"),
            ("gosterdi", "gösterdi"), ("gosterdigim", "gösterdiğim"),
            ("gosteren", "gösteren"), ("gostermis", "göstermiş"),
            ("gostersin", "göstersin"), ("gosterilecek", "gösterilecek"),
            ("gostereyim", "göstereyim"), ("gosterirken", "gösterirken"),
        ]),
        ("gozetim", "gözetim", []),
        ("goc", "göç", [("gocler", "göçler")]),
        ("gonderme", "gönderme", []),
        ("gondermek", "göndermek", []),
        ("gonderilir", "gönderilir", []),
        ("gonderilen", "gönderilen", []),
        ("gonderim", "gönderim", []),
        ("gonderen", "gönderen", []),
        ("gonderi", "gönderi", []),
        ("gonullu", "gönüllü", []),
        ("guvenlik", "güvenlik", [
            ("guvenligi", "güvenliği"), ("guvenligini", "güvenliğini"),
            ("guvenli", "güvenli"), ("guvenlikte", "güvenlikte"),
        ]),
        ("guclu", "güçlü", []),
        ("guc", "güç", [
            ("gucu", "gücü"), ("gucunu", "gücünü"),
            ("guclendirme", "güçlendirme"),
        ]),
        ("guncelleme", "güncelleme", [
            ("guncellemek", "güncellemek"), ("guncellestirme", "güncelleme"),
            ("guncellemede", "güncellemede"), ("guncellemelerinde", "güncellemelerinde"),
            ("guncellemelerinin", "güncellemelerinin"),
            ("guncellemenizi", "güncellemenizi"), ("guncellemesi", "güncellemesi"),
            ("guncellemeyi", "güncellemeyi"), ("guncellemez", "güncellemez"),
            ("guncellemeleri", "güncellemeleri"), ("guncellemeler", "güncellemeler"),
        ]),
        ("guncelle", "güncelle", [
            ("guncellendi", "güncellendi"), ("guncelleniyor", "güncelleniyor"),
            ("guncellediginde", "güncellendiğinde"),
            ("guncellerken", "güncellerken"), ("guncelleyen", "güncelleyen"),
            ("guncelleyin", "güncelleyin"),
        ]),
        ("guncellmesi", "güncellmesi", []),
        ("guncellmez", "güncellmez", []),
        ("guncel", "güncel", []),
        ("hizli", "hızlı", [("hizlica", "hızlıca")]),
        ("hizla", "hızla", [("hizlandirmak", "hızlandırmak")]),
        ("hiz", "hız", [("hizi", "hızı"), ("hizini", "hızını")]),
        ("icerik", "içerik", [
            ("icerigi", "içeriği"), ("icerigini", "içeriğini"),
            ("icerikleri", "içerikleri"), ("icerikle", "içerikle"),
            ("icerikten", "içerikten"),
        ]),
        ("iceren", "içeren", []),
        ("icerir", "içerir", []),
        ("iceriyor", "içeriyor", []),
        ("icerisinde", "içerisinde", []),
        ("iceri", "içeri", [("icerige", "içeriğe")]),
        ("icinde", "içinde", [("icindeki", "içindeki")]),
        ("icinden", "içinden", []),
        ("icine", "içine", []),
        ("icindir", "içindir", []),
        ("icin", "için", []),
        ("icsel", "içsel", []),
        ("ihtiyac", "ihtiyaç", [
            ("ihtiyaci", "ihtiyacı"), ("ihtiyaclari", "ihtiyaçları"),
            ("ihtiyacim", "ihtiyacım"), ("ihtiyacimiz", "ihtiyacımız"),
            ("ihtiyacina", "ihtiyacına"), ("ihtiyacini", "ihtiyacını"),
            ("ihtiyaclarina", "ihtiyaçlarına"),
        ]),
        ("iliski", "ilişki", [
            ("iliskileri", "ilişkileri"), ("iliskilerinin", "ilişkilerinin"),
            ("iliskisel", "ilişkisel"), ("iliskili", "ilişkili"),
            ("iliskiler", "ilişkiler"), ("iliskilendiremez", "ilişkilendiremez"),
        ]),
        ("isaret", "işaret", [
            ("isaretci", "işaretçi"), ("isaretlemek", "işaretlemek"),
            ("isaretleme", "işaretleme"), ("isaretinde", "işaretinde"),
            ("isaretler", "işaretler"), ("isaretlerini", "işaretlerini"),
            ("isaretleyen", "işaretleyen"), ("isaretleyici", "işaretleyici"),
            ("isaretledigi", "işaretlediği"), ("isaretlenmis", "işaretlenmiş"),
        ]),
        ("isbirligi", "işbirliği", [("isbirligini", "işbirliğini")]),
        ("islem", "işlem", [
            ("islemi", "işlemi"), ("islemler", "işlemler"), ("islemleri", "işlemleri"),
            ("islemlerin", "işlemlerin"), ("islemlerini", "işlemlerini"),
            ("islemci", "işlemci"), ("islemcileri", "işlemcileri"),
            ("isleme", "işleme"), ("islemede", "işlemede"),
            ("islemeden", "işlemeden"), ("islemek", "işlemek"),
            ("islemeye", "işlemeye"), ("islemin", "işlemin"),
            ("isleminde", "işleminde"), ("islemlerde", "işlemlerde"),
            ("islemlerinde", "işlemlerinde"),
        ]),
        ("islev", "işlev", [
            ("islevi", "işlevi"), ("islevsel", "işlevsel"),
            ("islevselligi", "işlevselliği"), ("islevselligini", "işlevselliğini"),
            ("islevsellik", "işlevsellik"), ("islevselliin", "işlevselliin"),
            ("islevsellikle", "işlevsellikle"), ("islevleri", "işlevleri"),
            ("islevlerini", "işlevlerini"),
        ]),
        ("isleyis", "işleyiş", [
            ("isleyisi", "işleyişi"), ("isleyisini", "işleyişini"),
        ]),
        ("islenmis", "işlenmiş", []),
        ("issizlik", "işsizlik", []),
        ("issiz", "işsiz", []),
        ("isveren", "işveren", [
            ("isverene", "işverene"), ("isverenler", "işverenler"),
            ("isverenleri", "işverenleri"), ("isverenlerin", "işverenlerin"),
        ]),
        ("iscilik", "işçilik", []),
        ("isci", "işçi", []),
        ("kalitim", "kalıtım", [("kalitimi", "kalıtımı"), ("kalitimla", "kalıtımla")]),
        ("kaldir", "kaldır", [
            ("kaldirmak", "kaldırmak"), ("kaldirma", "kaldırma"),
            ("kaldiracagi", "kaldıracağı"), ("kaldiracak", "kaldıracak"),
            ("kaldirilacak", "kaldırılacak"), ("kaldirildi", "kaldırıldı"),
            ("kaldirilmak", "kaldırılmak"), ("kaldirin", "kaldırın"),
        ]),
        ("kanit", "kanıt", [
            ("kanitlama", "kanıtlama"), ("kanitlamak", "kanıtlamak"),
            ("kanitlayacagini", "kanıtlayacağını"),
            ("kaniti", "kanıtı"), ("kanitla", "kanıtla"),
            ("kanitladi", "kanıtladı"), ("kanitlar", "kanıtlar"),
            ("kanitlari", "kanıtları"), ("kanitlarina", "kanıtlarına"),
        ]),
        ("kapsayici", "kapsayıcı", [
            ("kapsayicilarda", "kapsayıcılarda"),
            ("kapsayicilastirma", "kapsayıcılaştırma"),
            ("kapsayicilastirmak", "kapsayıcılaştırmak"),
            ("kapsayicisi", "kapsayıcısı"), ("kapsayiciya", "kapsayıcıya"),
        ]),
        ("karmasik", "karmaşık", [
            ("karmasikligi", "karmaşıklığı"), ("karmasiklik", "karmaşıklık"),
            ("karmasikligina", "karmaşıklığına"), ("karmasikligini", "karmaşıklığını"),
            ("karmasikliginin", "karmaşıklığının"), ("karmasiksa", "karmaşıksa"),
        ]),
        ("karsilastir", "karşılaştır", [
            ("karsilastirma", "karşılaştırma"), ("karsilastirmak", "karşılaştırmak"),
            ("karsilastiralim", "karşılaştıralım"), ("karsilastirici", "karşılaştırıcı"),
            ("karsilastirirken", "karşılaştırırken"),
            ("karsilastirmali", "karşılaştırmalı"), ("karsilastirmasi", "karşılaştırması"),
        ]),
        ("karsilasma", "karşılaşma", [("karsilasmak", "karşılaşmak")]),
        ("karsilama", "karşılama", []),
        ("karsilik", "karşılık", [
            ("karsiligi", "karşılığı"), ("karsilikli", "karşılıklı"),
        ]),
        ("karsi", "karşı", [("karsisinda", "karşısında"), ("karsisindaki", "karşısındaki")]),
        ("katilabilecek", "katılabilecek", []),
        ("kayit", "kayıt", [("kayitlari", "kayıtları")]),
        ("kaynaklari", "kaynakları", []),
        ("kaynakli", "kaynaklı", []),
        ("kisayollar", "kısayollar", []),
        ("klasor", "klasör", [("klasoru", "klasörü"), ("klasorunu", "klasörünü")]),
        ("kosul", "koşul", [
            ("kosulu", "koşulu"), ("kosullar", "koşullar"), ("kosullari", "koşulları"),
            ("kosullu", "koşullu"), ("kosulsuz", "koşulsuz"),
            ("kosulari", "koşulları"), ("kosullarini", "koşullarını"),
            ("kosulun", "koşulun"), ("kosulunu", "koşulunu"),
        ]),
        ("kucuk", "küçük", [("kucultmek", "küçültmek")]),
        ("kuresel", "küresel", []),
        ("kultur", "kültür", [
            ("kulturel", "kültürel"), ("kulturunu", "kültürünü"),
            ("kulturuyle", "kültürüyle"),
        ]),
        ("kutuphane", "kütüphane", [
            ("kutuphaneleri", "kütüphaneleri"), ("kutuphanesi", "kütüphanesi"),
            ("kutuphanesini", "kütüphanesini"),
        ]),
        ("modul", "modül", [
            ("modulu", "modülü"), ("moduller", "modüller"), ("modulleri", "modülleri"),
            ("moduldeki", "modüldeki"), ("modullerini", "modüllerini"),
            ("modulun", "modülün"), ("modulunu", "modülünü"),
        ]),
        ("muhendis", "mühendis", [
            ("muhendislik", "mühendislik"), ("muhendisligi", "mühendisliği"),
            ("muhendisligine", "mühendisliğine"), ("muhendisligini", "mühendisliğini"),
            ("muhendisi", "mühendisi"), ("muhendislerin", "mühendislerin"),
        ]),
        ("mulakat", "mülakat", [
            ("mulakatta", "mülakatta"), ("mulakati", "mülakatı"),
            ("mulakatlari", "mülakatları"), ("mulakatlarda", "mülakatlarda"),
            ("mulakatci", "mülakatçı"), ("mulakatim", "mülakatım"),
            ("mulakatin", "mülakatın"), ("mulakatina", "mülakatına"),
            ("mulakatinda", "mülakatında"), ("mulakatlara", "mülakatlara"),
            ("mulakatten", "mülakattan"), ("mulakattinda", "mülakattında"),
        ]),
        ("mukemmel", "mükemmel", [
            ("mukemmeliyetcilik", "mükemmeliyetçilik"),
            ("mukemmeliyetini", "mükemmeliyetini"),
        ]),
        ("mumkun", "mümkün", [("mumkunse", "mümkünse"), ("mumkundur", "mümkündür")]),
        ("musteri", "müşteri", [
            ("musteriler", "müşteriler"), ("musterileri", "müşterileri"),
            ("musteriye", "müşteriye"), ("musterinin", "müşterinin"),
            ("musterisi", "müşterisi"),
        ]),
        ("ogren", "öğren", [
            ("ogrenmek", "öğrenmek"), ("ogrenme", "öğrenme"),
            ("ogrenmeye", "öğrenmeye"), ("ogrenmege", "öğrenmeye"),
            ("ogrenmeyi", "öğrenmeyi"), ("ogrenmesi", "öğrenmesi"),
            ("ogrenmeliyim", "öğrenmeliyim"), ("ogrenmez", "öğrenmez"),
            ("ogrenci", "öğrenci"), ("ogrenciler", "öğrenciler"),
            ("ogrenim", "öğrenim"), ("ogrenimini", "öğrenimini"),
            ("ogrenimez", "öğrenimez"),
            ("ogrendigim", "öğrendiğim"), ("ogrendiginiz", "öğrendiğiniz"),
            ("ogrendiklerini", "öğrendiklerini"), ("ogrendikten", "öğrendikten"),
            ("ogrendim", "öğrendim"), ("ogrendin", "öğrendin"),
            ("ogrendi", "öğrendi"), ("ogrendigini", "öğrendiğini"),
            ("ogrenilen", "öğrenilen"), ("ogrenin", "öğrenin"),
            ("ogrenirim", "öğrenirim"), ("ogrenirken", "öğrenirken"),
            ("ogreniyorum", "öğreniyorum"), ("ogrenrir", "öğrenrir"),
            ("ogrenm", "öğrenm"),
        ]),
        ("ogretici", "öğretici", []),
        ("ogretim", "öğretim", []),
        ("ogretmen", "öğretmen", []),
        ("olasi", "olası", [
            ("olasilik", "olasılık"), ("olasiliklari", "olasılıkları"),
        ]),
        ("olcek", "ölçek", [
            ("olceklenebilir", "ölçeklenebilir"),
            ("olceklenebilirlik", "ölçeklenebilirlik"),
            ("olceklenebilirligi", "ölçeklenebilirliği"),
            ("olcekli", "ölçekli"), ("olceklenmez", "ölçeklenmez"),
            ("olcekte", "ölçekte"), ("olceklendirme", "ölçeklendirme"),
        ]),
        ("olcut", "ölçüt", []),
        ("olcum", "ölçüm", [("olcume", "ölçüme"), ("olcumleme", "ölçümleme")]),
        ("olustur", "oluştur", [
            ("olusturma", "oluşturma"), ("olusturmak", "oluşturmak"),
            ("olusturmayi", "oluşturmayı"), ("olusturmaya", "oluşturmaya"),
            ("olusturmasi", "oluşturması"), ("olusturmada", "oluşturmada"),
            ("olusturmadan", "oluşturmadan"), ("olusturmasini", "oluşturmasını"),
            ("olusturmaz", "oluşturmaz"),
            ("olusturun", "oluşturun"), ("olusturur", "oluşturur"),
            ("olusturulur", "oluşturulur"), ("olusturulan", "oluşturulan"),
            ("olusturulmus", "oluşturulmuş"), ("olusturulabilir", "oluşturulabilir"),
            ("olusturucu", "oluşturucu"),
            ("olustirma", "oluşturma"),
            ("olusturan", "oluşturan"), ("olusturarak", "oluşturarak"),
            ("olusturdugu", "oluşturduğu"), ("olusturdum", "oluşturdum"),
            ("olusturdm", "oluşturdum"), ("olusturdur", "oluşturdur"),
            ("olusturuldu", "oluşturuldu"), ("olusturuldugu", "oluşturulduğu"),
            ("olusturuldugunda", "oluşturulduğunda"),
            ("olusturulduktan", "oluşturulduktan"),
            ("olusturulmadan", "oluşturulmadan"), ("olusturulmak", "oluşturulmak"),
            ("olusturulmali", "oluşturulmalı"),
            ("olustururken", "oluştururken"), ("olustururlar", "oluştururlar"),
            ("olusturursan", "oluşturursun"),
        ]),
        ("olusan", "oluşan", []),
        ("olusur", "oluşur", []),
        ("olusum", "oluşum", []),
        ("olusuyor", "oluşuyor", []),
        ("olusmuyor", "oluşmuyor", []),
        ("olustugu", "oluştuğu", [
            ("olustugunda", "oluştuğunda"), ("olustugunu", "oluştuğunu"),
        ]),
        ("oldugu", "olduğu", [
            ("oldugumu", "olduğumu"), ("olduguna", "olduğuna"),
            ("oldugunca", "olduğunca"), ("oldugunda", "olduğunda"),
            ("oldugundan", "olduğundan"), ("oldugunu", "olduğunu"),
            ("oldugunun", "olduğunun"), ("oldugunuz", "olduğunuz"),
            ("oldugunuzu", "olduğunuzu"), ("oldugunuzun", "olduğunuzun"),
            ("olduggumuzu", "olduğumuzu"),
        ]),
        ("onem", "önem", [
            ("onemi", "önemi"), ("onemli", "önemli"),
            ("onemlisi", "önemlisi"), ("onemliligi", "önemliliği"),
            ("onemini", "önemini"), ("onemlidir", "önemlidir"),
            ("onemsmez", "önemsmez"),
        ]),
        ("oneri", "öneri", [
            ("onerileri", "önerileri"), ("onerir", "önerir"),
            ("onermek", "önermek"),
        ]),
        ("once", "önce", [("onceden", "önceden"), ("onceki", "önceki")]),
        ("oncelik", "öncelik", [
            ("onceliklendirme", "önceliklendirme"), ("oncelikli", "öncelikli"),
        ]),
        ("onbellek", "önbellek", [("onbellege", "önbelleğe"), ("onbellegi", "önbelleği")]),
        ("onlem", "önlem", [("onlemek", "önlemek"), ("onleme", "önleme")]),
        ("ornek", "örnek", [
            ("ornegi", "örneği"), ("ornekler", "örnekler"),
            ("ornekleri", "örnekleri"), ("orneklerle", "örneklerle"),
            ("ornegin", "örneğin"), ("orneklendirmek", "örneklendirmek"),
            ("orneklerin", "örneklerin"), ("ornekli", "örnekli"),
            ("orneklenemeyen", "örneklenemeyen"),
        ]),
        ("ozel", "özel", [
            ("ozellestirme", "özelleştirme"), ("ozellestirilmis", "özelleştirilmiş"),
            ("ozellestir", "özelleştir"),
        ]),
        ("ozellik", "özellik", [
            ("ozelligi", "özelliği"), ("ozellikleri", "özellikleri"),
            ("ozelliklerini", "özelliklerini"), ("ozellikle", "özellikle"),
        ]),
        ("ozgun", "özgün", []),
        ("ozgur", "özgür", []),
        ("ozet", "özet", [("ozeti", "özeti"), ("ozetlemek", "özetlemek")]),
        ("ozkaynak", "özkaynak", [("ozkaynaklar", "özkaynaklar")]),
        ("paylasim", "paylaşım", [
            ("paylasimi", "paylaşımı"), ("paylasiminda", "paylaşımında"),
            ("paylasiminiz", "paylaşımınız"), ("paylasimlara", "paylaşımlara"),
            ("paylasimlarin", "paylaşımların"), ("paylasimlarina", "paylaşımlarına"),
        ]),
        ("paylasan", "paylaşan", []),
        ("paylasmak", "paylaşmak", []),
        ("paylasma", "paylaşma", []),
        ("parca", "parça", [
            ("parcasi", "parçası"), ("parcalama", "parçalama"),
            ("parcalamak", "parçalamak"), ("parcalari", "parçaları"),
            ("parcali", "parçalı"), ("parcasindaki", "parçasındaki"),
            ("parcasini", "parçasını"), ("parcasinin", "parçasının"),
            ("parcalanmasini", "parçalanmasını"), ("parcalamaz", "parçalamaz"),
            ("parcalara", "parçalara"),
            ("parcacigi", "parçacığı"), ("parcaciginda", "parçacığında"),
            ("parcacigini", "parçacığını"), ("parcaciginin", "parçacığının"),
        ]),
        ("sagla", "sağla", [
            ("saglama", "sağlama"), ("saglamak", "sağlamak"),
            ("saglayan", "sağlayan"), ("saglar", "sağlar"),
            ("sagladi", "sağladı"), ("sagladigi", "sağladığı"),
            ("sagladim", "sağladım"), ("saglanan", "sağlanan"),
            ("saglandigi", "sağlandığı"), ("saglayin", "sağlayın"),
            ("saglayabilecegime", "sağlayabileceğime"),
            ("saglayabilecegini", "sağlayabileceğini"),
            ("saglayabilecek", "sağlayabilecek"),
            ("saglayabilir", "sağlayabilir"),
            ("saglamadan", "sağlamadan"), ("saglamamda", "sağlamamda"),
        ]),
        ("saglam", "sağlam", [("saglamligi", "sağlamlığı")]),
        ("saglik", "sağlık", []),
        ("saldiri", "saldırı", [("saldirilarin", "saldırıların"), ("saldirisi", "saldırısı")]),
        ("sayi", "sayı", [
            ("sayisi", "sayısı"), ("sayisal", "sayısal"), ("sayisini", "sayısını"),
            ("sayida", "sayıda"), ("sayilar", "sayılar"), ("sayilari", "sayıları"),
            ("sayilarla", "sayılarla"), ("sayilir", "sayılır"),
            ("sayilmasi", "sayılması"), ("sayisiz", "sayısız"),
        ]),
        ("sifre", "şifre", [
            ("sifreleme", "şifreleme"), ("sifrelemek", "şifrelemek"),
            ("sifreli", "şifreli"), ("sifreleyen", "şifreleyen"),
            ("sifremi", "şifremi"),
        ]),
        ("sinif", "sınıf", [
            ("sinifi", "sınıfı"), ("sinifin", "sınıfın"), ("siniflar", "sınıflar"),
            ("siniflari", "sınıfları"), ("siniflandirma", "sınıflandırma"),
            ("siniflandirarak", "sınıflandırarak"),
            ("siniflandirilmasi", "sınıflandırılması"),
            ("siniflandirmada", "sınıflandırmada"),
            ("siniflarindan", "sınıflarından"), ("siniflarini", "sınıflarını"),
            ("sinifta", "sınıfta"), ("siniftan", "sınıftan"),
            ("sinifa", "sınıfa"), ("sinifindan", "sınıfından"),
        ]),
        ("sira", "sıra", [
            ("sirada", "sırada"), ("siradan", "sıradan"), ("sirayla", "sırayla"),
            ("sirasinda", "sırasında"), ("sirasiyla", "sırasıyla"),
            ("siralanir", "sıralanır"), ("siraya", "sıraya"),
            ("sirasi", "sırası"), ("sirasini", "sırasını"),
            ("sirasinin", "sırasının"), ("siradi", "sıradı"),
        ]),
        ("siralama", "sıralama", [
            ("siralamak", "sıralamak"), ("siralamasini", "sıralamasını"),
            ("siralanmis", "sıralanmış"),
        ]),
        ("sirali", "sıralı", []),
        ("sonuc", "sonuç", [
            ("sonuclari", "sonuçları"), ("sonuclarini", "sonuçlarını"),
            ("sonuclanir", "sonuçlanır"), ("sonuclar", "sonuçlar"),
            ("sonuclara", "sonuçlara"), ("sonuclarindaki", "sonuçlarındaki"),
        ]),
        ("sozcuk", "sözcük", []),
        ("sozluk", "sözlük", []),
        ("sozdizimi", "sözdizimi", []),
        ("sozkonusu", "sözkonusu", []),
        ("sozde", "sözde", []),
        ("soyleme", "söyleme", [("soylemek", "söylemek")]),
        ("surec", "süreç", [
            ("sureci", "süreci"), ("surecin", "sürecin"),
            ("surecleri", "süreçleri"), ("surecinde", "sürecinde"),
            ("surecini", "sürecini"), ("sureclerinde", "süreçlerinde"),
            ("sureclerini", "süreçlerini"), ("sureclerinizi", "süreçlerinizi"),
            ("surece", "sürece"), ("sureccnizi", "süreçlerinizi"),
            ("surecindeki", "sürecindeki"), ("surecinin", "sürecinin"),
        ]),
        ("sure", "süre", [
            ("sureyi", "süreyi"), ("sureden", "süreden"), ("suresi", "süresi"),
            ("surede", "sürede"), ("suresini", "süresini"),
            ("suresinin", "süresinin"), ("surelerini", "sürelerini"),
            ("sureli", "süreli"), ("surebilir", "sürebilir"),
            ("surer", "sürer"), ("surerse", "sürerse"),
            ("suremizdeki", "süremizdeki"), ("surecegini", "süreceğini"),
        ]),
        ("surekli", "sürekli", [("sureklilik", "süreklilik")]),
        ("surum", "sürüm", [
            ("surumu", "sürümü"), ("surumler", "sürümler"), ("surumleri", "sürümleri"),
        ]),
        ("surdur", "sürdür", [
            ("surdurmek", "sürdürmek"), ("surdurulebilir", "sürdürülebilir"),
            ("surdurulebilirlik", "sürdürülebilirlik"),
        ]),
        ("tamsayi", "tamsayı", []),
        ("tanimla", "tanımla", [
            ("tanimlama", "tanımlama"), ("tanimlamak", "tanımlamak"),
            ("tanimlamakta", "tanımlamakta"), ("tanimlamada", "tanımlamada"),
            ("tanimlamadan", "tanımlamadan"), ("tanimlamaz", "tanımlamaz"),
            ("tanimlandi", "tanımlandı"), ("tanimlanmis", "tanımlanmış"),
            ("tanimlanmamis", "tanımlanmamış"), ("tanimlanir", "tanımlanır"),
            ("tanimlanan", "tanımlanan"), ("tanimlarken", "tanımlarken"),
            ("tanimlayan", "tanımlayan"), ("tanimlayici", "tanımlayıcı"),
            ("tanimlayicisi", "tanımlayıcısı"), ("tanimlayin", "tanımlayın"),
        ]),
        ("tanim", "tanım", [
            ("tanimi", "tanımı"), ("tanimlari", "tanımları"), ("tanimlar", "tanımlar"),
        ]),
        ("tanit", "tanıt", [("tanitim", "tanıtım"), ("tanitimi", "tanıtımı")]),
        ("tasarim", "tasarım", [
            ("tasarimi", "tasarımı"), ("tasarimci", "tasarımcı"),
            ("tasarimda", "tasarımda"), ("tasarimdaki", "tasarımdaki"),
            ("tasarimdan", "tasarımdan"), ("tasarimin", "tasarımın"),
            ("tasariminda", "tasarımında"), ("tasarimini", "tasarımını"),
            ("tasariminin", "tasarımının"), ("tasarimlar", "tasarımlar"),
            ("tasarimlarini", "tasarımlarını"),
        ]),
        ("tasinabilir", "taşınabilir", []),
        ("tasima", "taşıma", []),
        ("tesekkur", "teşekkür", [("tesekkurler", "teşekkürler")]),
        ("tur", "tür", [
            ("turu", "türü"), ("turleri", "türleri"), ("turlerini", "türlerini"),
            ("turunde", "türünde"), ("turlu", "türlü"),
        ]),
        ("uyari", "uyarı", [
            ("uyarilari", "uyarıları"), ("uyarilar", "uyarılar"),
            ("uyarilarini", "uyarılarını"), ("uyarisi", "uyarısı"),
            ("uyarisini", "uyarısını"), ("uyariyla", "uyarıyla"),
        ]),
        ("uzerinde", "üzerinde", [("uzerindeyim", "üzerindeyim"), ("uzerindeki", "üzerindeki")]),
        ("uzerinden", "üzerinden", []),
        ("uzerine", "üzerine", []),
        ("uzere", "üzere", []),
        ("ust", "üst", [
            ("ustu", "üstü"), ("ustun", "üstün"), ("ustunluk", "üstünlük"),
            ("ustunde", "üstünde"), ("ustune", "üstüne"),
        ]),
        ("uretim", "üretim", [("uretimi", "üretimi")]),
        ("uretme", "üretme", [("uretmek", "üretmek")]),
        ("ureten", "üreten", []),
        ("uretici", "üretici", []),
        ("urun", "ürün", [
            ("urunu", "ürünü"), ("urunler", "ürünler"), ("urunleri", "ürünleri"),
        ]),
        ("ucretsiz", "ücretsiz", []),
        ("ucretli", "ücretli", []),
        ("ucret", "ücret", [("ucreti", "ücreti")]),
        ("uye", "üye", [("uyelik", "üyelik")]),
        ("varsayilan", "varsayılan", [
            ("varsayilani", "varsayılanı"), ("varsayimlari", "varsayımları"),
        ]),
        ("yaklasim", "yaklaşım", [
            ("yaklasimi", "yaklaşımı"), ("yaklasimin", "yaklaşımın"),
            ("yaklasimim", "yaklaşımım"), ("yaklasimlar", "yaklaşımlar"),
            ("yaklasimini", "yaklaşımını"), ("yaklasiminizi", "yaklaşımınızı"),
            ("yaklasimlarini", "yaklaşımlarını"), ("yaklasimlariniz", "yaklaşımlarınız"),
        ]),
        ("yaklasarak", "yaklaşarak", []),
        ("yapi", "yapı", [
            ("yapisi", "yapısı"), ("yapilari", "yapıları"), ("yapilarin", "yapıların"),
            ("yapisal", "yapısal"), ("yapilir", "yapılır"), ("yapilan", "yapılan"),
            ("yapilmasi", "yapılması"), ("yapilabilir", "yapılabilir"),
            ("yapilacak", "yapılacak"), ("yapilmis", "yapılmış"),
            ("yapiyor", "yapıyor"),
            ("yapimi", "yapımı"), ("yapiyi", "yapıyı"),
            ("yapici", "yapıcı"), ("yapiciyi", "yapıcıyı"),
            ("yapilabilirlik", "yapılabilirlik"), ("yapilabiliyor", "yapılabiliyor"),
            ("yapilacagini", "yapılacağını"), ("yapilamiyor", "yapılamıyor"),
            ("yapildiginda", "yapıldığında"), ("yapildigini", "yapıldığını"),
            ("yapildgini", "yapıldığını"), ("yapildi", "yapıldı"),
            ("yapilirsa", "yapılırsa"), ("yapiliyor", "yapılıyor"),
            ("yapilmak", "yapılmak"), ("yapilmali", "yapılmalı"),
            ("yapilmamasi", "yapılmaması"), ("yapilmayi", "yapılmayı"),
            ("yapilmiyor", "yapılmıyor"), ("yapilsin", "yapılsın"),
            ("yapin", "yapın"), ("yapip", "yapıp"),
            ("yapisini", "yapısını"), ("yapisinin", "yapısının"),
            ("yapiyordu", "yapıyordu"), ("yapiyorsaniz", "yapıyorsanız"),
            ("yapiyorsun", "yapıyorsun"), ("yapiyorum", "yapıyorum"),
            ("yapiyoruz", "yapıyoruz"),
        ]),
        ("yapistir", "yapıştır", [
            ("yapisirmak", "yapıştırmak"), ("yapistirdiktan", "yapıştırdıktan"),
            ("yapistin", "yapıştın"),
        ]),
        ("yapilandirma", "yapılandırma", [
            ("yapilandirmak", "yapılandırmak"),
            ("yapilandirmasi", "yapılandırması"),
            ("yapilandirmasini", "yapılandırmasını"),
            ("yapilandir", "yapılandır"),
            ("yapilandiran", "yapılandıran"), ("yapilandirdim", "yapılandırdım"),
            ("yapilandirilmis", "yapılandırılmış"),
            ("yapilandirilmistir", "yapılandırılmıştır"),
            ("yapilandirin", "yapılandırın"),
            ("yapilandirir", "yapılandırır"), ("yapilandirirken", "yapılandırırken"),
            ("yapilandirirsan", "yapılandırırsan"),
            ("yapilandirmasinda", "yapılandırmasında"),
            ("yapilandrilabilir", "yapılandırılabilir"),
        ]),
        ("yapilanmasinda", "yapılanmasında", []),
        ("yaptigi", "yaptığı", [
            ("yaptiginda", "yaptığında"), ("yaptigini", "yaptığını"),
            ("yaptiginin", "yaptığının"), ("yaptiginiz", "yaptığınız"),
            ("yaptiginizi", "yaptığınızı"), ("yaptiginizin", "yaptığınızın"),
        ]),
        ("yaratici", "yaratıcı", [("yaraticilik", "yaratıcılık")]),
        ("yardim", "yardım", [
            ("yardimci", "yardımcı"), ("yardimcidir", "yardımcıdır"),
            ("yardiminiza", "yardımınıza"),
        ]),
        ("yayinla", "yayınla", [
            ("yayinlama", "yayınlama"), ("yayinlamak", "yayınlamak"),
            ("yayinlanan", "yayınlanan"), ("yayinladi", "yayınladı"),
            ("yayinlandiktan", "yayınlandıktan"), ("yayinlanmadan", "yayınlanmadan"),
            ("yayinlayacagiz", "yayınlayacağız"), ("yayinlayalim", "yayınlayalım"),
        ]),
        ("yayin", "yayın", []),
        ("yazilim", "yazılım", [
            ("yazilimi", "yazılımı"), ("yazilimci", "yazılımcı"),
            ("yazilimcilari", "yazılımcıları"),
            ("yazilimda", "yazılımda"), ("yazilimin", "yazılımın"),
            ("yazilimla", "yazılımla"), ("yazilima", "yazılıma"),
        ]),
        ("yil", "yıl", [
            ("yillik", "yıllık"), ("yildir", "yıldır"), ("yilda", "yılda"),
            ("yilinda", "yılında"), ("yili", "yılı"),
        ]),
        ("yonetim", "yönetim", [
            ("yonetimi", "yönetimi"), ("yonetimini", "yönetimini"),
            ("yonetiminde", "yönetiminde"),
        ]),
        ("yonetici", "yönetici", [
            ("yoneticisi", "yöneticisi"), ("yoneticileri", "yöneticileri"),
        ]),
        ("yonetmek", "yönetmek", []),
        ("yontem", "yöntem", [("yontemleri", "yöntemleri")]),
        ("yonlendirme", "yönlendirme", []),
        ("yon", "yön", [("yonu", "yönü")]),
        ("yukari", "yukarı", [("yukarida", "yukarıda"), ("yukaridaki", "yukarıdaki")]),
        ("yukleme", "yükleme", [
            ("yuklemek", "yüklemek"), ("yuklendiginde", "yüklendiğinde"),
            ("yuklenmesi", "yüklenmesi"), ("yuklenmis", "yüklenmiş"),
            ("yuklenme", "yüklenme"), ("yuklenen", "yüklenen"),
            ("yuklendi", "yüklendi"), ("yuklenebilecek", "yüklenebilecek"),
            ("yuklemelrini", "yüklemelerini"),
        ]),
        ("yukle", "yükle", [
            ("yukleyen", "yükleyen"), ("yukleyin", "yükleyin"),
        ]),
        ("yukler", "yükler", []),
        ("yuk", "yük", [("yuku", "yükü")]),
        ("yuksek", "yüksek", [
            ("yukseklik", "yükseklik"), ("yuksekligi", "yüksekliği"),
        ]),
        ("zayif", "zayıf", [
            ("zayiflik", "zayıflık"), ("zayiftir", "zayıftır"),
        ]),
        ("dayaniklilik", "dayanıklılık", [
            ("dayanikliligi", "dayanıklılığı"),
            ("dayanikiliginda", "dayanıklılığında"),
            ("dayanimliligi", "dayanımlılığı"),
        ]),
        ("dayanikli", "dayanıklı", []),
        ("olcekleme", "ölçekleme", [("olceklemek", "ölçeklemek")]),
        ("gosterdigi", "gösterdiği", []),
        ("ogrenecegini", "öğreneceğini", []),
        ("adlandirilmis", "adlandırılmış", []),
        ("yapilacak", "yapılacak", []),
        ("yonetime", "yönetime", []),
        ("sonuca", "sonuca", []),  # already correct
        ("sonucu", "sonucu", []),  # already correct
        ("sonucun", "sonucun", []),  # already correct
        ("sonucunu", "sonucunu", []),  # already correct

        # ─── Standalone / misc ───
        ("arayuz", "arayüz", [
            ("arayuzu", "arayüzü"), ("arayuzun", "arayüzün"),
            ("arayuzler", "arayüzler"), ("arayuzleri", "arayüzleri"),
            ("arayuzlere", "arayüzlere"),
        ]),
        ("arguman", "argüman", [
            ("argumanlari", "argümanları"), ("argumanlar", "argümanlar"),
            ("argumani", "argümanı"),
        ]),
        ("acik", "açık", [("aciga", "açığa")]),
        ("acilir", "açılır", [("acilmasi", "açılması")]),
        ("aciklama", "açıklama", [
            ("aciklamak", "açıklamak"), ("aciklamalari", "açıklamaları"),
            ("aciklamasi", "açıklaması"), ("aciklamasinda", "açıklamasında"),
            ("aciklamasini", "açıklamasını"), ("aciklamaz", "açıklamaz"),
            ("aciklamalar", "açıklamalar"), ("aciklamasinin", "açıklamasının"),
            ("aciklamaya", "açıklamaya"),
        ]),
        ("acikca", "açıkça", []),
        ("aciklayici", "açıklayıcı", []),
        ("acis", "açış", [("acisi", "açısı"), ("acisindan", "açısından")]),
        ("altyapi", "altyapı", [("altyapisi", "altyapısı"), ("altyapisini", "altyapısını")]),
        ("alfasayisal", "alfasayısal", []),
        ("anlatim", "anlatım", [("anlatiminiz", "anlatımınız")]),
        ("anlatiyor", "anlatıyor", [("anlatiyorsun", "anlatıyorsun")]),
        ("anlatir", "anlatır", [
            ("anlatirken", "anlatırken"), ("anlatirdin", "anlatırdın"),
        ]),
        ("anlatirim", "anlatırım", []),
        ("anlatin", "anlatın", []),
        ("anlatilir", "anlatılır", []),
        ("anlatilmis", "anlatılmış", []),
        ("anlasilir", "anlaşılır", []),
        ("anlasma", "anlaşma", [("anlasmasi", "anlaşması")]),
        ("arac", "araç", [
            ("araci", "aracı"), ("araclari", "araçları"),
            ("araclarini", "araçlarını"), ("araclarina", "araçlarına"),
            ("araclara", "araçlara"), ("araclarla", "araçlarla"),
            ("araciligiyla", "aracılığıyla"), ("aractir", "araçtır"),
            ("araclariinda", "araçlarında"),
        ]),
        ("arastirma", "araştırma", [
            ("arastirmak", "araştırmak"), ("arastirmasi", "araştırması"),
            ("arastirildi", "araştırıldı"), ("arastiriliyor", "araştırılıyor"),
            ("arastirip", "araştırıp"), ("arastirirken", "araştırırken"),
            ("arastirmali", "araştırmalı"), ("arastirmama", "araştırmama"),
            ("arastirmanin", "araştırmanın"), ("arastirmasinda", "araştırmasında"),
            ("arastirmaz", "araştırmaz"),
        ]),
        ("asama", "aşama", [
            ("asamasi", "aşaması"), ("asamalari", "aşamaları"),
            ("asamada", "aşamada"),
        ]),
        ("asiri", "aşırı", []),
        ("ayni", "aynı", []),
        ("arasira", "arasıra", []),
        ("aldigi", "aldığı", [
            ("aldigin", "aldığın"), ("aldiginda", "aldığında"),
            ("aldiginiz", "aldığınız"),
        ]),
        ("aldim", "aldım", []),
        ("bagli", "bağlı", [("bagliydi", "bağlıydı"), ("baglidir", "bağlıdır")]),
        ("baglanti", "bağlantı", [
            ("baglantisi", "bağlantısı"), ("baglantisini", "bağlantısını"),
            ("baglantilari", "bağlantıları"), ("baglantilar", "bağlantılar"),
        ]),
        ("baglam", "bağlam", [("baglami", "bağlamı"), ("baglaminda", "bağlamında")]),
        ("bagimli", "bağımlı", [
            ("bagimliligi", "bağımlılığı"), ("bagimlilik", "bağımlılık"),
            ("bagimliliklari", "bağımlılıkları"),
            ("bagimliliklarini", "bağımlılıklarını"),
            ("bagimliliklar", "bağımlılıklar"),
        ]),
        ("bagimsiz", "bağımsız", []),
        ("birak", "bırak", [
            ("birakamadigi", "bırakamadığı"), ("birakan", "bırakan"),
            ("birakildi", "bırakıldı"), ("birakilmis", "bırakılmış"),
            ("birakir", "bırakır"), ("birakma", "bırakma"),
            ("birakmadi", "bırakmadı"), ("birakmak", "bırakmak"),
            ("birakmayin", "bırakmayın"),
        ]),
        ("bugun", "bugün", [("bugunku", "bugünkü")]),
        ("duyarim", "duyarım", []),
        ("edis", "ediş", []),
        ("endiseniz", "endişeniz", []),
        ("faydali", "faydalı", []),
        ("faydalari", "faydaları", []),
        ("hatasi", "hatası", [
            ("hatasinda", "hatasında"), ("hatasini", "hatasını"),
        ]),
        ("istege", "isteğe", []),
        ("istegi", "isteği", []),
        ("kacabilecek", "kaçabilecek", []),
        ("kaldik", "kaldık", []),
        ("kaldim", "kaldım", []),
        ("katki", "katkı", [
            ("katkida", "katkıda"), ("katkisi", "katkısı"),
        ]),
        ("kisayollar", "kısayollar", []),
        ("noktasina", "noktasına", []),
        ("noktasinda", "noktasında", []),
        ("noktasindasin", "noktasındasın", []),
        ("olabilecegi", "olabileceği", [("olabilecegini", "olabileceğini")]),
        ("otomatiklestirme", "otomatikleştirme", [
            ("otomatiklestirin", "otomatikleştirin"),
            ("otomatiklestirmek", "otomatikleştirmek"),
        ]),
        ("takipci", "takipçi", [("takipcisinde", "takipçisinde")]),
        ("tamamlandi", "tamamlandı", [("tamamlandiginda", "tamamlandığında")]),
        ("tamamlanmasi", "tamamlanması", []),
        ("tamamlanmis", "tamamlanmış", []),
        ("veritabani", "veritabanı", [
            ("veritabaninda", "veritabanında"), ("veritabanini", "veritabanını"),
            ("veritabaninin", "veritabanının"), ("veritabanlari", "veritabanları"),
        ]),
        ("kullanici", "kullanıcı", [
            ("kullanicinin", "kullanıcının"), ("kullaniciyi", "kullanıcıyı"),
            ("kullaniciya", "kullanıcıya"), ("kullanicilar", "kullanıcılar"),
            ("kullanicilari", "kullanıcıları"), ("kullanicilarini", "kullanıcılarını"),
            ("kullanicilarin", "kullanıcıların"),
        ]),
        ("kullanim", "kullanım", [("kullanimi", "kullanımı"), ("kullanimin", "kullanımın")]),
        ("kullanilir", "kullanılır", []),
        ("kullanilan", "kullanılan", []),
        ("kullanilabilir", "kullanılabilir", []),
        ("kullanilabilecek", "kullanılabilecek", [
            ("kullanilabilecegi", "kullanılabileceği"),
        ]),
        ("kullanilmasi", "kullanılması", [("kullanilmasini", "kullanılmasını")]),
        ("kullanilmaz", "kullanılmaz", []),
        ("bocek", "böcek", []),
        ("yolculugum", "yolculuğum", []),
        ("yolculuklari", "yolculukları", []),
        ("alani", "alanı", []),
        ("alaninda", "alanında", [("alanindaki", "alanındaki")]),
        ("katilabilecek", "katılabilecek", []),
        ("disaridan", "dışarıdan", []),
        ("disari", "dışarı", [("disaridan", "dışarıdan")]),
        ("disarlama", "dışarlama", []),
        ("disa", "dışa", []),
        ("disinda", "dışında", [("disindaki", "dışındaki")]),
        ("disi", "dışı", []),

        # Stand-alone short words (whole word match only)
        ("ise", "işe", []),
        ("isin", "işin", []),
        ("isi", "işi", []),
        ("iste", "işte", []),
        ("dis", "dış", []),
        ("dun", "dün", []),
    ]

    for ascii_root, turkish_root, extras in roots:
        # Add root itself
        if ascii_root != turkish_root:
            corrections[ascii_root] = turkish_root
        # Add extra forms
        for ascii_form, turkish_form in extras:
            if ascii_form != turkish_form:
                corrections[ascii_form] = turkish_form

    return corrections


CORRECTIONS = _expand_roots()

# Pre-compile regex for fast whole-word matching
# Sort keys by length descending for greedy matching
_sorted_keys = sorted(CORRECTIONS.keys(), key=len, reverse=True)
_pattern = re.compile(
    r'\b(' + '|'.join(re.escape(k) for k in _sorted_keys) + r')\b',
    re.IGNORECASE
)


def fix_turkish_text(text):
    """Replace ASCII Turkish words with properly encoded versions."""
    if not isinstance(text, str):
        return text

    def replace_match(match):
        word = match.group(0)
        lower = word.lower()

        if lower in CORRECTIONS:
            corrected = CORRECTIONS[lower]
            if corrected == lower:
                return word

            # Preserve capitalization
            if word[0].isupper() and len(word) > 1 and word[1:].islower():
                return corrected[0].upper() + corrected[1:]
            elif word.isupper():
                return corrected.upper()
            else:
                return corrected
        return word

    return _pattern.sub(replace_match, text)


def fix_json_recursive(obj):
    """Recursively fix Turkish characters in all string values."""
    if isinstance(obj, str):
        return fix_turkish_text(obj)
    elif isinstance(obj, list):
        return [fix_json_recursive(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: fix_json_recursive(v) for k, v in obj.items()}
    else:
        return obj


def process_file(filepath):
    """Process a single JSON file."""
    print(f"Processing: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fixed_data = fix_json_recursive(data)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(fixed_data, f, ensure_ascii=False, indent=2)

    print(f"  Done: {filepath}")


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    files = [
        os.path.join(base_dir, "content", "english", "vocabulary.json"),
        os.path.join(base_dir, "content", "english", "sentence_patterns.json"),
    ]

    career_dir = os.path.join(base_dir, "content", "career")
    if os.path.isdir(career_dir):
        for fname in sorted(os.listdir(career_dir)):
            if fname.endswith(".json"):
                files.append(os.path.join(career_dir, fname))

    for filepath in files:
        if os.path.exists(filepath):
            process_file(filepath)
        else:
            print(f"  WARNING: File not found: {filepath}")

    print("\nAll files processed successfully!")


if __name__ == "__main__":
    main()

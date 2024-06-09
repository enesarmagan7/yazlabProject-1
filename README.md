I.  OZET

 Bu projede Google Akademik gibi akademik arama motor
ları üzerinden web scraping (web kazıma) yöntemiyle aratılan
 akademik yayınlara ait bilgilerin kaydedildigi bir veritabanıyla
 birlikte bu bilgilerin webden aratılması, görüntülenmesi
 ve istenilen ¨ ozelliklere göre sorguların yapılmasına imkan
 sağlayacak bir web arayüzü geliştirmek amaçlanmaktadır.

 Amaç
Proje sayesinde web scraping ile bir web sayfasından bilgiye erişim sağlama; MongoDB veritabanı ile Elasticsearch sorgu yapılarını kullanma ve web kodlama becerilerinin geliştirilmesi amaçlanmaktadır.

Programlama Dili
Proje veritabanı ve sorguları için MongoDB ile Elasticsearch yapısı kullanılmalıdır. Web arayüzü, istenilen bir web programlama dili kullanılarak oluşturulacaktır.

Proje Kısımları
Proje aşağıda detayları verilen 3 ana kısımdan oluşmaktadır:

1. Web Scraping
En az bir akademik arama motorundan web scraping kullanılarak kullanıcının gireceği anahtar kelimelere göre listelenmiş en az ilk 10 akademik yayının bilgileri, kendi oluşturacağınız web sayfasında görüntülenmelidir. Kullanıcının arama yapmak için kullanacağı anahtar kelimeler oluşturacağınız kendi web sayfanızdaki bir text alanı üzerinden girilecektir.
Web scraping işlemi için siteye ait HTML bilgiler kullanılarak veya siteye request isteği yapılarak istenen veriye erişilmelidir. (Erişilecek siteye yönelik hazır web API'ler kullanılmamalıdır.)
İstenen yayına ilişkin bilgiler doğrudan akademik arama motorunun sayfasından çekilebileceği gibi arama motoru sayfasındaki link üzerinden yönlendirilecek diğer bir web sayfasından da elde edilebilir. (İkincil sitelere geçiş yapılarak web scraping yapılması durumunda artı puan verilecektir.)
İstenen her yayın için PDF dosyası mutlaka indirilmelidir. Daha sonra tercihe göre yayın bilgileri ya web sayfası üzerinden ya da indirilmiş PDF dosyasının içeriğinden elde edilebilir.
2. Veritabanı
Web scraping ile elde edilen veriler MongoDB kullanılarak veritabanına kaydedilecektir.
Veritabanında tutulması gereken bilgiler şunlardır:
Yayın id,
Yayın adı,
Yazarların isimleri,
Yayın türü (araştırma makalesi, derleme, konferans, kitap vb.),
Yayımlanma tarihi,
Yayıncı adı (yayının yayımlandığı konferans ismi; dergi veya kitap yayınevi),
Anahtar kelimeler (Arama motorunda aratılan),
Anahtar kelimeler (Makaleye ait),
Özet,
Referanslar,
Alıntı sayısı,
DOI numarası (Eğer varsa),
URL adresi
3. Web Sayfası
Erişilen yayınların bilgilerinin kullanıcıya gösterilmesi için bir web sayfası oluşturmanız beklenmektedir.
Web sayfasında aratılacak yayınlar için bir text alanı oluşturulmalı ve bu text alanına girilecek anahtar kelimeler üzerinden ilgili arama motorunun yayınları aratıp bilgilerini web sayfasına getirmesi sağlanmalıdır.
Web sayfası ilk açıldığında veritabanında bulunan tüm kayıtlar sayfaya getirilmelidir.
Listeleme işleminde yayınların isimleri sırasına uygun biçimde listelenmelidir. Listelenen bir makale ismine tıklandığında o makaleye özgü bilgiler ayrı bir sayfada gösterilmelidir.
Web sayfasından herhangi bir çalışmaya yönelik dinamik arama işlemi yapılabilmelidir. Ayrıca arama sırasında yazım yanlışı olması durumunda sistem düzeltilmiş öneride bulunmalıdır. Örnek: "deep learrning" -- yazımı düzeltilmiş sonuçları görüyorsunuz: "deep learning" şeklinde olmalıdır.
Web sayfasında dinamik filtreleme işlemi de ayrıca yer almalıdır. Filtreleme işlemi veritabanında yer alan yayının tüm özellikleri için hem ayrı ayrı hem de birlikte uygulanabilir olmalıdır.
Web sayfasında en son veya en önce yayımlanma tarihine göre sıralama yapılabilmeli ayrıca yine atıf sayısına göre de en az veya en çok olacak şekilde sıralama yapılabilmelidir.

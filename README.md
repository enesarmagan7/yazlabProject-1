# Proje Özeti

Bu proje, Google Akademik gibi akademik arama motorları üzerinden web scraping yöntemiyle aratılan akademik yayınlara ait bilgilerin kaydedildiği bir veritabanıyla birlikte, bu bilgilerin webden aratılması, görüntülenmesi ve sorguların yapılmasını sağlayacak bir web arayüzü geliştirmeyi amaçlamaktadır.

## Amaç

- Web scraping ile bir web sayfasından bilgiye erişim sağlama
- MongoDB ve Elasticsearch kullanarak veritabanı ve sorgu yapılarını öğrenme
- Web kodlama becerilerinin geliştirilmesi

## Programlama Dili

- Veritabanı ve sorgular: MongoDB ve Elasticsearch
- Web arayüzü: Tercih edilen bir web programlama dili

## Proje Bileşenleri

### 1. Web Scraping

- Akademik arama motorlarından web scraping ile kullanıcı tarafından girilen anahtar kelimelerle ilk 10 yayının bilgilerini çekme
- HTML bilgileri veya request kullanarak veri erişimi (hazır API kullanılmamalı)
- Yayın bilgilerini ve PDF dosyalarını indirme

### 2. Veritabanı

- Web scraping ile elde edilen verilerin MongoDB'de saklanması
- Saklanacak bilgiler: Yayın id, ad, yazarlar, tür, tarih, yayıncı, anahtar kelimeler, özet, referanslar, alıntı sayısı, DOI, URL

### 3. Web Arayüzü

- Yayın bilgilerini kullanıcıya gösteren bir web sayfası oluşturma
- Anahtar kelimelerle arama yapma ve sonuçları listeleme
- Dinamik arama ve filtreleme özellikleri
- Yayınların tarih ve alıntı sayısına göre sıralanması

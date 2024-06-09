from difflib import get_close_matches

from bson import ObjectId
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['scholar']
collection = db['yayinlar']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        anahtar_kelime = request.form['anahtar_kelime']
        google_scholar_scrape(anahtar_kelime)
    yayinlar = collection.find()
    return render_template('index.html', yayinlar=yayinlar)
@app.route('/arama/<anahtar_kelime>')
def arama(anahtar_kelime):
    yayinlar = collection.find({'baslik': {'$regex': anahtar_kelime, '$options': 'i'}}).sort([('tarih', -1)])
    return render_template('index.html', yayinlar=yayinlar, anahtar_kelime=anahtar_kelime)

@app.route('/yayin/<yayin_id>')
def yayin_detay(yayin_id):
    yayin = collection.find_one({'_id': ObjectId(yayin_id)})  # ObjectId ile belirtilmesi gerekiyor
    return render_template('yayin_detay.html', yayin=yayin)

@app.route('/oneri/<anahtar_kelime>')
def oneri(anahtar_kelime):
    yakın_kelime = get_close_matches(anahtar_kelime, collection.distinct('baslik'))
    return jsonify(yakın_kelime)


@app.route('/filtrele', methods=['POST'])
def filtrele():
    if request.method == 'POST':
        filtre_yil = request.form['yil']
        filtre_tur = request.form['tur']

        # Yıla ve türe göre filtreleme
        if filtre_yil != 'Tümü' and filtre_tur:
            yayinlar = collection.find({'yayin_tarihi': filtre_yil, 'yayin_turu': filtre_tur})
        # Yıla göre filtreleme
        elif filtre_yil != 'Tümü':
            yayinlar = collection.find({'yayin_tarihi': filtre_yil})
        # Türe göre filtreleme
        elif filtre_tur:
            yayinlar = collection.find({'yayin_turu': filtre_tur})
        else:
            yayinlar = collection.find()

        return render_template('index.html', yayinlar=yayinlar, filtre_yil=filtre_yil, filtre_tur=filtre_tur)



def temizle_html_metni(html_metni):
    soup = BeautifulSoup(html_metni, 'html.parser')
    temiz_metin = soup.get_text(strip=True)
    return temiz_metin


def get_article_details(article_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(article_url, headers=headers)

    if response.status_code != 200:
        print("Hata! İstek başarısız oldu.")
        return None

    article_content = response.content
    article_soup = BeautifulSoup(article_content, 'html.parser')

    pdf_url_element = article_soup.find('a', class_='kt-nav__link')
    pdf_urls = pdf_url_element['href'] if pdf_url_element else None
    pdf_url = 'https://dergipark.org.tr'+pdf_urls

    # Özet
    summary_element = article_soup.find('div', class_='article-abstract')
    summary = summary_element.get_text().strip() if summary_element else None

    # Kaynaklar
    references_element = article_soup.find('div', class_='article-citations')
    references = references_element.get_text().strip() if references_element else None

    authors_element = article_soup.find('p', class_='article-authors')
    if authors_element:
        authors = [author.get_text().strip() for author in authors_element.find_all('a', class_='is-user')]




    # Yayın yılı
    publication_year_element = article_soup.find('span', class_='article-subtitle')
    publication_year = publication_year_element.find_all('a')[0].text.strip() if publication_year_element else None

    # Anahtar kelimeler
    keywords_element = article_soup.find('div', class_='article-keywords')
    keywords = [a.text.strip() for a in keywords_element.find_all('a')] if keywords_element else None


    return {
        'ozet': summary,
        'kaynaklar': references,
        'yayin_yili': publication_year,
        'anahtar_kelimeler': keywords,
        'yazar': authors,
        'pdf_url':pdf_url

    }


def google_scholar_scrape(anahtar_kelime):
    collection.delete_many({})  # Veritabanını sıfırla
    url = f"https://dergipark.org.tr/tr/search?q={anahtar_kelime}&section=articles"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = [] # Yayınları tutmak için boş bir liste oluşturalım

    article_cards = soup.find_all('div', class_='card-body')

    # Her bir makale kartı için işlemleri yap
    for card in article_cards:
        article = {}

        # Yayın ID'sini al
        article['yayin_id'] = card.get('data-id')


        # Başlık
        title_element = card.find('h5', class_='card-title')
        if title_element:
            article['baslik'] = title_element.a.get_text().strip()


        # Yazarlar
        authors_element = card.find('span', title='Sorumlu Yazar')
        if authors_element:
            authors = [author.strip() for author in authors_element.get_text().split(',')]
            article['yazarlar'] = authors

        # Yayın Türü
        article_type_element = card.find('span', class_='badge badge-secondary')
        if article_type_element:
            article['yayin_turu'] = article_type_element.get_text().strip()

        # Yayın Tarihi
        publication_year = re.search(r'\(\d{4}\)', card.get_text())
        if publication_year:
            article['yayin_tarihi'] = publication_year.group()[1:-1]  # Parantezleri kaldırarak sadece yılı al

        # Yayıncı Adı
        journal_element = card.find('a', class_='fw-500')
        if journal_element:
            article['yayinci_adi'] = journal_element.get_text().strip()

        # Anahtar Kelimeler (Arama Motorunda Aratılan)
        search_keywords_element = card.find('small', class_='article-meta').find_all('a', href=True)
        if search_keywords_element:
            search_keywords = [keyword.get_text().strip() for keyword in search_keywords_element]
            article['arama_motoru_anahtar_kelimeleri'] = search_keywords

        # Anahtar Kelimeler (Makaleye Ait)
        article_keywords_element = card.find('div', class_='article-text-block kt-margin-l-0 kt-margin-t-20 matches')
        if article_keywords_element:
            article_keywords = [keyword.strip() for keyword in
                                article_keywords_element.find('span', class_='badge').get_text().split(',')]
            article['makale_anahtar_kelimeleri'] = article_keywords

        # Özet
        abstract_element = card.find('div', class_='kt-list kt-list--badge matches')
        if abstract_element:
            abstracts = [abstract.get_text().strip() for abstract in
                         abstract_element.find_all('span', class_='kt-list__text')]
            article['ozet'] = ' '.join(abstracts)

        # Referanslar (Henüz bulunamadı)
        article['referanslar'] = None

        # Alıntı Sayısı (Henüz bulunamadı)
        article['alinti_sayisi'] = None

        # DOI Numarası
        doi_element = card.find('a', href=re.compile("doi"))
        if doi_element:
            article['doi'] = doi_element.get('href').split('doi=')[-1]

        # URL Adresi
        url_element = card.find('a', href=True)

        if url_element:
            article['url_adresi'] = url_element.get('href')

        article_details = get_article_details(article['url_adresi'])

        article.update(article_details)

        articles.append(article)


    # Verileri MongoDB'ye kaydedin
    for yayin in articles:
        collection.insert_one(yayin)

if __name__ == '__main__':
    app.run(debug=True)

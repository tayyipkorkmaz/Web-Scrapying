# Web-Scrapying
"www.kitapyurdu.com" ve "www.kitapsepeti.com" web sitesini taramak ve farklı kategorilerdeki kitaplar hakkında bilgi toplamak için tasarlanmıştır. Örümcek, Python dilinde yazılmış olup web kazıma işlemleri için Scrapy framework kullanmaktadır.

# Özellikler

  - Kategori sayfasını kazıyarak kitap bilgilerini, yazar, yayınevi ve fiyat gibi veriler toplar.
  - Sayfalama işlemini yöneterek her kategorideki birden çok sayfayı tarar.
  - Scrapy'nin XPath ve CSS seçicilerini kullanarak HTML yanıtından veri çıkarır.
  - Kazıma verilerini işlemek için özel ayarlar ve veri akışı (pipeline) kullanır.
  - Kazıma verilerini farklı collections ile MongoDb' de saklar

# Item Pipelines

Bu Scrapy projelerinde, kazıma işlemi sonucunda elde edilen verileri depolamak için MongoDB'ye kaydeden iki adet öğe (item) pipeline tanımlanmıştır.

KitapyurduPipeline ve KitapsepetiPipeline

Bu pipeline, "www.kitapyurdu.com" ve "www.kitapsepeti.com" web sitelerinde kazılan verileri MongoDB veritabanına kaydetmek için kullanılır.

  - `mongo_uri`: MongoDB bağlantı URI'si.
  - `mongo_db`: MongoDB veritabanı adı.
  - `collection_name`: Kaydedilecek verilerin saklanacağı koleksiyon adı.
    

Database Örnek Kod Çıktısı:
```
 "category_title": "Akademik",
        "yeni_cikanlar": [
            {
                "book_name": "Fransa’da Yerel Yönetimler Ve Yerelleşme Reformları (Fransız İhtilalinden 2020’lere)",
                "book_publisher": "SON ÇAĞ YAYINLARI-AKADEMİK",
                "book_author": "  Turgut Atasoy",
                "book_price": 190.75
            },
```

MongoDB Çıktısı:

![Screenshot from 2023-07-07 13-24-36](https://github.com/tayyipkorkmaz/Web-Scrapying/assets/58427584/3ae2ceae-91f0-48ad-9dc3-140bcdd7ccaf)



## Quickstart

Repoyu klonlayın ve içine girin
```shell
git clone https://github.com/tayyipkorkmaz/Web-Scrapying.git
cd Web-Scrapying/smartmaple
```

Poetry'yi indirin ve bağımlılıkları indirin
```shell
python -m pip install poetry
poetry install
poetry shell
```
Spiderleri başlatın
```shell
poetry run python main.py
```

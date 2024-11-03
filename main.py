import requests
import time


def check_url(url):
    """
    URL'nin erişilebilir olup olmadığını kontrol eder.
    """
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


def filter_valid_urls(m3u_file_path, output_file_path, batch_size=5):
    """
    M3U dosyasındaki geçerli URL'leri filtreler ve bunları yeni bir M3U dosyasına kaydeder.
    """
    print("M3U dosyası okunuyor...")
    # M3U dosyasını oku
    with open(m3u_file_path, 'r', encoding='utf-8') as file:
        m3u_content = file.readlines()

    # URL'leri ayıkla
    urls = [line.strip() for line in m3u_content if line.strip().startswith("http")]
    valid_urls = []
    print(f"{len(urls)} adet URL bulundu. Kontrol ediliyor...")

    # URL'leri küçük gruplar halinde kontrol et
    for i in range(0, len(urls), batch_size):
        batch = urls[i:i + batch_size]
        print(f"{i + 1}/{len(urls)}. URL grubunu kontrol ediyor...")

        for url in batch:
            if check_url(url):
                print(f"Geçerli URL bulundu: {url}")
                valid_urls.append(url)
            else:
                print(f"Geçersiz URL: {url}")

        # Fazla istekten kaçınmak için bekleme süresi
        time.sleep(1)

    # Geçerli URL'leri yeni bir M3U dosyasına kaydet
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for line in m3u_content:
            if line.strip() in valid_urls or not line.strip().startswith("http"):
                output_file.write(line)

    print(f"Geçerli URL'ler '{output_file_path}' dosyasına kaydedildi.")
    print("İşlem tamamlandı.")


# Kullanım
m3u_file_path = "dosyanız.m3u"  # Orijinal M3U dosya yolu
output_file_path = "filtered_test.m3u"  # Geçerli URL'lerin kaydedileceği dosya

filter_valid_urls(m3u_file_path, output_file_path)

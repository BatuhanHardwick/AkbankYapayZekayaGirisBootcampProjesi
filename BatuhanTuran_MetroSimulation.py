# Gerekli modüllerin import edilmesi
from collections import defaultdict, deque
import heapq
from itertools import count
from typing import Dict, List, Tuple, Optional, Set


class Istasyon:
    """
    Metro istasyonunu temsilen oluşturduğum sınıf.
    Her istasyonun bir kimliği (id), adı (ad) ve hattı (hat) var.
    Ayrıca, bağlantılı (komşu) istasyonlar ve oradaki seyahat sürelerini bulunduruyor.
    """

    def __init__(self, id_: str, ad: str, hat: str):
        # Istasyon kimliğinin geçerliliğini kontrol.
        if not id_ or not isinstance(id_, str):
            raise ValueError("Geçersiz istasyon ID'si")
        # Istasyon adının geçerliliğini kontrol
        if not ad or not isinstance(ad, str):
            raise ValueError("Geçersiz istasyon adı")
        # Hat bilgisinin geçerliliğini kontrol
        if not hat or not isinstance(hat, str):
            raise ValueError("Geçersiz hat bilgisi")

        self.id = id_
        self.ad = ad
        self.hat = hat
        # Komşu istasyonları saklayan liste oluşturuyorum.
        self.komsular: List[Tuple[Istasyon, int]] = []

    def komsu_ekle(self, istasyon: "Istasyon", sure: int) -> None:
        """
        Belirtilen istasyonu belirtilen süre ile komşu olarak ekliyor
        ve süre değerinin geçerli bir değer olmadığını kontrol ediyorum
        """
        if not isinstance(sure, int) or sure < 0:
            raise ValueError("Süre pozitif tam sayı olmalıdır")
        self.komsular.append((istasyon, sure))

    def __repr__(self) -> str:
        # Istasyon nesnesinin okunabilir gösterimi
        return f"<Istasyon: {self.ad} ({self.hat})>"


class MetroAgi:

    def __init__(self):
        # Tüm istasyonlar kimlik ile istasyondan türetilen bir obje olarak tutuluyor.
        self.istasyonlar: Dict[str, Istasyon] = {}
        # Hat isimlerine göre istasyonları sakla
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)
        # sayaç Dijkstra ve A* algoritmasında kıyaslamak için kullanıyorum.
        self._sayac = count()

    def istasyon_ekle(self, id_: str, ad: str, hat: str) -> None:
        """
        Metro ağına yeni bir istasyon ekler.
        Verilen id ad ve hat bilgilerine göre yeni Istasyon nesnesi oluşturulur.
        """
        if id_ in self.istasyonlar:
            raise ValueError(f"{id_} ID'li istasyon zaten mevcut")

        istasyon = Istasyon(id_, ad, hat)
        # Istasyon sözlüğüne ekleme yapılır
        self.istasyonlar[id_] = istasyon
        # İlgili hatta ait istasyon listesine ekleme yapılır
        self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        """
        İki istasyon arasında çift yönlü bağlantı ekler.
        Verilen süre her iki istasyonada aynı şekild eklenir.
        """
        try:
            istasyon1 = self.istasyonlar[istasyon1_id]
            istasyon2 = self.istasyonlar[istasyon2_id]
        except KeyError as e:
            raise ValueError(f"İstasyon bulunamadı: {e}") from None

        # Süre negatif girilmemesi için bir kontrol sağlıyorum.
        if sure < 0:
            raise ValueError("Süre negatif olamaz")

        # Aynı bağlantının daha önceden eklenip eklenmediği kontrolü için
        for komsu, mevcut_sure in istasyon1.komsular:
            if komsu.id == istasyon2_id:
                if mevcut_sure != sure:
                    raise ValueError(f"Mevcut bağlantı {mevcut_sure} dakika ile zaten var")
                return

        # Her iki istasyonun birbirlerine komşuluk durumu eklenir.
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)

    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        """
        BFS (genişlik öncelikli arama) algoritmasını kullanarak en az aktarmalı rota bulunur.
        Aktarma sayısı, geçilen istasyon sayısından 1 eksiktir (başlangıç değeri hariç).
        """
        baslangic = self.istasyonlar.get(baslangic_id)
        hedef = self.istasyonlar.get(hedef_id)
        if not baslangic or not hedef:
            return None

        # BFS : Her eleman (şuanki istasyon, o ana kadar izlenen yol) şeklinde saklanır.
        kuyruk = deque([(baslangic, [baslangic])])
        # Ziyaret edilmiş istasyonlar
        ziyaret: Set[Istasyon] = set()

        while kuyruk:
            current, path = kuyruk.popleft()
            # Hedefe ulaşıldıysa mevcut yolu döndür.
            if current == hedef:
                return path
            if current in ziyaret:
                continue
            # Şu anki istasyon ziyaret edilmiştir.
            ziyaret.add(current)

            # Her komşu için yolu genişleterek kuyruğa eklenir.
            for komsu, _ in current.komsular:
                if komsu not in ziyaret:
                    kuyruk.append((komsu, path + [komsu]))
        return None

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """
        Dijkstra algoritması kullanılarak en kısa süredeki (en hızlı) rota bulunur.
        Her kenarın ağırlığı, isteğe bağlı olarak süre olarak belirlenmiştir.
        """
        baslangic = self.istasyonlar.get(baslangic_id)
        hedef = self.istasyonlar.get(hedef_id)
        if not baslangic or not hedef:
            return None

        # Min-heap: (mevcut maliyet (süre), sayaç değeri, güncel istasyon, yol)
        heap = [(0, next(self._sayac), baslangic, [baslangic])]
        # Her istasyona ulaşım için en düşük maliyet
        maliyetler = {baslangic: 0}

        while heap:
            current_maliyet, _, current, path = heapq.heappop(heap)
            # Eğer hedefe ulaşıldıysa yolu ve maliyeti döndür.
            if current == hedef:
                return (path, current_maliyet)

            # Eğer mevcut maliyet daha önceden hesaplanan maliyetten fazla ise yola devam etme.
            if current_maliyet > maliyetler.get(current, float('inf')):
                continue

            # Komşular için maliyetleri güncelle ve heap'e ekle.
            for komsu, sure in current.komsular:
                yeni_maliyet = current_maliyet + sure
                if yeni_maliyet < maliyetler.get(komsu, float('inf')):
                    maliyetler[komsu] = yeni_maliyet
                    heapq.heappush(heap, (yeni_maliyet, next(self._sayac), komsu, path + [komsu]))
        return None

    def _heuristic(self, current: Istasyon, hedef: Istasyon) -> int:
        """
        A* algoritması için basit bir tahmin fonksiyonu.
        Aynı hattaysalar tahmini maliyeti 0, farklı hat için 2 olarak düşünüyoruz.
        örnek olması amacıyla verilmiştir.
        """
        return 0 if current.hat == hedef.hat else 2

    def a_star_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """
        A* algoritması kullanılarak optimize edilmiş rotayı bulur.
        f = g + h şeklinde hesaplama yapılır.
        g: Başlangıçtan o anki istasyona kadar olan maliyet
        h: Sezgisel tahmin ile o istasyondan hedefe olan tahmini maliyet
        """
        baslangic = self.istasyonlar.get(baslangic_id)
        hedef = self.istasyonlar.get(hedef_id)
        if not baslangic or not hedef:
            return None

        # Heap elemanı: (f değeri, g değeri, sayaç, güncel istasyon, yol)
        heap = [(0, 0, next(self._sayac), baslangic, [baslangic])]
        # Başlangıçtan her istasyona ulaşım için maliyetlerin saklanması için
        maliyetler = {baslangic: 0}

        while heap:
            current_f, current_g, _, current, path = heapq.heappop(heap)
            # Hedefe ulaşıldığında, yolu ve g değeri (toplam maliyet) döndür.
            if current == hedef:
                return (path, current_g)

            if current_g > maliyetler.get(current, float('inf')):
                continue

            # Her komşu için 
            for komsu, sure in current.komsular:
                yeni_g = current_g + sure
                # Daha iyi bir yol bulmuşsak güncelle ve heap'e ekle.
                if yeni_g < maliyetler.get(komsu, float('inf')):
                    h = self._heuristic(komsu, hedef)
                    heapq.heappush(heap, (yeni_g + h, yeni_g, next(self._sayac), komsu, path + [komsu]))
                    maliyetler[komsu] = yeni_g
        return None


# Metro Ağı Kurulumu

# MetroAgi sınıfından bir nesne oluşturulur
metro = MetroAgi()

# İstasyonların tanımlanması
istasyonlar = [
    ("K1", "Kızılay", "Kırmızı Hat"),
    ("K2", "Ulus", "Kırmızı Hat"),
    ("K3", "Demetevler", "Kırmızı Hat"),
    ("K4", "OSB", "Kırmızı Hat"),
    ("M1", "AŞTİ", "Mavi Hat"),
    ("M2", "Kızılay", "Mavi Hat"),
    ("M3", "Sıhhiye", "Mavi Hat"),
    ("M4", "Gar", "Mavi Hat"),
    ("T1", "Batıkent", "Turuncu Hat"),
    ("T2", "Demetevler", "Turuncu Hat"),
    ("T3", "Gar", "Turuncu Hat"),
    ("T4", "Keçiören", "Turuncu Hat"),
]

# Her istasyon Metro ağına ekleniyor
for id_, ad, hat in istasyonlar:
    metro.istasyon_ekle(id_, ad, hat)

# Bağlantıların tanımlanması
baglantilar = [
    # Kırmızı Hat üzerindeki istasyonlar arasındaki bağlantılar
    ("K1", "K2", 4),
    ("K2", "K3", 6),
    ("K3", "K4", 8),
    # Mavi Hat üzerindeki istasyonlar arasındaki bağlantılar
    ("M1", "M2", 5),
    ("M2", "M3", 3),
    ("M3", "M4", 4),
    # Turuncu Hat üzerindeki istasyonlar arasındaki bağlantılar
    ("T1", "T2", 7),
    ("T2", "T3", 9),
    ("T3", "T4", 5),
    # Farklı hatlar arasındaki aktarma noktaları
    ("K1", "M2", 2),
    ("K3", "T2", 3),
    ("M4", "T3", 2),
]

# Tanımlı her bağlantı Metro ağına eklenir.
for baglanti in baglantilar:
    metro.baglanti_ekle(*baglanti)


# Test Senaryoları
def test_rota(baslangic: str, hedef: str):
    """
    Verilen başlangıç ve hedef istasyon ID'leri için üç farklı algoritma (BFS, Dijkstra, A*)
    kullanarak rota hesaplaması yapar ve sonuçları yazdırıyor.
    """
    print(f"\n{baslangic} -> {hedef}")

    # En az aktarmalı (BFS) rota
    rota = metro.en_az_aktarma_bul(baslangic, hedef)
    if rota:
        print(f"BFS: {' -> '.join(i.ad for i in rota)} ({len(rota) - 1} aktarma)")
    else:
        print("BFS ile rota bulunamadı")

    # En hızlı (Dijkstra) rota
    sonuc = metro.en_hizli_rota_bul(baslangic, hedef)
    if sonuc:
        rota, sure = sonuc
        print(f"Dijkstra: {' -> '.join(i.ad for i in rota)} ({sure} dk)")
    else:
        print("Dijkstra ile rota bulunamadı")

    # A* algoritması ile rota
    sonuc = metro.a_star_rota_bul(baslangic, hedef)
    if sonuc:
        rota, sure = sonuc
        print(f"A*: {' -> '.join(i.ad for i in rota)} ({sure} dk)")
    else:
        print("A* ile rota bulunamadı")

# Test senaryoları:

print("\n1. AŞTİ'den OSB'ye:")
test_rota("M1", "K4")  # AŞTİ -> OSB

print("\n2. Batıkent'ten Keçiören'e:")
test_rota("T1", "T4")  # Batıkent -> Keçiören

print("\n3. Keçiören'den AŞTİ'ye:")
test_rota("T4", "M1")  # Keçiören -> AŞTİ

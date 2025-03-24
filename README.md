# 🚇 Metro Ağı Rota Bulma Projesi  

Bu proje Akbank ve Yapay Zekaya Giriş bootcamp'i için hazırlanmıştır, Bu projede bir metro ağı üzerinde **en az aktarmalı** ve **en hızlı** rotaları hesaplamak için **BFS, Dijkstra ve A*** algoritmalarını kullanmaktadır. Python dili ile geliştirilen proje, metro istasyonları arasındaki bağlantıları modelleyerek en uygun güzergahları belirlemeyi amaçlar.  

## 🛠 Kullanılan Teknolojiler ve Kütüphaneler  

Proje Python programlama dili ile geliştirilmiştir ve aşağıdaki standart kütüphaneler kullanılmıştır:  

- **`collections.defaultdict`** → Metro hatlarını ve istasyonları saklamak için kullanıldı.  
- **`collections.deque`** → BFS algoritmasında genişlik öncelikli arama sırasında kuyruğu yönetmek için kullanıldı.  
- **`heapq`** → Dijkstra ve A* algoritmalarında en kısa süreyi belirlemek için öncelikli kuyruk olarak kullanıldı.  
- **`itertools.count`** → Algoritmaların kıyaslamalarında kullanılmak üzere sayaç görevi gördü.  
- **`typing`** → Kodun daha okunaklı olması ve tip güvenliği için kullanıldı.  

---

## 📌 Algoritmaların Çalışma Mantığı  

Bu proje, üç farklı algoritmayı kullanarak en iyi metro güzergahını belirler:  

### **1️⃣ BFS (Genişlik Öncelikli Arama) - En Az Aktarma**  
**Çalışma Mantığı:**  
- BFS, kuyruk (queue) veri yapısını kullanarak metro hattında **istasyon sayısını minimize eden** rotayı bulur.  
- İlk olarak başlangıç istasyonu kuyruğa eklenir.  
- Her adımda mevcut istasyonun komşuları kontrol edilir.  
- En az aktarma ile hedefe ulaşan ilk yol bulunduğunda işlem tamamlanır.  

**Neden Kullanıldı?**  
- Aktarma sayısını minimize etmek için idealdir.  
- Ancak, sadece istasyon sayısını dikkate alır, seyahat süresi gözetilmez.  

---

### **2️⃣ Dijkstra Algoritması - En Hızlı Rota**  
**Çalışma Mantığı:**  
- Dijkstra algoritması **öncelikli kuyruk (heapq)** kullanarak her istasyon için en düşük maliyetli (en kısa sürede) rotayı hesaplar.  
- Başlangıç istasyonundan başlar ve her adımda en düşük ağırlığa (süreye) sahip olan istasyonu seçer.  
- Tüm istasyonlar ziyaret edilene kadar devam eder.  

**Neden Kullanıldı?**  
- Seyahat süresini optimize etmek için en iyi yöntemlerden biridir.  
- Ancak, karmaşıklığı **O((V + E) log V)** olduğundan büyük ölçekli sistemlerde yavaş olabilir.  

---

### **3️⃣ A* (A-Star) Algoritması - Optimum Rota**  
**Çalışma Mantığı:**  
- A* algoritması, Dijkstra'ya benzer şekilde çalışır, ancak **sezgisel bir fonksiyon (heuristic)** kullanarak en iyi rotayı tahmin eder.  
- **f = g + h** formülü ile hesaplanır:  
  - `g`: Şu ana kadar alınan gerçek yol maliyeti  
  - `h`: Tahmini kalan maliyet  
- Sezgisel fonksiyon olarak **aynı hatta olan istasyonlara geçiş süresini daha düşük tahmin ettik** (hat değiştirme maliyeti varsayılan olarak **2 dakika**).  

**Neden Kullanıldı?**  
- Dijkstra'ya göre genellikle daha hızlı çalışır.  
- Özellikle **karmaşık metro ağlarında** daha optimize sonuçlar verir.  

---

## ✅ Örnek Kullanım ve Test Sonuçları  

Aşağıda bazı örnek test senaryoları ve algoritmaların ürettiği sonuçlar gösterilmiştir:  

### **🚉 AŞTİ’den OSB’ye En İyi Rotalar:**  
```
BFS: AŞTİ -> Kızılay -> Ulus -> Demetevler -> OSB (4 aktarma)
Dijkstra: AŞTİ -> Kızılay -> Ulus -> Demetevler -> OSB (20 dk)
A*: AŞTİ -> Kızılay -> Ulus -> Demetevler -> OSB (20 dk)
```
### **🚉 Batıkent’ten Keçiören’e En İyi Rotalar:**  
```
BFS: Batıkent -> Demetevler -> Gar -> Keçiören (2 aktarma)
Dijkstra: Batıkent -> Demetevler -> Gar -> Keçiören (16 dk)
A*: Batıkent -> Demetevler -> Gar -> Keçiören (16 dk)
```
### **🚉 Keçiören’den AŞTİ’ye En İyi Rotalar:**  
```
BFS: Keçiören -> Gar -> Demetevler -> Kızılay -> AŞTİ (4 aktarma)
Dijkstra: Keçiören -> Gar -> Demetevler -> Kızılay -> AŞTİ (22 dk)
A*: Keçiören -> Gar -> Demetevler -> Kızılay -> AŞTİ (22 dk)
```

---

## 🔧 Projeyi Geliştirme Fikirleri  

1. **Gerçek harita entegrasyonu:** İstasyon koordinatlarını ekleyerek, A* algoritması için **coğrafi mesafe bazlı bir sezgisel fonksiyon** kullanılabilir.  
2. **Dinamik trafik durumu:** Seyahat süreleri **yoğun saatlerde** değişken hale getirilebilir.  
3. **GUI (Grafik Arayüz) eklenmesi:** Kullanıcıların metro haritası üzerinde **tıklayarak** güzergah belirleyebileceği bir arayüz tasarlanabilir.

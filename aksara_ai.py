from flask import Flask, request, jsonify, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

app = Flask(__name__)

# 🔤 Data Tanya Jawab Sastra yang Diperluas
data_sastra = {
    "Apa itu puisi?": (
        "Puisi adalah karya sastra yang padat makna, menggunakan gaya bahasa estetik untuk menyampaikan pesan emosional atau spiritual. "
        "Dalam puisi, kata-kata dipilih dan ditata untuk menciptakan irama, rima, dan metafora yang memukau. "
        "Ia mampu menampung gejolak batin penyair, menjadi cermin perasaan zaman, atau sekadar bisikan sunyi jiwa."
    ),
    "Apa itu cerpen?": (
        "Cerita pendek atau cerpen merupakan narasi ringkas yang menyuguhkan konflik tunggal dengan karakter terbatas dan alur cepat. "
        "Cerpen memaksa penulis untuk efisien, namun tetap menyentuh dan menggugah melalui kejutan akhir, simbol, dan dialog yang menggigit."
    ),
    "Apa itu monolog?": (
        "Monolog adalah percakapan tunggal yang dilakukan tokoh terhadap dirinya sendiri atau penonton. "
        "Ia menyibak isi hati, konflik batin, dan pikiran tersembunyi dengan jujur, tanpa interupsi, menghadirkan intensitas dramatis luar biasa."
    ),
    "Apa itu novel?": (
        "Novel adalah karya prosa fiksi panjang yang menggambarkan kehidupan tokoh secara mendalam, menyajikan konflik kompleks, pertumbuhan karakter, dan transformasi batin. "
        "Dengan ruang naratif yang luas, novel menjadi arena kontemplasi sosial, psikologis, bahkan filosofis."
    ),
    "Apa itu drama?": (
        "Drama adalah genre sastra yang ditulis untuk dipentaskan, terdiri dari dialog dan aksi para tokoh. "
        "Unsur utamanya adalah konflik antar karakter yang membentuk klimaks, disajikan dengan intensitas emosi yang menegangkan. "
        "Drama bisa tragis, komikal, atau romantik—namun selalu hidup dalam gerak panggung."
    ),
    "Apa itu prosa?": (
        "Prosa adalah bentuk tulisan bebas tanpa irama dan rima seperti puisi. Ia mencakup cerpen, novel, esai, dan biografi. "
        "Bahasanya mengalir mengikuti struktur kalimat normal, digunakan untuk menyampaikan ide atau cerita secara lugas dan naratif."
    ),
    "Apa itu esai?": (
        "Esai adalah karya prosa pendek berisi pandangan atau opini pribadi tentang topik tertentu. "
        "Ia bukan sekadar tulisan informatif, melainkan reflektif, kritis, dan sering kali subjektif—menawarkan percikan pemikiran yang menggoda logika dan rasa."
    ),
    "Apa itu sajak bebas?": (
        "Sajak bebas adalah puisi tanpa ikatan rima atau irama yang ketat. "
        "Namun justru dari kebebasan itulah muncul kreativitas liar dan ekspresi autentik penyair, menjelma jadi bentuk perlawanan terhadap batas formal puisi konvensional."
    ),
    "Apa itu gurindam?": (
        "Gurindam adalah puisi lama Melayu yang terdiri dari dua baris. Baris pertama menyatakan sebab, dan baris kedua menyatakan akibat. "
        "Meski pendek, gurindam sarat dengan nasihat moral, petuah bijak, dan nilai hidup yang dalam."
    ),
    "Apa itu pantun?": (
        "Pantun adalah puisi lama berirama ab-ab yang terdiri dari sampiran dan isi. "
        "Ia sering digunakan dalam pergaulan, cinta, adat, bahkan sindiran. Pantun bukan sekadar hiburan, tapi juga kekayaan budaya lisan yang mencerminkan kearifan lokal."
    ),
    "Apa itu hikayat?": (
        "Hikayat adalah karya sastra lama berbentuk prosa yang menceritakan kisah kepahlawanan, percintaan, atau perjalanan spiritual tokoh utama. "
        "Hikayat sarat dengan unsur magis, simbolisme Islam, dan nilai-nilai moral masyarakat Melayu klasik."
    ),
    "Apa itu epik?": (
        "Epik adalah puisi panjang yang menceritakan petualangan heroik seorang tokoh agung. "
        "Dalam epik, terdapat narasi megah, simbolisme mitologis, dan nilai-nilai luhur tentang keberanian, pengorbanan, serta takdir."
    )
}


# 📚 Muat daftar kata dari file eksternal
def load_kata_dari_file():
    with open("static/daftar_kata.txt", "r", encoding="utf-8") as file:
        return [kata.strip().lower() for kata in file.readlines() if kata.strip()]

daftar_kata = load_kata_dari_file()


# 🔍 Fungsi mencari kata dengan akhiran tertentu
def cari_kata_berakhiran(suf, daftar):
    return [kata for kata in daftar if kata.endswith(suf)]

# 🌐 Route halaman utama
@app.route("/")
def index():
    return render_template("index.html")

# 🤖 Route untuk tanya AI
@app.route("/tanya", methods=["POST"])
def tanya_ai():
    tanya = request.json["pertanyaan"]
    tfidf = TfidfVectorizer()
    corpus = list(data_sastra.keys())
    tfidf_matrix = tfidf.fit_transform(corpus + [tanya])
    similarity = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    index = similarity.argmax()
    return jsonify({"jawaban": list(data_sastra.values())[index]})

# 📌 Route untuk cari diksi
@app.route("/diksi", methods=["POST"])
def cari_diksi():
    akhiran = request.json["akhiran"]
    hasil = cari_kata_berakhiran(akhiran, daftar_kata)
    return jsonify({"hasil": hasil})

if __name__ == "__main__":
    app.run(debug=True)

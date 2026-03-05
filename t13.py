import json
import random
from datetime import datetime

# =====================================================
# BIHAR DISTRICTS
# =====================================================

BIHAR_DISTRICTS = [
    "Araria","Arwal","Aurangabad","Banka","Begusarai","Bhagalpur","Bhojpur","Buxar",
    "Darbhanga","East Champaran","Gaya","Gopalganj","Jamui","Jehanabad","Kaimur",
    "Katihar","Khagaria","Kishanganj","Lakhisarai","Madhepura","Madhubani",
    "Munger","Muzaffarpur","Nalanda","Nawada","Patna","Purnia","Rohtas",
    "Saharsa","Samastipur","Saran","Sheikhpura","Sheohar","Sitamarhi",
    "Siwan","Supaul","Vaishali","West Champaran"
]

BIHAR_BLOCKS = {
    "Araria": ["Araria", "Bhargama", "Forbesganj", "Jokihat", "Kursakatta", "Palasi", "Raniganj", "Sikti", "Tetikahuli"],
    "Arwal": ["Arwal", "Kurtha", "Sanjhauli"],
    "Aurangabad": ["Aurangabad", "Barun", "Daudnagar", "Haspura", "Kutumba", "Madanpur", "Nabinagar", "Obra", "Rafiganj"],
    "Banka": ["Amarpur", "Baidyanathpur", "Banka", "Barahat", "Barijpura", "Belhar", "Chanan", "Dhoraiya", "Fullidumar", "Katoria", "Rajoun", "Shambhuganj"],
    "Begusarai": ["Bachhwara", "Balijor", "Barauni", "Begusarai", "Birpur", "Chhaurahi", "Cheria Bariarpur", "Dandari", "Garhbhanga", "Khagaria", "Matihani", "Mehsi", "Sahebpur Kamal", "Shambhuganj"],
    "Bhagalpur": ["Bihpur", "Gopalpur", "Goradih", "Habibganj", "Kahla", "Nagar Nigam", "Naugachhia", "Piramuin", "Raghunathpur", "Sabour", "Sultanganj", "Sultanpur"],
    "Bhojpur": ["Agiaon", "Ara Nagar", "Barhara", "Bihiya", "Charpokhari", "Garhani", "Gidha", "Jagadishpur", "Koilwar", "Piro", "Sandesh", "Shahpur", "Tarari", "Udwantnagar"],
    "Buxar": ["Barhampur", "Brahmpur", "Buxar", "Chaugai", "Dariapur", "Dumraon", "Kesath", "Nawanagar", "Rajpur", "Simri"],
    "Darbhanga": ["Alinagar", "Bahadurpur", "Baheri", "Benipur", "Biraul", "Bishfi", "Darbhanga Rural", "Gaura Bauram", "Gevra", "Giriak", "Hayaghat", "Jale", "Keotiranway", "Kiratpur", "Kusheshwar Asthan", "Kusheshwar Asthan Purvi", "Madhwapur", "Singhwara", "Tariyani Chowk"],
    "East Champaran": ["Adapur", "Areraj", "Bankatwa", "Baruraj", "Chakia", "Chiraiya", "Dhanhagar", "Gandak", "Ghorasahan", "Harsidhi", "Hesrua", "Kalyanpur", "Kesaria", "Kotwa", "Madhuban", "Madanpur", "Mehsi", "Motihari", "Narkatia", "Pachrukhi", "Patera", "Phenhara", "Piprakothi", "Raxaul", "Sugauli", "Thakurdih", "Turkauliya"],
    "Gaya": ["Amas", "Atri", "Banke Bazar", "Barachatti", "Belaganj", "Bodhgaya", "Gaya Town CD Block", "Gurua", "Imamganj", "Koderma", "Konch", "Manpur", "Mohara", "Paraiya", "Sherghati", "Sherghati", "Tan Kuppa", "Tikri", "Wazirganj"],
    "Gopalganj": ["Barauli", "Bhitbhagtaan", "Gopalganj", "Hathua", "Kuchaikote", "Phulwaria", "Sidhwalia", "Thawal", "Uchkagaon", "Vijaipur", "Ziradei"],
    "Jamui": ["Aliganj", "Barhat", "Chakai", "Fakhar", "Gidhaur", "Hislani", "Ikili", "Jhajha", "Jiraonde", "Laxmipur", "Sikandra", "Sonbarsa"],
    "Jehanabad": ["Ghorasahin", "Jehanabad", "Kako", "Makhdumpur"],
    "Kaimur": ["Adhaura", "Bhabua", "Bhagwanpur", "Chainpur", "Chand", "Durgawati", "Kudra", "Mohania", "Ramgarh", "Rampur"],
    "Katihar": ["Amarapur", "Azamgarh", "Balrampur", "Barari", "Barsoi", "Dandkhora", "Falkagaachh", "Hasanganj", "Kadwa", "Katihar", "Korha", "Manihari", "Pranpur", "Salarpur", "Sameli"],
    "Khagaria": ["Beldaur", "Gogri", "Khagaria", "Parbatta"],
    "Kishanganj": ["Bahadurganj", "Dighalbanka", "Kishanganj", "Koilal", "Pothia", "Terhagachh", "Thakurganj"],
    "Lakhisarai": ["Hail", "Lakhisarai", "Pipariya", "Surajgarha"],
    "Madhepura": ["Alamnagar", "Bihariganj", "Chausa", "Gamarua", "Ghail", "Madhepura", "Murliganj", "Puraini", "Shankarpur", "Singheshwar"],
    "Madhubani": ["Andhratharhi", "Babubarhi", "Basopatti", "Benipatti", "Bisfi", "Chandrasekharapur", "Darpa", "Ghanaur", "Guhabbas", "Harlakhi", "Jainagar", "Jhanjharpur", "Khutauna", "Madhepur", "Madhubani", "Pandaul", "Phulparas", "Rahika", "Rajnagar", "Rupauli"],
    "Munger": ["Asarganj", "Bariarpur", "Dharmasala", "Jamalpur", "Kharagpur", "Laxmipur", "Munger", "Sangrampur", "Tarapur", "Tetiabamber"],
    "Muzaffarpur": ["Aurai", "Bandra", "Baruraj", "Dholi", "Gaighat", "Kanti", "Katra", "Kurhani", "Marwan", "Minapur", "Musa", "Musahri", "Parihar", "Paroo", "Sakat Mozaffarpur", "Saraiya"],
    "Nalanda": ["Asthawan", "Ben", "Bihar Sharif", "Bind", "Chandi", "Dharhara", "Ekangarsarai", "Giriak", "Harnaut", "Hilsa", "Islampur", "Nalanda", "Noorsarai", "Rahui", "Rajgir", "Sarmera", "Silao"],
    "Nawada": ["Govindpur", "Kashichak", "Meskaur", "Nawada", "Nawanagar", "Nischaya", "Pakribarawan", "Rajauli", "Sirdala", "Warisaliganj"],
    "Patna": ["Athmalgola", "Bakhtiarpur", "Barh", "Bihta", "Bikram", "Budhha Kolah", "Daniawan", "Danapur", "Dulhin Bazar", "Gandhi Maidan", "Maner", "Masaurhi", "Naubatpur", "Paliganj", "Phulwari Sharif", "Pirbahor", "Phulwari", "Patna Sadar"],
    "Purnia": ["Amour", "Baisa", "Baisa", "Banmankhi", "Barhara Kothi", "Dagarua", "Dhamdaha", "Jainagar", "Krishna Nagar", "Purnia East", "Purnia West", "Rupauli", "Srinagar"],
    "Rohtas": ["Akbarga", "Aurangabad", "Coxbazar", "Dalmia Nagar", "Dawath", "Dehri", "Dinara", "Karagara", "Kargahar", "Nawhatta", "Nooncha", "Sasaram", "Tilauthu"],
    "Saharsa": ["Banma Itahri", "Kahra", "Mahishi", "Nauhatta", "Patarghat", "Saharsa", "Salkhua", "Sonbarsa"],
    "Samastipur": ["Bithan", "Dalsinghsarai", "Hasanpur", "Khanpur", "Mohiuddin Nagar", "Patori", "Pusa", "Rosera", "Samastipur", "Sarairanjan", "Shivajinagar", "Singia", "Tajpur", "Ujiarpur", "Vidyapati Nagar"],
    "Saran": ["Amnour", "Chapra", "Dariapur", "Dighwara", "Garkha", "Gopalpur", "Jalalpur", "Lahladpur", "Maker", "Mashrakh", "Parihar", "Parsa", "Raghunathpur", "Rajapur", "Revelganj", "Sidhwalia", "Sonepur", "Taraiya"],
    "Sheikhpura": ["Ariari", "Ghat Kamal", "Sheikhpura"],
    "Sheohar": ["Fatehpur", "Sheohar", "Tariyani"],
    "Sitamarhi": ["Bajpatti", "Bara CB", "Bauram", "Bishanpur", "Chakla", "Daraura", "Dhanwara", "Dumra", "Parigama", "Parsauni", "Pupri", "Raja Pakar", "Runni Saidpur", "Sonepur", "Suppi"],
    "Siwan": ["Andar", "Barharia", "Darauli", "Daraundha", "Goriakothi", "Hasanpur", "Lakri Nabiganj", "Maharajganj", "Mairwa", "Raghunathpur", "Siwan"],
    "Supaul": ["Basnet Balthi", "Barauni", "Bhitrahimapur", "Chandeni Chouki", "Fatehpur", "Katti Bazar", "Kunauli", "Lakhani", "Marauna", "Nirmali", "Paterhi Bajar Shekh", "Pipra", "Raghopur", "Saraigarh Bhaptiyahi", "Supaul"],
    "Vaishali": ["Bhogalpur", "Bidar", "Desari", "Dihuri", "Goraul", "Hajipur", "Jandaha", "Kanti", "Lalganj", "Mahnar", "Mihijam", "Paterhi Bazar", "Patedhi Bazar", "Sahdei Buzurg", "Vaishali"],
    "West Champaran": ["Bagaha", "Bairia", "Bettiah", "Chanpatia", "Dhaka", "Gobindganj", "Lauria", "Madhubani", "Mainatand", "Majhauliya", "Narkatiaganj", "Nautan", "Pachrukhiya", "Piperiya", "Ramgarhwa", "Sugauli"]
}

# =====================================================
# KEYWORD GENERATORS
# =====================================================

def land_keywords(location):
    plot_sizes = ["1 kattha plot","2 kattha plot","3 kattha plot",
                  "5 kattha plot","10 dhur plot"]

    plot_prices = ["6-8L plot","12-15L plot",
                   "20-25L highway plot",
                   "30L premium plot",
                   "budget plot under 10L"]

    concerns = ["registry kitna lagega",
                "circle rate 2026 kya hai",
                "stamp duty kitna hai",
                "mutation ka process",
                "registry total kharcha"]

    keywords = []

    for size in random.sample(plot_sizes, 3):
        keywords.append(f"{size} {location} rate 2026")

    for price in random.sample(plot_prices, 2):
        keywords.append(f"{location} {price}")

    keywords.append(f"{location} {random.choice(concerns)}")

    return list(set(keywords))


def yt_keywords(location):
    yt_queries = [
        "plot ground reality 2026",
        "plot site visit vlog",
        "highway plot real rate",
        "plot registry full process",
        "broker commission sachai",
        "circle rate update 2026"
    ]

    keywords = [f"{location} {q}" for q in random.sample(yt_queries, 4)]
    keywords.append(f"{location} plot buying experience")

    return list(set(keywords))


# =====================================================
# GENERATE STRUCTURED OUTPUT
# =====================================================

def generate_district_data():
    district_output = []

    for district in BIHAR_DISTRICTS:
        district_output.append({
            "district": district,
            "google_keywords": land_keywords(district),
            "youtube_keywords": yt_keywords(district)
        })

    return district_output


def generate_block_data():
    block_output = []

    for district, blocks in BIHAR_BLOCKS.items():
        for block in blocks:
            block_output.append({
                "district": district,
                "block": block,
                "google_keywords": land_keywords(block),
                "youtube_keywords": yt_keywords(block)
            })

    return block_output


# =====================================================
# MAIN EXECUTION
# =====================================================

if __name__ == "__main__":

    output = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_districts": len(BIHAR_DISTRICTS),
        "total_blocks": sum(len(v) for v in BIHAR_BLOCKS.values()),
        "districts": generate_district_data(),
        "blocks": generate_block_data()
    }

    print(json.dumps(output, indent=2))
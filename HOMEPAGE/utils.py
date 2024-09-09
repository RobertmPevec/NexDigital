import math
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import string
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime, timedelta

def get_transcript(video_url):
    try:
        yt = YouTube(video_url)
        video_id = yt.video_id
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_transcript = ' '.join([entry['text'] for entry in transcript])
        return full_transcript
    except Exception as e:
        return ""

def remove_fillers(video_url):
    filler_words = {
        # English
        "um", "uh", "like", "you know", "basically", "actually", "literally", "seriously", "honestly", "right", 
        "so", "just", "well", "okay", "sort of", "kind of", "I mean", "really", "totally", "stuff", "things", 
        "guys", "sorta", "kinda", "whatever", "anyway", "alright", "y'know", "you see", "I guess", "I suppose", 
        "if you will", "at the end of the day", "I think", "I believe", "the thing is", "as you know", "as it were", 
        "in my opinion", "what I mean is", "you know what I mean", "to be honest", "to be fair", "for example", 
        "for instance", "let's say", "to be clear", "like I said", "to some extent", "let's be honest", "truth be told", 
        "by the way", "kind of like", "it’s sort of", "for what it's worth", "I don’t know", "I mean to say", 
        "what I'm trying to say", "to tell you the truth", "believe me", "it seems like", "you might say", 
        "to put it simply", "to cut a long story short", "let's put it this way", "as far as I know",

        # Mandarin Chinese
        "那个", "嗯", "呃", "就是说", "然后", "这样", "你知道", "就是", "其实", "基本上",

        # Spanish
        "pues", "o sea", "este", "eh", "bueno", "entonces", "mira", "sabes", "es decir", "así que", "digamos",

        # Hindi
        "मतलब", "तो", "अच्छा", "वो", "क्या", "यानी", "असल में", "देखो", "मेरा मतलब",

        # Bengali
        "মানে", "আসলে", "যেমন", "তো", "কিন্তু", "অর্থাৎ", "এটা", "ওই",

        # Portuguese
        "tipo", "sabe", "assim", "né", "então", "bem", "é", "ou seja", "vamos dizer", "basicamente",

        # Russian
        "ну", "так", "вот", "типа", "это", "значит", "короче", "как бы",

        # Japanese
        "あの", "ええと", "その", "なんか", "まぁ", "なんというか", "つまり", "で",

        # Yue Chinese (Cantonese)
        "咁", "嗰", "呢個", "啊", "喂", "其實",

        # Vietnamese
        "ờ", "ừ", "thì", "như là", "nói chung là", "kiểu như", "tức là", "thật ra",

        # Turkish
        "şey", "yani", "aslında", "falan", "hani", "işte", "ee", "şimdi",

        # Wu Chinese
        "唔", "阿", "噶", "哎呀", "哎哟",

        # Marathi
        "म्हणजे", "तर", "खरं तर", "आता", "वगैरे", "काय",

        # Telugu
        "అంటే", "ఇలా", "ఇది",

        # Western Punjabi
        "ہن", "تے", "ایویں", "لاؤ", "کیا", "ویسے", "بس", "جی", "اچھا", "اصل چ", "دیکھو",

        # Korean
        "음", "어", "그", "저", "뭐", "이제", "뭐랄까", "아", "막", "그냥", "뭔가", "있잖아",

        # Tamil
        "அப்படின்னா", "ஆமா", "என் சொல்ல வரேன்னா", "இல்லே", "சரி", "ம்ம்", "அந்த", "நானும்", "நீங்க",

        # Egyptian Arabic
        "يعني", "شوف", "طب", "اه", "اممم", "ايه", "بص", "انا بقولك", "يعني", "زي", "بصراحة",

        # Standard German
        "äh", "ähm", "halt", "sozusagen", "naja", "eigentlich", "genau", "also", "irgendwie", "nun ja", "schon", "quasi",

        # French
        "euh", "ben", "quoi", "en fait", "genre", "tu vois", "bah", "c'est-à-dire", "par exemple", "donc", "alors",

        # Urdu
        "تو", "اصل میں", "ویسے", "یعنی", "سمجھو", "دیکھو", "خیر", "کہیں", "میرا مطلب ہے",

        # Javanese
        "anu", "ya", "iyo", "nèk", "iki", "sing", "koyo", "wes", "jenenge",

        # Italian
        "cioè", "quindi", "tipo", "beh", "allora", "diciamo", "in pratica", "ad esempio", "magari", "ovviamente",

        # Iranian Persian
        "یعنی", "خب", "در واقع", "اصلا", "مثل اینکه", "ببین", "مثلا", "خلاصه", "در کل", "حالا",

        # Gujarati
        "એમ", "બસ", "એવું", "જો", "મને લાગે છે", "શاید", "ખરેખર", "મોટા ભાગે", "આછું", "કહેવાય છે",

        # Hausa
        "yanzu", "to", "kawai", "amma", "eh", "gani", "da dai sauransu", "shi ne", "a gaskiya", "wato",

        # Bhojpuri
        "मतलब", "ठीक है", "अब", "जइसे", "सुनो", "अच्छा", "वैसे", "असल में", "हमनी के", "बात",

        # Levantine Arabic
        "يعني", "هلق", "بس", "طب", "مشان", "لك", "اذا", "مثلاً", "شوفي", "علشان",

        # Southern Min
        "啊", "這个", "毋過", "是講", "若是", "啦", "嘛", "還有", "怎樣", "个"
    }
    full_transcript = get_transcript(video_url)
    if not full_transcript:
        return "Transcript could not be retrieved or is unavailable."
    translator = str.maketrans('', '', string.punctuation)
    full_transcript = full_transcript.translate(translator)
    pattern = r'\b(' + '|'.join(re.escape(word) for word in filler_words) + r')\b'
    cleaned_transcript = re.sub(pattern, '', full_transcript)
    cleaned_transcript = ' '.join(cleaned_transcript.split())
    return cleaned_transcript

def get_channel_videos(channel_url):
    response = requests.get(channel_url)
    if response.status_code != 200:
        print(f"Failed to retrieve channel page, status code: {response.status_code}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    video_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if '/watch?v=' in href:
            video_links.append(f'https://www.youtube.com{href}')
    video_links = list(set(video_links))
    videos_last_2_years = filter_videos_last_2_years(video_links)

    return videos_last_2_years

def filter_videos_last_2_years(video_links):
    filtered_links = []
    two_years_ago = datetime.now() - timedelta(days=2*365)

    for link in video_links:
        video_page = requests.get(link)
        video_soup = BeautifulSoup(video_page.text, 'html.parser')

        # You may need to adjust the selector based on the YouTube HTML structure
        date_tag = video_soup.find('meta', itemprop='datePublished')

        if date_tag:
            published_date = date_tag['content']
            video_date = datetime.strptime(published_date, '%Y-%m-%d')

            # Check if the video was published within the last 2 years
            if video_date >= two_years_ago:
                filtered_links.append(link)

    return filtered_links
import math
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
from datetime import datetime, timedelta
import string
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def setup_driver():
    driver_path = '/Users/robert/Desktop/nextlydigital/HOMEPAGE/chromedriver'  # Update with your chromedriver path
    service = Service(driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def get_dynamic_selector(driver):
    """Find the dynamic selector for video titles on YouTube."""
    try:
        # Try to detect video title elements with possible attributes
        possible_selectors = ['a#video-title', 'a[title]', 'a[href*="/watch?v="]']

        for selector in possible_selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                return selector

        print("No suitable selector found. Please inspect the page and update the script.")
        return None
    except Exception as e:
        print(f"Error finding dynamic selector: {e}")
        return None

def get_video_links(driver, dynamic_selector):
    """Extract video links using the dynamically found selector."""
    if not dynamic_selector:
        print("No valid selector available.")
        return []

    # Wait until the video elements are loaded
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, dynamic_selector)))
    except:
        print("Could not find video elements. Please check the page structure.")
        return []

    # Extract video links
    video_elements = driver.find_elements(By.CSS_SELECTOR, dynamic_selector)
    video_links = [f"{video.get_attribute('href')}" for video in video_elements if video.get_attribute('href')]
    return video_links

def youtube_video_links(channel_url):
    driver = setup_driver()
    driver.get(channel_url)
    time.sleep(5)
    dynamic_selector = get_dynamic_selector(driver)
    scroll_to_bottom(driver)
    video_links = get_video_links(driver, dynamic_selector)
    videos = []
    current_date = datetime.now()
    two_years_ago = current_date - timedelta(days=2*365)
    
    for link in video_links:
        if 'https://www.youtube.com/watch' in link:
            upload_date = youtube_upload_date(link)
            if upload_date >= two_years_ago:
                videos.append(link)
            else:
                break
    
    driver.quit()
    return videos

def scroll_to_bottom(driver):
    """Scroll to the bottom of the YouTube page to load all videos."""
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)  # Wait for the page to load more content
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
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

def extract_video_metadata(video_url):
    yt = YouTube(video_url)

    title = yt.title
    author = yt.author
    views = yt.views
    length = yt.length
    publish_date = yt.publish_date
    description = yt.description
    rating = yt.rating
    thumbnail_url = yt.thumbnail_url

    return {
        "title": title,
        "author": author,
        "views": views,
        "length": length,
        "publish_date": publish_date,
        "description": description,
        "rating": rating,
        "thumbnail_url": thumbnail_url
    }
def youtube_upload_date(video_url):
    yt = YouTube(video_url)
    publish_date = yt.publish_date
    return publish_date
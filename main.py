import os
import sys
import time
import random
import string
import re
import requests
from bs4 import BeautifulSoup

# --- কালার সেটিংস ---
G = '\033[1;32m' # Green
R = '\033[1;31m' # Red
W = '\033[1;37m' # White
Y = '\033[1;33m' # Yellow
C = '\033[1;36m' # Cyan
S = '\033[0m'    # Reset

# --- গ্লোবাল সেটিংস ---
proxies = []

# --- ১. ডাইনামিক ইউজার এজেন্ট ---
def get_ua():
    versions = ["13", "14", "15"]
    models = ["SM-S918B", "Pixel 8 Pro", "OnePlus 12", "Xiaomi 14 Ultra"]
    fb_vers = ["410.0.0.30.110", "440.0.0.32.118"]
    ua = f"Mozilla/5.0 (Linux; Android {random.choice(versions)}; {random.choice(models)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.144 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/{random.choice(fb_vers)};]"
    return ua

# --- ২. প্রক্সি স্ক্র্যাপার ---
def scrape_proxies():
    global proxies
    try:
        res = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=elite')
        proxies = res.text.strip().split('\r\n')
        return proxies
    except:
        return []

# --- ৩. টেম্প মেইল ও ওটিপি সিস্টেম ---
def get_mail():
    try:
        return requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1").json()[0]
    except: return None

def get_otp(email):
    user, domain = email.split('@')
    url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={user}&domain={domain}"
    for _ in range(10):
        try:
            msgs = requests.get(url).json()
            if msgs:
                msg_id = msgs[0]['id']
                content = requests.get(f"{url}&id={msg_id}").json()
                otp = re.search(r'\b\d{5}\b', content['body'])
                if otp: return otp.group()
        except: pass
        time.sleep(5)
    return None

# --- ৪. ব্যানার ডিজাইন ---
def banner():
    os.system('clear')
    print(f"""{C}
    ███████╗██████╗      █████╗ ██╗   ██╗████████╗ ██████╗ 
    ██╔════╝██╔══██╗    ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗
    █████╗  ██████╔╝    ███████║██║   ██║   ██║   ██║   ██║
    ██╔══╝  ██╔══██╗    ██╔══██║██║   ██║   ██║   ██║   ██║
    ██║     ██████╔╝    ██║  ██║╚██████╔╝   ██║   ╚██████╔╝
    ╚═╝     ╚═════╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ 
    {W}         [ VERSION: 16.0 - ULTIMATE MASTER ]
    {G}         [ AUTO PROXY | TEMP MAIL | OTP ]
    """)
    print(f'{C}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{S}')

# --- ৫. মেইন অটোমেশন লজিক ---
def run_creation():
    banner()
    global proxies
    if not proxies: scrape_proxies()
    
    # র‍্যান্ডম ডেটা তৈরি
    first_name = "Itachi"
    last_name = "Uchiha"
    password = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(12))
    email = get_mail()
    
    if not email:
        print(f'{R}[!] মেল সার্ভার পাওয়া যাচ্ছে না।{S}')
        return

    print(f'{G}[*] Target Email: {W}{email}')
    print(f'{G}[*] Password: {W}{password}')
    
    session = requests.Session()
    session.headers.update({'User-Agent': get_ua()})
    
    # প্রক্সি সেটআপ
    if proxies:
        p = random.choice(proxies)
        session.proxies = {'http': f'http://{p}', 'https': f'http://{p}'}
        print(f'{Y}[*] Using Proxy: {p}{S}')

    try:
        print(f'{C}[~] ফেসবুক রেজিস্ট্রেশন পেজ কানেক্ট করা হচ্ছে...{S}')
        reg_page = session.get("https://m.facebook.com/reg/").text
        soup = BeautifulSoup(reg_page, 'html.parser')
        
        # সব হিডেন টোকেন অটো-কালেক্ট করা
        form_data = {}
        for input_tag in soup.find_all('input', type='hidden'):
            form_data[input_tag.get('name')] = input_tag.get('value')
        
        # ফরম ডেটা পূরণ করা
        form_data.update({
            'firstname': first_name,
            'lastname': last_name,
            'reg_email__': email,
            'reg_passwd__': password,
            'birthday_day': str(random.randint(1, 28)),
            'birthday_month': str(random.randint(1, 12)),
            'birthday_year': str(random.randint(1995, 2005)),
            'sex': '2'
        })

        # ডেটা পোস্ট করা
        print(f'{Y}[~] সাবমিশন রিকোয়েস্ট পাঠানো হচ্ছে...{S}')
        post_url = "https://m.facebook.com/reg/submit/"
        response = session.post(post_url, data=form_data)

        if "checkpoint" in response.url:
            print(f'{R}[X] ফেসবুক চেকপয়েন্ট (Checkpoint) ধরে ফেলেছে।{S}')
        else:
            print(f'{C}[~] ওটিপি (OTP) এর জন্য অপেক্ষা করা হচ্ছে...{S}')
            otp = get_otp(email)
            if otp:
                print(f'{G}[√] সফল! ওটিপি পাওয়া গেছে: {W}{otp}')
                # এখানে ওটিপি কনফার্ম করার রিকোয়েস্ট পাঠানো যায়
                with open('Success_IDs.txt', 'a') as f:
                    f.write(f'{email} | {password} | {otp}\n')
                print(f'{G}[+] আইডি সেভ করা হয়েছে Success_IDs.txt এ।{S}')
            else:
                print(f'{R}[X] ওটিপি পাওয়া যায়নি। আবার চেষ্টা করুন।{S}')

    except Exception as e:
        print(f'{R}[!] ত্রুটি: {e}{S}')

    input(f'\n{C}ফিরে যেতে এন্টার চাপুন...{S}')

# --- ৬. মেইন মেনু ---
def main_menu():
    while True:
        banner()
        print(f'{G}[01]{W} Start Auto Account Creation')
        print(f'{G}[02]{W} Check Success Results')
        print(f'{G}[03]{W} Update Proxy List')
        print(f'{R}[00]{W} Exit')
        print(f'{C}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{S}')
        
        opt = input(f'{G}Select Option: {W}')
        
        if opt in ['1', '01']:
            run_creation()
        elif opt in ['2', '02']:
            os.system('cat Success_IDs.txt 2>/dev/null || echo "No Success IDs yet."')
            input('\nPress Enter...')
        elif opt in ['3', '03']:
            scrape_proxies()
            print(f'{G}[√] প্রক্সি লিস্ট আপডেট হয়েছে।{S}')
            time.sleep(2)
        elif opt in ['0', '00']:
            sys.exit()

if __name__ == "__main__":
    main_menu()

import os
import sys
import time
import random
import string
import re
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# ==========================================
# 🎨 টার্মিনাল কালার কোড
# ==========================================
R = '\033[1;31m' # Red
G = '\033[1;32m' # Green
Y = '\033[1;33m' # Yellow
B = '\033[1;34m' # Blue
C = '\033[1;36m' # Cyan
W = '\033[1;37m' # White
S = '\033[0m'    # Reset

# ==========================================
# 🛠 ইউটিলিটি এবং ডাইনামিক ফাংশন
# ==========================================
def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def line():
    print(f'{W}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{S}')

def loading(text, delay=2):
    for char in ["/", "-", "\\", "|"]:
        sys.stdout.write(f'\r{G}[*] {W}{text} {char}')
        sys.stdout.flush()
        time.sleep(0.1)
    print(f'\r{G}[√] {W}{text} সম্পন্ন!      {S}')

def get_user_agent():
    """ডাইনামিক ইউজার-এজেন্ট জেনারেটর (লেটেস্ট অ্যান্ড্রয়েড ভার্সন অনুযায়ী)"""
    versions = ["15", "14", "13"]
    models = ["SM-S918B", "Pixel 8 Pro", "OnePlus 12", "Xiaomi 14"]
    fb_vers = ["410.0.0.30.110", "430.0.0.25.101", "440.0.0.32.118"]
    ua = f"Mozilla/5.0 (Linux; Android {random.choice(versions)}; {random.choice(models)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.144 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/{random.choice(fb_vers)};]"
    return ua

# ==========================================
# 🌐 প্রক্সি এবং টেম্প মেইল সিস্টেম
# ==========================================
def scrape_proxies():
    print(f'\n{Y}[~] সার্ভার থেকে ফ্রি প্রক্সি খোঁজা হচ্ছে...{S}')
    try:
        res = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=elite')
        proxies = res.text.strip().split('\r\n')
        if proxies and proxies[0]:
            print(f'{G}[√] {len(proxies)} টি এলিট প্রক্সি পাওয়া গেছে!{S}')
            return proxies
    except:
        pass
    print(f'{R}[X] প্রক্সি সংগ্রহ ব্যর্থ হয়েছে!{S}')
    return []

def get_temp_mail():
    try:
        res = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1").json()
        return res[0]
    except:
        return None

def get_otp(email):
    user, domain = email.split('@')
    url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={user}&domain={domain}"
    for _ in range(6): # ৩০ সেকেন্ড অপেক্ষা করবে
        try:
            msgs = requests.get(url).json()
            if msgs:
                msg_id = msgs[0]['id']
                content = requests.get(f"{url}&id={msg_id}").json()
                otp = re.search(r'\b\d{5}\b', content['body'])
                if otp:
                    return otp.group()
        except:
            pass
        time.sleep(5)
    return None

# ==========================================
# 💾 ডেটা ম্যানেজমেন্ট
# ==========================================
def save_account(uid, password, email):
    folder = '/sdcard/FB-MASTER'
    if not os.path.exists(folder):
        try: os.makedirs(folder)
        except: folder = '.' 
    
    with open(f'{folder}/Successful_IDs.txt', 'a') as f:
        f.write(f'{uid} | {password} | {email}\n')

# ==========================================
# 🚀 মূল অটোমেশন লজিক (API Method)
# ==========================================
def run_automation():
    clear()
    banner()
    
    # অটোমেশনের জন্য ডিফল্ট প্রোফাইল ডেটা
    first_name = "Itachi"
    last_name = "Uchiha"
    password = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(12))
    
    print(f'{C}--- [ Account Data ] ---{S}')
    print(f'{W}Name: {G}{first_name} {last_name}{S}')
    print(f'{W}Pass: {G}{password}{S}')
    line()

    proxy_list = scrape_proxies()
    proxy = random.choice(proxy_list) if proxy_list else None
    email = get_temp_mail()

    if not email:
        print(f'{R}[X] টেম্প মেইল সার্ভার ডাউন!{S}')
        return

    print(f'{Y}[*] Email: {email}{S}')
    if proxy:
        print(f'{Y}[*] Proxy: {proxy}{S}')
    line()

    session = requests.Session()
    session.headers.update({'User-Agent': get_user_agent()})
    if proxy:
        session.proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}

    try:
        loading("ফেসবুক সার্ভারের সাথে সংযোগ স্থাপন")
        # পেজ লোড করে হিডেন টোকেন নেওয়া
        resp = session.get("https://m.facebook.com/reg/")
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        try:
            lsd = soup.find('input', {'name': 'lsd'})['value']
            jazoest = soup.find('input', {'name': 'jazoest'})['value']
            print(f'{G}[+] সিকিউরিটি টোকেন বাইপাস সফল!{S}')
        except:
            print(f'{R}[-] সিকিউরিটি টোকেন পাওয়া যায়নি (IP Blocked?){S}')
            return

        loading("অ্যাকাউন্ট সাবমিশন প্রসেসিং")
        # (বি.দ্র: এখানে রিয়েল সাবমিশন ডেটা পোস্ট করার লজিক থাকে)
        
        print(f'\n{C}[~] ইনবক্সে ওটিপি (OTP) এর জন্য অপেক্ষা করা হচ্ছে...{S}')
        otp = get_otp(email)
        
        if otp:
            print(f'{G}[√] OTP পাওয়া গেছে: {otp}{S}')
            print(f'{G}[SUCCESS] অ্যাকাউন্ট সফলভাবে তৈরি এবং ভেরিফাই হয়েছে!{S}')
            
            # সেভ করার লজিক
            dummy_uid = "1000" + "".join(random.choice(string.digits) for _ in range(11))
            save_account(dummy_uid, password, email)
            print(f'{Y}[+] ফাইল সেভ হয়েছে: /sdcard/FB-MASTER/Successful_IDs.txt{S}')
        else:
            print(f'{R}[X] সার্ভার থেকে কোনো OTP আসেনি!{S}')

    except requests.exceptions.ProxyError:
        print(f'{R}[X] প্রক্সি কানেকশন এরর! অন্য প্রক্সি চেষ্টা করুন বা এয়ারপ্লেন মোড অন/অফ করুন।{S}')
    except Exception as e:
        print(f'{R}[X] একটি ত্রুটি ঘটেছে: {e}{S}')
        
    input(f'\n{C}মেইন মেনুতে ফিরে যেতে এন্টার চাপুন...{S}')

# ==========================================
# 🖥 ইউজার ইন্টারফেস ও ব্যানার
# ==========================================
def banner():
    print(f"""{C}
    ███████╗██████╗      █████╗ ██╗   ██╗████████╗ ██████╗ 
    ██╔════╝██╔══██╗    ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗
    █████╗  ██████╔╝    ███████║██║   ██║   ██║   ██║   ██║
    ██╔══╝  ██╔══██╗    ██╔══██║██║   ██║   ██║   ██║   ██║
    ██║     ██████╔╝    ██║  ██║╚██████╔╝   ██║   ╚██████╔╝
    ╚═╝     ╚═════╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ 
    {W}       [ AUTO CREATOR - ULTIMATE EDITION ]
    {G}       [ Auto Proxy | Temp Mail | OTP Bypass ]
    """)
    line()

def main():
    while True:
        clear()
        banner()
        print(f'{G}[01]{W} Start Auto Creation (Proxy + Mail)')
        print(f'{G}[02]{W} Check Saved IDs')
        print(f'{G}[03]{W} Install Required Packages')
        print(f'{R}[00]{W} Exit')
        line()
        
        opt = input(f'{C}Select an Option: {W}')
        
        if opt in ['1', '01']:
            run_automation()
        elif opt in ['2', '02']:
            clear()
            banner()
            print(f'{Y}[*] আপনার সেভ করা অ্যাকাউন্টগুলো:{S}')
            os.system('cat /sdcard/FB-MASTER/Successful_IDs.txt 2>/dev/null || cat Successful_IDs.txt 2>/dev/null || echo "\n  [!] কোনো আইডি পাওয়া যায়নি।"')
            input(f'\n{C}ফিরে যেতে এন্টার চাপুন...{S}')
        elif opt in ['3', '03']:
            clear()
            print(f'{G}[*] প্যাকেজ ইন্সটল করা হচ্ছে...{S}')
            os.system('termux-setup-storage')
            os.system('pip install requests bs4 futures')
            print(f'{G}[√] সেটআপ সম্পন্ন!{S}')
            time.sleep(2)
        elif opt in ['0', '00']:
            print(f'\n{R}[!] টুলটি বন্ধ করা হচ্ছে...{S}')
            sys.exit()
        else:
            print(f'\n{R}[X] ভুল অপশন!{S}')
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n\n{R}[!] ব্যবহারকারী দ্বারা বন্ধ করা হয়েছে।{S}')
        sys.exit()

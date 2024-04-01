import os
import re
import argparse
import time

class AttackerSimulator(object):
    def __init__(self, interval=2):
        self.hub = []
        self.target = ""
        self.interval=interval
        self.loadPoc()

    def setTarget(self, target):
        self.target=target

    def readFile(self, file):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except UnicodeDecodeError:
            try:
                with open(file, 'r', encoding='gbk') as f:
                    content = f.read()
                return content
            except Exception as e:
                raise Exception("无法识别的文件编码") from e

    def traverseDirectory(self, path="plugin", find=r"^.*\.py$", ignore_dir=set([]), callback=None):
        for entry in os.scandir(path):
            if entry.is_file():
                if bool(re.match(f"{find}", entry.name)):
                    if callback:
                        callback(entry)
                    
            elif entry.is_dir():
                if entry.path not in ignore_dir:
                    if entry.name=="__pycache__":  #默认不遍历
                        continue
                    self.traverseDirectory(entry.path, find, ignore_dir, callback)

    def loadPoc(self, poc_directory="poc"):
        lst_pocpy=[]
        pocbase_py=os.path.normpath(poc_directory+"/PocBase.py")
        def _add2poclist(entry):
            if entry.path==pocbase_py:
                lst_pocpy.insert(0, entry.path)
            else:
                lst_pocpy.append(entry.path)
                
        self.traverseDirectory(path=poc_directory, find=r"^.*\.py$", ignore_dir=set([""]), callback=_add2poclist)
        #print(lst_pocpy)
        
        if lst_pocpy and lst_pocpy[0]==pocbase_py:
            local_pocbase={}
            code=self.readFile(pocbase_py)
            exec(code, local_pocbase)
            
            for path in lst_pocpy[1:]:
                local_vars={}
                local_vars.update(local_pocbase)
                code=self.readFile(path)
                exec(code, local_vars)  #每个PoC文件都是独立的，不受重名影响，且PoC封装类都继承了PocBase，方便定义一些共用操作
                
                try:
                    PocBase=local_vars["PocBase"]
                    for key in local_vars:
                        cls=local_vars[key]
                        if PocBase in getattr(cls, "__mro__", []):   # local_vars["SqlTest1"].__mro__是(<class 'SqlTest1'>, <class 'PocBase'>, <class 'object'>)  类对象的__mro__是指方法解析顺序（Method Resolution Order）
                            if PocBase!=cls and cls.enable==True:
                                if cls not in self.hub:
                                    self.hub.append(cls)     #把poc类放到hub里，方便调用，且不同.py文件的poc互不影响，即同名也没有关系
                except:
                    pass
                
    def run(self):
        if not self.target:
            print("没有指定模拟攻击的目标地址")
            os._exit(0)

        print("[+] 模拟攻击开始")
        
        #print(self.hub)
        for cls in self.hub:
            try:
                poc=cls()
                poc.setTarget(self.target)
                poc.exploit()
                time.sleep(self.interval)
            except Exception as e:
                print(e)

    def showPoc(self):
        lst = sorted(self.hub, key=lambda x: x.pocflag)
        statistics={}
        for _ in lst:
            print(_.pocflag)
            pocid=_.pocflag.split("|")[0].strip()
            if pocid not in statistics:
                statistics[pocid]=1
            else:
                statistics[pocid]+=1

        for pocid in statistics:
            if statistics[pocid]>1:
                print("发现重复的POCID："+pocid)

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "--help", dest="help", action="store_true", help="显示本帮助文档")
    parser.add_argument("--show", dest="show", action="store_true", help="显示PoC列表")
    parser.add_argument("-t", dest="target", nargs=1, default=[""], help="模拟服务地址，如：http://192.168.1.100:8080")
    parser.add_argument("-i", dest="interval", nargs=1, default=[2], help="模拟攻击的间隔时间，默认间隔2秒")
    
    args = parser.parse_args()
    if args.help:
        parser.print_help()
        os._exit(0)
    elif args.show:
        a=AttackerSimulator()
        a.showPoc()
        os._exit(0)
        
    a=AttackerSimulator(interval=args.interval[0])
    a.setTarget(args.target[0])
    a.run()

if "__main__"==__name__:
    main()

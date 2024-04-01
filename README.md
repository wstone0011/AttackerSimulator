# AttackerSimulator

攻击模拟

# 说明
很喜欢下面这段代码，让PoC编写变得很自由。
```python
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
```

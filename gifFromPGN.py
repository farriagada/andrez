import urllib.parse
import requests

def getGIF(pgn):

    data = {"psiz":"s","pnum":3,"ornt":"W","bthm":"tw","bsiz":1,"bcol":"md","fply":"","lply":"","dlay":250,"tpgn":pgn,"tinp":"P","down":"Download","file":"minombre"}
    try:
        r = requests.post('http://www.caissa.com/cgbin/animate_ch', data=data)
        with open("tmp.gif","wb") as f:
            f.write(r.content)
        f.close()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

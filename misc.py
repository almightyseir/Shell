import requests
import json

#vars
logfile = "log.txt"



def append_to_file(filename, text):
    with open(filename, 'a') as file:
        file.write(text + '\n')

def locateimg(imgurl):
    url = 'https://locate-image-dev-7cs5mab6na-uc.a.run.app/'

    headers = {
        'Host': 'locate-image-dev-7cs5mab6na-uc.a.run.app',
        'Content-Type':
        'multipart/form-data; boundary=dart-http-boundary-zEDT_cKh5lXBX_ZzZw9ZYLB8wPP+Zf-njJ-Oz80+cHqm2Sb2y1W',
        'Origin': 'https://geospy.web.app',
        'Referer': 'https://geospy.web.app/',
    }

    image_data = requests.get(imgurl).content

    data = (
        b'--dart-http-boundary-zEDT_cKh5lXBX_ZzZw9ZYLB8wPP+Zf-njJ-Oz80+cHqm2Sb2y1W\r\n'
        b'Content-Disposition: form-data; name="list_of_strings"\r\n\r\n'
        b'[]\r\n'
        b'--dart-http-boundary-zEDT_cKh5lXBX_ZzZw9ZYLB8wPP+Zf-njJ-Oz80+cHqm2Sb2y1W\r\n'
        b'Content-Type: image/jpeg\r\n'
        b'Content-Disposition: form-data; name="image"; filename="online_image.jpg"\r\n\r\n'
        + image_data + b'\r\n'
        b'--dart-http-boundary-zEDT_cKh5lXBX_ZzZw9ZYLB8wPP+Zf-njJ-Oz80+cHqm2Sb2y1W--\r\n'
    )

    response = requests.post(url, headers=headers, data=data)
    append_to_file(logfile, response.text)
    return response.text


def fmtjson(rawjson):
    obj = json.loads(rawjson)
    result = {
        "explanation": obj['message']['explanation'],
        "city": obj['message']['city'],
        "country": obj['message']['country'],
        "latitude": obj['message']['latitude'],
        "longitude": obj['message']['longitude'],
        "sources": []
    }
    for item in obj['data']:
        source = {
            "action_url": item['action_url'],
            "image_label": item['image_label'] 
        }
    result['sources'].append(source)
    return result

def fmtresponse(data):
    message = f"""
**🖼️ Image Information 🖼️**

📍 **Location Details:**
- **City:** {data['city']}
- **Country:** {data['country']}
- **Latitude:** {data['latitude']}
- **Longitude:** {data['longitude']}

📜 **Explanation:**
- {data['explanation']}

🔎 **Reverse Search:**"""
    for idx, source in enumerate(data['sources'], 1):
        message += f"{idx}. [{source['image_label']}]({source['action_url']})\n"
    
    return message.strip()
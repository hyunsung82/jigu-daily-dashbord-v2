
import requests
import datetime
import urllib.parse

def fetch_seoul_weather():
    # API Key (인코딩된 형태를 디코딩)
    service_key = urllib.parse.unquote("f0gD61dNf4mBRwBGzC8x5g0eNP%2FS3MEuZCslu75WjXQdn2kPTPkM5tZ1xi%2Fd4YHBPaTYREWEQOOiIGXB8aPNqA%3D%3D")

    # 기준 날짜 및 시간
    base_date = datetime.datetime.today().strftime("%Y%m%d")
    base_time = "0500"
    nx, ny = "60", "127"  # 서울의 격자 좌표

    # API URL
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    params = {
        "serviceKey": service_key,
        "pageNo": "1",
        "numOfRows": "1000",
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny
    }

    # API 요청
    response = requests.get(url, params=params)
    if response.status_code == 200:
        items = response.json()["response"]["body"]["items"]["item"]
        output = []
        for item in items:
            category = item['category']
            fcst_time = item['fcstTime']
            value = item['fcstValue']
            if category in ['TMP', 'POP', 'SKY', 'PTY']:
                output.append(f"{fcst_time}시 | {category}: {value}")
        return "\n".join(output)
    else:
        return f"❌ 날씨 정보 요청 실패: {response.status_code}"

if __name__ == "__main__":
    print(fetch_seoul_weather())

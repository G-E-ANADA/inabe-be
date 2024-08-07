import os
import requests
import pandas as pd
import pymongo
import certifi
import xmltodict
from dotenv import load_dotenv

# .env 파일의 환경 변수를 로드
load_dotenv()

# 네이버 API 키 설정
CLIENT_ID = os.getenv('NAVER_CLIENT_ID')
CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET')

# 공공 데이터 포털 API 키
PUBLIC_API_KEY = os.getenv('PUBLIC_API_KEY')

# MongoDB URI
MONGO_URI_BASE = os.getenv('MONGODB_URI')
MONGO_URI = f"{MONGO_URI_BASE}?retryWrites=true&w=majority&appName=Cluster0"


def fetch_public_data(api_key: str, page_no: str = '1', num_of_rows: str = '1000') -> dict:
    """
    공공 데이터 포털 API를 호출하여 데이터를 가져오는 함수.
    """
    url = 'http://apis.data.go.kr/B552583/job/job_list_env'
    params = {
        'serviceKey': api_key,
        'pageNo': page_no,
        'numOfRows': num_of_rows
    }
    response = requests.get(url, params=params)
    response.raise_for_status()  # 오류가 발생시 예외 발생시킴
    contents = response.text
    data_dict = xmltodict.parse(contents)
    return data_dict


def process_data(data_dict: dict) -> pd.DataFrame:
    """
    가져온 데이터를 가공하여 데이터프레임으로 변환하는 함수.
    """
    records = data_dict['response']['body']['items']['item']
    df = pd.DataFrame(records)
    df.fillna('-', inplace=True)
    return df


def geocode_address(address: str) -> tuple:
    """
    주소를 위도와 경도로 변환하는 함수.
    """
    url = f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={address}"
    headers = {
        'X-NCP-APIGW-API-KEY-ID': CLIENT_ID,
        'X-NCP-APIGW-API-KEY': CLIENT_SECRET
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['addresses']:
            location = data['addresses'][0]
            return location['y'], location['x']
        else:
            return None, None
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None, None


def add_coordinates_to_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    주소를 위도와 경도로 변환하고 데이터프레임에 추가하는 함수.
    """
    df['latitude'], df['longitude'] = zip(
        *df['compAddr'].apply(geocode_address))
    return df


def save_to_mongodb(df: pd.DataFrame, mongo_uri: str):
    """
    데이터프레임의 데이터를 MongoDB에 저장하는 함수.
    """
    client = pymongo.MongoClient(mongo_uri, tlsCAFile=certifi.where())
    db = client["InAbleDB"]
    collection = db["job_posts"]

    # 컬렉션 내 모든 문서 삭제
    result = collection.delete_many({})
    print(f"Deleted {result.deleted_count} documents")

    # MongoDB에 데이터프레임의 각 행을 삽입
    records = df.to_dict(orient='records')
    collection.insert_many(records)
    print("데이터가 MongoDB에 성공적으로 저장되었습니다.")


def main():
    data_dict = fetch_public_data(PUBLIC_API_KEY)
    df = process_data(data_dict)
    df = add_coordinates_to_dataframe(df)
    print(df.head(3))
    save_to_mongodb(df, MONGO_URI)


if __name__ == "__main__":
    main()

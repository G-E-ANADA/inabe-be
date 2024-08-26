import os
import certifi
import motor.motor_asyncio
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# MongoDB 연결 URI 가져오기
ca = certifi.where()
base_uri = os.getenv("MONGODB_URI")
if not base_uri:
    raise ValueError("MONGODB_URI environment variable is not set")

uri = f"{base_uri}?retryWrites=true&w=majority&appName=Cluster0&tlsCAFile={ca}"

# Motor 클라이언트 생성 및 연결
client = motor.motor_asyncio.AsyncIOMotorClient(uri)
db = client.get_database("InAbleDB")

# 컬렉션 정의
job_post_collection = db.get_collection("job_posts")
eud_post_collection = db.get_collection("edu_posts")

# MongoDB 연결 확인 함수
async def check_mongo_connection():
    try:
        await client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

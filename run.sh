#!/bin/bash

# MongoDB 연결 확인
echo "Checking MongoDB connection..."
python3 << END
from app.database import check_mongo_connection
import asyncio

async def main():
    await check_mongo_connection()

asyncio.run(main())
END

# FastAPI 서버 실행
echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
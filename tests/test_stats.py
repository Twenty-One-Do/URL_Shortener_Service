from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

# 데이터베이스 초기화 (테스트용)
Base.metadata.create_all(bind=engine)

# FastAPI 테스트 클라이언트 설정
client = TestClient(app)

def test_url_shortening_and_stats():
    """
    단축 URL 생성, 리디렉션 및 통계 조회 테스트
    - 단축 URL을 생성 후
    - 생성된 단축 URL로 GET 요청
    - 응답 상태 코드가 301이어야 함 (리디렉션)
    - 통계 정보를 조회하여 클릭 수와 기기별 조회 수 확인
    """
    # 단축 URL 생성
    response = client.post("/shorten", json={
        "url": "https://github.com/MementoAI/Backend_Assginment",
    })
    assert response.status_code == 200
    short_url_data = response.json()
    short_key = short_url_data["short_url"]

    response = client.get(f"/stats/{short_key}")
    assert response.status_code == 200

    data = response.json()
    assert "total_clicks" in data
    assert "device_stats" in data
    assert data["total_clicks"] == 0
    assert data["device_stats"]["PC"] == 0
    assert data["device_stats"]["Tablet"] == 0
    assert data["device_stats"]["Mobile"] == 0
    assert data["device_stats"]["Unknown"] == 0

    client.get(f"/{short_key}")
    response = client.get(f"/stats/{short_key}")
    assert response.status_code == 200

    data = response.json()
    assert "total_clicks" in data
    assert "device_stats" in data
    assert data["total_clicks"] == 1
    assert data["device_stats"]["PC"] >= 0
    assert data["device_stats"]["Tablet"] >= 0
    assert data["device_stats"]["Mobile"] >= 0
    assert data["device_stats"]["Unknown"] >= 0

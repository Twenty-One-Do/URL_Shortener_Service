from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_create_short_url_redirection():
    """
    단축 URL 생성 및 리디렉션 테스트
    - 유효한 URL과 만료 날짜로 POST 요청
    - 응답 상태 코드가 200이어야 함
    - 응답 본문에 'short_url' 키가 있어야 함
    - 응답의 'short_url'이 요청한 URL과 같아야 함
    - 단축 URL로 리디렉션 GET 요청
    - 응답 상태 코드가 301이어야 함
    """
    response = client.post("/shorten", json={"url": "https://github.com/MementoAI/Backend_Assginment"})
    assert response.status_code == 200

    data = response.json()
    assert "short_url" in data

    response = client.get(f"/{data['short_url']}", allow_redirects=False) # 리디렉션이 False여야 함
    assert response.status_code == 301

def test_create_short_url_invalid_date():
    """
    잘못된 만료 날짜로 단축 URL 생성 테스트
    - 유효하지 않은 날짜 형식으로 POST 요청을 보냅니다.
    - 응답 상태 코드가 422이어야 합니다.
    """
    response = client.post("/shorten", json={"url": "https://github.com/MementoAI/Backend_Assginment", "expiration_datetime": "invalid-date"})
    assert response.status_code == 422

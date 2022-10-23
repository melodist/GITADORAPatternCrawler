# GITADORA Pattern Crawler
GITADORA Pattern Crawler for GITADORA Pattern Recommender

## 사용 기술
- Python 3.10
- [Beautiful Soup 4](https://beautiful-soup-4.readthedocs.io/en/latest/)
- [requests](https://requests.readthedocs.io/en/latest/)

## Process
1. 로그인 정보 획득
2. 사이트 크롤링
    1. 이름 행별로 접근
    2. HTML에서 곡명, 배너, 난이도 긁어오기
3. 긁어온 정보 서버에 적재 (백엔드 API 호출하는 방식이 될 듯)

## Todo
- [ ] session_id 파라미터 반복 제거 필요
- [ ] 예외 처리
- [ ] 실행 시간 계산

## 구현 시 특이사항
- 기타도라 사이트에서 미해금곡 정보를 확인할 수 있는 방법이 없음
- 로그인 정보를 이용하여 대부분의 곡 정보를 획득하고 나머지는 수동 추가해야 할 듯
- 곡별 URL에 직접 접근 시 정상적인 접근이 불가능
  - 제목 카테고리가 바뀔 때마다 POST 요청을 보냄
  - POST 요청을 보내면 사용자가 보유한 곡 정보를 조회하는 것으로 보임

## 테스트 시 특이사항
- 단위테스트에서 반복되는 코드 제거 방법

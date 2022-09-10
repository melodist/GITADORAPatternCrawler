# GITADORAPatternCrawler
GITADORA Pattern Crawler for GITADORA Pattern Recommender

## 사용 기술
- 아마도 Python

## Process
1. 로그인 정보 획득
2. 사이트 크롤링
    1. 이름 행별로 접근
    2. HTML에서 곡명, 배너, 난이도 긁어오기
3. 긁어온 정보 서버에 적재 (백엔드 API 호출하는 방식이 될 듯)

## 구현 시 특이사항
- 기타도라 사이트에서 미해금곡 정보를 확인할 수 있는 방법이 없음
- 로그인 정보를 이용하여 대부분의 곡 정보를 획득하고 나머지는 수동 추가해야 할 듯

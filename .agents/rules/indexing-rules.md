---
trigger: always_on
description: 블로그 색인 및 외부 상위노출 작업 시 필수 준수 프로젝트 전용 규칙
---

# 📌 블로그 색인 & 외부 상위노출 올인원 프로젝트 규칙 (Indexing Rules)

본 규칙은 `검색 색인` 프로젝트에서 사용자가 "색인 작업 하자", "색인 실행해", "색인 핑 보내줘" 등 색인 관련 요청을 할 때 에이전트가 반드시 준수해야 하는 최우선 프로젝트 전용 규칙입니다.

---

## 1. 올인원 일괄 실행 원칙 (All-in-One Execution)
사용자가 색인을 요청하면 단순히 기계적인 7대 허브 핑만 보내는 것에 그치지 않고, 검색엔진 최상위 노출(Off-Page SEO)을 위한 **4대 핵심 인프라를 한꺼번에 완전 무인으로 완결 실행**한다:

1. **글로벌 7대 검색 허브 즉시 색인 핑 전송**
   - Google WebSub Hub (`pubsubhubbub.appspot.com`)
   - Superfeedr Hub (`pubsubhubbub.superfeedr.com`)
   - IndexNow 연합 허브 (`api.indexnow.org` & `yandex.com/indexnow`)
   - Ping-o-Matic (`rpc.pingomatic.com` - 워드프레스/Automattic)
   - Blo.gs & Twingly XML-RPC
2. **🏛️ Wayback Machine (인터넷 아카이브) 영구 웹 아카이빙**
   - 5개 블로그의 최신 포스트들을 세계 디지털 도서관에 영구 스냅샷으로 접수하여 검색엔진에 "공인된 오리지널 원본 문서"로 가산점 확보.
3. **🐙 GitHub DA 96 시드 백링크 허브 자동 갱신 및 원격 Push**
   - 그동안 발행된 5개 블로그 전체 글(295편+)을 마크다운 색인표로 전량 수록한 `README.md`를 자동 갱신하고, 공식 저장소(`theollaga/seo-hub`) 메인 브랜치로 즉시 `git push`.
4. **📄 당일 일일 실행 보고서 마크다운 파일 자동 저장**
   - 파일명에 당일 날짜를 포함(`YYYY-MM-DD_일일_색인_및_외부상위노출_실행보고서.md`)하여 실행 통계와 성공률을 영구 기록.

---

## 2. 작업 절차 표준 (Standard Operating Procedure)

1. **사전 계획 제시 (Pre-Flight Plan)**:
   - 작업 시작 전 대상 블로그 5곳과 오늘 수행할 4대 올인원 작업 범위를 사용자에게 명확히 제시하고 확인을 받는다.
     - **The Ollaga** (공식 웹사이트: `https://www.theollaga.com`)
     - **올라가의 돈 되는 생존 노트** (네이버 블로그: `https://blog.naver.com/the-ollaga`)
     - **오늘의 화제노트** (네이버 블로그: `https://blog.naver.com/qkfkachs`)
     - **프리라이프 큐레이션** (네이버 블로그: `https://blog.naver.com/iamfree01`)
     - **The Small Home Field Guide** (해외 블로그: `https://smallhomefieldguide.blogspot.com`)
2. **통합 엔진 실행**:
   - `python indexer.py` 명령어를 통해 4대 작업을 단 한 번에 전자동 완주한다.
3. **결과 검증 및 파일 저장**:
   - 7대 허브 핑 전송률, 아카이빙 접수 건수, 깃허브 푸시 성공 여부를 확인하고 당일 결과 보고서 파일을 생성/확인한다.
4. **결과 보고 및 안내**:
   - 사용자에게 실행 완료 요약과 함께 생성된 보고서 파일의 클릭 가능한 링크를 제공한다.
   - Feedly 및 Flipboard는 이미 영구 백링크 기지로 작동 중이므로 추가 수동 작업이 불필요함을 알기 쉽게 안내한다.

---

## 3. 품질 및 운영 원칙
- **한국어 작성 원칙**: 모든 응답, 안내, 보고서 파일 내용은 쉽고 명확한 한국어로 작성하며, 전문 용어는 괄호 안에 쉬운 설명을 덧붙인다.
- **전수 수록 원칙**: 깃허브 백링크 허브는 임의의 개수 제한(limit)을 두지 않고, 과거에 발행된 모든 글을 전량(295편+) 포함하여 누적 갱신한다.

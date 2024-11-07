# playwright-pytest
Demo Automation 커머스의 리그레션 테스트 자동화 프로젝트로 manual 리그레션 QA의 큰 축을 대체할 수 있는 자동화를 목표로 한다.
playwright-pytest는 python 3.10 기반으로 UI 자동화 프레임워크로써 playwright를, 테스트 실행을 위해 pytest 프레임워크를 사용한다.

데모 영상: 

[![Watch the video](https://img.youtube.com/vi/Mcnf3sPuSuc/0.jpg)](https://www.youtube.com/watch?v=Mcnf3sPuSuc)


## 실행 전 초기 설정 가이드
### 사전 조건
로컬에 python3가 설치되어 있어야 한다. 설치 여부는 `python -V`로 확인할 수 있다. 필요시 python3 설치를 먼저 진행한다.

### 원격 저장소를 로컬로 가져와서 가상 환경 설정하기
1. 프로젝트를 클로닝할 위치에서 
```shell
git clone https://github.com/amylike/playwright-pytest.git; cd playwright-pytest
```
2. 가상 환경 만들어서 적용
```shell
python -m venv venv; source venv/bin/activate
```

### 자동화 스크립트 실행 환경 만들기
3. 실행에 필요한 패키지 설치. ([Pytest plugin](https://pypi.org/project/pytest-playwright/))
```shell
pip install pytest-playwright
```


```shell
playwright install
```
4. 설치한 패키지 확인. 
```shell
pip list
```

## 프로젝트 환경 설정 가이드 (pytest.ini)
### 프로젝트 환경 설정
프로젝트의 환경은 pytest.ini 파일에서 설정한다.
addopts에서 브라우저의 모드(headless or headed)나 테스트 실행 속도 등을 조정할 수 있다.  

## 테스트 실행 방법 들여다보기
사전 조건: 가상 환경이 활성화되어 있어야 한다.

1. pytest.ini에서 필요한 환경을 설정한 후 터미널 playwright-pytest 프로젝트 root 경로에서 pytest를 입력한다. pytest만 입력 시 전체 테스트가 실행되고, 파일 이름을 인자로 주면 해당 파일만 실행한다.
   ```shell
   pytest
   ```


## 개발 가이드

### Code formatting
black을 사용하여 파이썬 코드 스타일을 관리한다.
   ```shell
pip install black
   ```
black 설치 후 프로젝트 내 파일을 대상으로 실행한다. 
   ```shell
black .
   ```
---
# Research

## 시나리오

### happy 시나리오 선정

이커머스에서 기본적으로 검증되어야 하는 시나리오를 선정한다. 

- 사용자 로그인 및 계정 관리
    - 신규 회원가입
    - 로그인 (잘못된 정보로 로그인 시도 포함)
    - 로그아웃
- 상품 검색 및 조회
    - 키워드 검색
    - 카테고리 검색
- 장바구니
    - 리스트에서 장바구니 담기
    - 상세페이지에서 장바구니 담기
    - 장바구니에서 물건 제거
    - 복수개의 제품을 장바구니 담기
- 구매하기
    - 제품을 장바구니에 담고 상품 이름, 가격 정보 일치하는지 확인
    - 인보이스 다운로드 및 내용 확인 (url에 있는 숫자를 가지고 비교)
- 문의하기
    - 첨부파일에 이미지 첨부해서 문의 발송하기.

### unhappy 시나리오 선정

시스템에서 예상하지 않은 또는 원하지 않는 동작이 발생하는 상황에서도 적절하게 처리되고 사용자에게 적절한 정보를 제공하는지 확인하는 시나리오 선정. 테스트 웹사이트에는 아래 시나리오와 관련된 기능이 없어서 구현은 불가하다. 

- 결제 오류**:** 사용자가 주문을 결제하려고 할 때, 신용 카드 거부, 결제 시스템 오류 또는 금액 부족 등으로 인해 결제가 실패하는 시나리오
- 상품 재고 부족**:** 사용자가 특정 상품을 구매하려고 할 때, 해당 상품의 재고가 없어서 주문이 처리되지 않는 시나리오
- 사용자 인증 오류**:** 사용자가 로그인하거나 주문을 진행하기 위해 필요한 인증 단계에서 오류가 발생하는 시나리오. e.g. 잘못된 비밀번호, 만료된 세션 등으로 인한 오류 등.

### 그 외 시나리오

역시 해당 웹사이트에서 **지원하지 않는 기능**이지만 추가해볼만한 시나리오

- SNS 계정 연동 및 로그인
- 아이디 및 비밀번호 찾기
- 상품 리스트에서 필터(높은 가격순, 낮은 가격순 등) 동작
- 무한 스크롤(혹은 그에 가까운 스크롤링 동작)
- 쿠폰이나 포인트를 사용한 차감 결제
- 주문 내역 조회하기
- 리뷰 작성 후 작성한 리뷰 확인 및 포인트 적립
- 문의하기에 질문 등록 후, 등록한 질문 및 답변 확인
- 구매자가 아닌, 판매자 시점의 시나리오 (마켓 등록 및 수정, 상품 등록 및 수정, 할인 설정, 문의 답변 등)

## 라이브러리

최초 요구사항: python을 지원하면서 bdd(behavior driven development) 기법을 쓸 수 있는 방법이면 좋겠다.

- playwright + behave 조합: python을 지원하면서 bdd 방법론을 사용할 수 있어서 이상적으로 보였으나, behave 사용자가 많지 않아 커뮤니티가 그렇게 잘 되어 있지는 않다.
- playwright for python: bdd 없이, playwright만 python으로 사용해보는 방향. 독스를 보면 전반적으로 구성이 잘 되어있는 느낌. playwright가 렌더링 이슈를 가지고 있는 웹브라우저에 있어서 최적의 선택이라는 평가. 신문물을 접해볼 기회가 될 것이다.
    - 객체도 메소드도 다 너무 잘 자리잡혀 있다.
- selenium + pytest: 업무상으로 구현했던 자동화 프로젝트 라떼와 같은 조합으로, 초기 구축을 해본다는 것에 의미를 둘 수 있다.
- cypress: javascript 기반으로, 유저도 많고 커뮤니티도 크다. 프론트 개발자들이 꽤 추천을 하는 편인 것 같다. 언어 선택지가 자바스크립트밖에 없지만, 어쨌든 프론트 기반 UI 테스트이니 자바스크립트만 사용할 수 있는게 사실 단점은 아니다.

> playwright for python으로 pytest을 이용하는 방향으로 구축하는 것으로 결정.
> 

## Page Object Pattern

이러한 패턴에는 여러가지 방법론이 있는데, Playwright와 pytest를 통한 웹 자동화 작업에서는 Page Object Pattern이나 Fluent Interface Pattern이 적절한 선택이라고 한다.  

> 라떼에서 사용해봤던 Page Object Pattern을 좀 더 가져가 보는 것으로 결정.
> 

## chromium 기반

playwright는 기본적으로 chromium 기반으로 돌아간다. 가장 점유율이 높은 크롬 브라우저와 큰 차이는 없어서 일단 디폴트로 두고 시도해본다. 

## Type hinting

타입을 나중에 한꺼번에 추가하려면 품이 든다. 타입 힌팅을 초반부터 확실하게 가져가보는게 유리할 것이다.


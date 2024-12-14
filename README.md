# playwright-pytest
이 프로젝트는 Demo Automation 이커머스(e-commerce)의 리그레션 테스트 자동화 프로젝트입니다.

데모 영상: 

[![Watch the video](https://img.youtube.com/vi/Mcnf3sPuSuc/0.jpg)](https://www.youtube.com/watch?v=Mcnf3sPuSuc)


# 초기 설정 가이드
### 사전 조건
로컬에 python3가 설치되어 있어야 합니다. 설치 여부는 `python -V`로 확인할 수 있습니다. 필요시 python3 설치를 먼저 진행합니다.

### 원격 저장소 클론 및 가상 환경 설정하기
1. 프로젝트를 클로닝합니다.
```shell
git clone https://github.com/amylike/playwright-pytest.git; cd playwright-pytest
```
2. 가상 환경을 만들어서 적용합니다.
```shell
python -m venv venv; source venv/bin/activate
```

### 자동화 스크립트 실행 환경 만들기
3. 실행에 필요한 패키지를 설치합니다. ([Pytest plugin](https://pypi.org/project/pytest-playwright/))
```shell
pip install pytest-playwright
```

```shell
playwright install
```
4. 설치한 패키지를 확인합니다.
```shell
pip list
```

## 개발 가이드

### Code formatting
black이라는 코드 포매터를 사용하여 파이썬 코드 스타일을 관리합니다.
   ```shell
brew install black
   ```
black 설치 후 프로젝트 내 파일을 대상으로 실행합니다. 
   ```shell
black .
   ```

## 프로젝트 환경 설정 가이드 (pytest.ini)
### 프로젝트 환경 설정
프로젝트의 환경은 pytest.ini 파일에서 설정한다. 이 파일에서 addopts를 통해 브라우저의 모드(headless or headed)나 테스트 실행 속도(slowmo) 등을 조정할 수 있다.

## 테스트 실행 방법
pytest.ini에서 필요한 환경을 설정한 후 pytest 명령어를 입력한다. pytest만 입력 시 전체 테스트가 실행되고, 파일 이름을 함께 입력하면 해당 파일만 실행한다.
```shell
pytest
```
```shell
pytest test_scripts/test_place_order.py
```

---
# 프로젝트 개요
이 프로젝트는 Playwright와 pytest를 활용하여 사용자가 웹 이커머스에 가입하여 상품을 검색하고 구매하는 메인 비즈니스 플로우를 자동화합니다. Python3을 기반으로 하며, UI 자동화 프레임워크로써 playwright를, 테스트 실행을 위해 pytest를 사용합니다.

### pytest-playwright
`pytest-playwright`는 pytest 플러그인 형태로 제공되는 라이브러리입니다. Playwright와 pytest를 결합하여 테스트 작성과 실행을 간소화하는 도구입니다. 
Playwright의 브라우저 객체 및 페이지 객체를 제공하는 Fixture(`page`, `context`, `browser` 등)를 자동으로 생성합니다. 브라우저를 직접 생성하고 닫는 코드를 작성할 필요 없이 테스트에만 집중할 수 있습니다.

### 프로젝트 구조
```text
project/
├── page_objects/
│   ├── locators/
│   │   ├── common_locators.py      # 로그인 버튼, 헤더 버튼 등 레이아웃 공통 로케이터 정의
│   │   ├── products_locators.py    # 상품 검색, 구매 등과 관련 페이지 로케이터 정의
│   │   ├── users_locators.py       # 회원 가입 및 계정 관련 페이지 로케이터 정의
│   ├── path.py                     # 페이지 URL 경로 관리
├── test_scripts/
│   ├── account
│   │   ├── conftest.py             # 로그인 및 계정 생성 관련 헬퍼 함수 정의
│   │   ├── test_signin.py          # 로그인 테스트 스크립트
│   │   ├── test_signup.py          # 계정 생성 테스트 스크립트
│   ├── product
│   │   ├── conftest.py             # 상품 검색, 담기, 구매 관련 헬퍼 함수 정의
│   │   ├── test_add_to_cart.py     # 상품을 장바구니에 담는 테스트 스크립트
│   │   ├── test_place_order.py     # 상품을 구매하는 테스트 스크립트
│   │   ├── test_search_items.py    # 상품을 검색하는 테스트 스크립트
├── pytest.ini                      # pytest 설정 파일
```

### 로케이터
로케이터는 페이지 객체 모델(Page Object Model)을 기반으로 테스트 코드와 로케이터를 분리하여 체계적으로 관리할 수 있도록 했습니다.
로케이터를 클래스로 구성하여 테스트 코드와 로케이터가 분리합니다. 
이로써 로케이터 관리가 간편해지고, 재사용성 및 코드 가독성이 좋아지기 때문에 협업과 유지보수에 유리합니다.

로케이터는 해당 다음과 같은 컨벤션으로 작성합니다:

`element의_이름_또는_기능` + `__` + `element의_유형`

더블 언더스코어(`__`)로 요소의 이름과 유형을 구분합니다. 띄어쓰기는 언더스코어(`_`)를 이용합니다. 

```text
class SignIn:
    def __init__(self, page: Page):
        self.page = page
        self.email_input = page.locator("[data-qa='login-email']")
```

### **경로 관리**
`path.py` 파일에서 각 페이지의 URL 경로를 정의하여 경로 관리를 단순화합니다. 
```shell
class Path:
    BASE_URL = "https://automationexercise.com/"
```

### 테스트 스크립트
테스트 스크립트는 로그인 및 회원가입 등 계정과 관련한 모듈을 다루는 `account`와 유저가 상품을 검색하고 구매하는 모듈을 다루는 `product`로 나눠집니다. 
재사용되는 헬퍼 함수는 확장성을 고려하여 `conftest.py` 파일에 분리하여 작성합니다.

## Notes
- 본 프로젝트는 사이드 프로젝트로 만들어졌기 때문에 함수 내부에 설명적인 주석을 삽입했습니다. 실제 개발 환경에서는 불필요한 주석은 지양하고, 명확한 함수 및 변수 이름을 통해 의도를 드러내는 것이 바람직합니다.
- 일반적으로는 .env 파일을 .gitignore에 포함시켜 외부에 노출되지 않도록 하지만, 더미 웹사이트 테스트 실행을 위해 임의로 생성된 계정의 이메일과 비밀번호를 포함하고 있습니다. 

---
# 사전 리서치에 대한 기록
## 시나리오

### Happy 시나리오 선정

이커머스에서 기본적으로 검증되어야 하는 시나리오를 선정합니다. 

- 사용자 로그인 및 계정 관리
    - 신규 회원가입
    - 로그인 (잘못된 정보로 로그인 시도 포함)
    - 로그아웃
- 상품 검색 및 조회
    - 키워드 검색
    - 카테고리 검색
- 장바구니
    - 리스트에서 장바구니 담기
    - 상세 페이지에서 장바구니 담기
    - 장바구니에서 물건 제거
    - 여러 개의 제품을 장바구니 담기
- 구매하기
    - 제품을 장바구니에 담고 상품 이름, 가격 정보 일치하는지 확인
    - 인보이스 다운로드 및 내용 확인 (URL에 있는 숫자를 가지고 비교)
- 문의하기
    - 첨부파일에 이미지 첨부해서 문의 발송하기.

### Unhappy 시나리오 선정

시스템에서 예상하지 않은 또는 원하지 않는 동작이 발생하는 상황에서도 적절하게 처리되고, 사용자에게 적절한 정보를 제공하는지 확인하는 시나리오 선정한다. 
이 더미 웹사이트에는 아래 시나리오와 관련된 기능이 없어서 구현은 불가하다. 

- 결제 오류: 사용자가 주문 중 결제하려고 할 때, 신용 카드 거부, 결제 시스템 오류 또는 금액 부족 등으로 인해 결제가 실패하는 시나리오
- 상품 재고 부족: 사용자가 특정 상품을 구매하려고 할 때, 해당 상품의 재고가 없어서 주문이 처리되지 않는 시나리오
- 사용자 인증 오류: 사용자가 로그인하거나 주문을 진행하기 위해 필요한 인증 단계에서 오류가 발생하는 시나리오. e.g. 잘못된 비밀번호, 만료된 세션 등으로 인한 오류 등.

### 그 외 시나리오

역시 해당 웹사이트에서 **지원하지 않는 기능**이지만, 추가해 볼만한 시나리오는 다음과 같다.  

- SNS 계정 연동 및 로그인
- 아이디 및 비밀번호 찾기
- 상품 리스트에서 필터(높은 가격순, 낮은 가격순 등) 동작
- 무한 스크롤(혹은 그에 가까운 스크롤링 동작)
- 쿠폰이나 포인트를 사용한 차감 결제
- 주문 내역 조회하기
- 리뷰 작성 후 작성한 리뷰 확인 및 포인트 적립
- 문의하기에 질문 등록 후, 등록한 질문 및 답변 확인
- 구매자가 아닌, 판매자 시점의 시나리오 (마켓 등록 및 수정, 상품 등록 및 수정, 할인 설정, 문의 답변 등)
- 주문 취소 및 환불 신청
- 상품 교환 및 반품 신청

## 라이브러리

최초 요구사항: python을 지원하면서 bdd(behavior driven development) 기법을 쓸 수 있는 방법이면 좋겠다.

- playwright + behave: python을 지원하면서 bdd 방법론을 사용할 수 있어서 이상적으로 보였으나, behave 사용자가 많지 않아 커뮤니티가 그렇게 잘 되어 있지는 않다.
- playwright for python + pytest: bdd 없이, playwright만 python으로 사용해 보는 방향. 독스를 보면 전반적으로 구성이 잘 되어있는 느낌. playwright가 렌더링 이슈를 가지고 있는 웹브라우저에 있어서 최적의 선택이라는 평가. 신문물을 접해볼 기회가 될 것이다. 객체도 메소드도 다 잘 자리잡혀있다.
- selenium + pytest: 업무상으로 구현했던 자동화 프로젝트 라떼와 같은 조합으로, 초기 구축을 해본다는 것에 의미를 둘 수 있다.
- cypress: javascript 기반으로, 유저도 많고 커뮤니티도 크다. 프론트 개발자들이 꽤 추천하는 편인 것 같다. 언어 선택지가 자바스크립트밖에 없지만, 어쨌든 프론트 기반 UI 테스트이니 자바스크립트만 사용할 수 있는 것이 사실 단점은 아니다.

>  playwright for python으로 pytest을 이용하는 방향으로 구축하는 것으로 결정.
> 

## Page Object Pattern

이러한 패턴에는 여러 가지 방법론이 있는데, Playwright와 pytest를 통한 웹 자동화 작업에서는 Page Object Pattern이나 Fluent Interface Pattern이 적절한 선택이라고 한다.  

> 라떼에서 사용해 봤던 Page Object Model을 좀 더 가져가 보는 것으로 결정.
> 

## Type hinting

타입을 나중에 한꺼번에 추가하려면 품이 든다. 타입 힌팅을 초반부터 확실하게 가져가 보는 게 유리할 것이다.


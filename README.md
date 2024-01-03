# playwright-pytest
Demo Automation 커머스의 리그레션 테스트 자동화 프로젝트로 manual QA 자동화를 목표로 한다.
Latte는 python 3.10 기반으로 UI 자동화 프레임워크로써 playwright, 테스트 실행을 위해 pytest 프레임워크를 사용한다.  

## 실행 전 초기 설정 가이드 (iTerm 등 터미널 환경에서 실행)
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
라떼 프로젝트의 환경은 pytest.ini 파일에서 설정한다.
testpaths에서 테스트할 영역을 지정할 수 있다. default는 step_definitions로 테스트 스크립트 폴더 전체를 가리키고 있다.

### Dash
dash-url를 통해 로컬 호스트에서 실행시킬지 원격 서버로 실행시킬지 설정한다.
로컬 호스트로 실행시 `http://localhost:9000/`, 원격 서버에 접속 시 `https://dashboard-stagingqa.buzzvil.com/` 를 사용한다.
dash-username에는 staff 계정이 필요하고 해당 권한을 가진 `autoTest@buzzvil.com` 계정을 사용할 수 있다.
dash-advertiser-username에는 테스트용 광고주 계정이 필요하고 `advTest@buzzvil.com` 계정을 사용할 수 있다.

## 테스트 실행 방법 들여다보기
사전 조건: 가상 환경이 활성화되어 있어야 한다.

테스트 결과를 전송하지 않고 로컬에서 자동화 스크립트 실행 결과만 확인하게 될 경우 아래 순서를 따른다.
1. pytest.ini에서 dash를 로컬 호스트로 띄우도록 설정한 경우 dash를 먼저 실행시킨다. (명령어는 dash 프로젝트 설정 후에 터미널에서 `API=STAGINGQA npm run dev` 이고 클로닝 및 초기 설정은 [dash readme](https://github.com/Buzzvil/dash#readme) 를 참고한다.)
2. pytest.ini에 dash 로그인 정보가 입력되어 있는지 확인한 후 터미널 latte 프로젝트 root 경로에서 pytest를 입력한다.
   ```shell
   pytest
   ```
3. pytest marker 기능을 이용해 시나리오 파일(.feature)에 표시된 @로 테스트 범위를 지정할 수 있다.
   예를 들어, 애드그룹의 display타입에서 report가 아닌 시나리오를 테스트하고 싶은 경우, adgroup, display, report 태그를 이용해 아래와 같이 범위를 지정할 수 있다.
   ```shell
   pytest -m "adgroup and display and not report"
   ```
4. pytest-html 플러그인을 통해 테스트 결과를 HTML report 형식으로 생성할 수 있다.
   ```shell
   pytest --html=report.html --self-contained-html
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


### 프로젝트 진행 순서
테스트 시나리오에 해당하는 .feature 파일을 features 폴더 아래 작성 후 대응하는 테스트 스트립트를 step_definitions 폴더 아래 .py 파일로 작성한다.
1. feature 파일은 given, when, then 형식으로 작성하며, 테스트 데이터는 examples에, 한 feature 파일 내 테스트 시나리오 간 공통으로 사용되는 given은 background에 작성한다.
   최초 작성시에는 @regression @to_automate 태그를 시나리오 제목 위에 붙인다. (@to_automate 태그는 conftest.py에서 @skip을 적용해 pytest 실행시에는 무시하게 된다.)
2. step definitions 폴더에 테스트케이스 given, when, then에 따른 자동화 스크립트 작성한다.
   특정 테스트 시나리오 섹션 내에서 공통으로 사용되는 기능은 conftest.py에 fixture로 작성한다. [pytest-bdd 참고](https://readthedocs.org/projects/pytest-bdd/)


### Trouble-shooting
위 과정에서 에러가 발생할 경우 `pip install -U pip pip-tools` 를 실행해서 `pip`과 `pip-tools` 버전을 동시에 최신으로 맞춘다.
보통의 경우 두 패키지의 버전 중 하나만 최신이라서 에러가 발생함

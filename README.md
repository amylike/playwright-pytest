# playwright-pytest
Demo Automation 커머스의 리그레션 테스트 자동화 프로젝트로 manual 리그레션 QA의 큰 축을 대체할 수 있는 자동화를 목표로 한다.
playwright-pytest는 python 3.10 기반으로 UI 자동화 프레임워크로써 playwright를, 테스트 실행을 위해 pytest 프레임워크를 사용한다.

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


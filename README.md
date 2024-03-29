# 소비내역 기록 및 관리 API

</br></br>


## API 테스트 케이스

> https://magnificent-trout-789.notion.site/API-baa22472034b4f58a9079ee221f4939e

</br></br>


## 개발 과정에서 고려한 부분

### REST API

1. REST Protocol (Uniform Interface, Client/Server 분리, Stateless, Cacheable, Layered System, Code on Demand)
2. URL 네이밍 규칙 (명사, 소문자, 복수형, 구분자는 "-", 파일 확장자 미포함)
3. url의 마지막에 /를 포함하지 않는다는 네이밍 규칙도 있지만 url의 마지막에 /를 포함하는 django의 네이밍 규칙이 선행됨.

### Pythonic

1. 파이썬의 고유한 메커니즘을 따르는 코드 작성
2. 짧고 이해하기 쉬운 코드

### 요구사항 구현

1. 요구사항 분석을 통한 요구 의도 파악
2. 요구사항에 없지만 고객에게 필요할 것으로 생각되는 것 구현

### Details

1. 개발의 편의와 효율을 생각한 디테일 </br>
ex. 복제 API 개발 시 클라이언트에서 data를 전송하지 않아도, 자동으로 해당 instance의 정보 가져와서 복제되게 만듦.

</br></br>


## 개발 과정에서 배운 점

### MySQL

5.7 버전 설치와 설정에 애를 먹었다. server start에서 계속된 오류가 발생해, 삭제와 설치를 반복하다가 err 파일과 log 파일의 이름에 문제가 있음을 알게 되었다. err 파일과 log 파일의 이름은 노트북의 이름을 자동으로 가져오는데, 내 노트북의 이름에 이모티콘이 들어가 있어 인코딩 오류가 발생한 것이다. 이전에 다뤄본 적이 없는 것이라 시간이 적지 않게 들었다.

### Login & Logout 직접 구현

이전에는 dj-auth 등 authentication 라이브러리를 사용해 login, logout을 구현했다. 이번 기회에 직접 login과 logout을 구현하며 그 작동방식에 대한 이해를 높일 수 있었다.

### signing 모듈

임시 단축 url을 출력하는 API를 구현하며 url data의 인코딩과 디코딩을 편리하게 도와주고, 필요에 따라 만료기간(expirated date) 확인까지 도와주는 django.core의 signing 모듈을 사용했다. documentation를 보니 활용도가 높은 모듈로 생각된다.
</br>
> documentation link</br>
https://docs.djangoproject.com/en/4.1/topics/signing/

</br></br>

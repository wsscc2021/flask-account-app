# About
Python 언어 자체를 공부하고 Web-Application의 Backend개발 경험을 쌓기 위해서 계정 관리, 인증 등을 수행하는 어플리케이션을 만들어 나가고자 합니다.
처음엔 기능 위주의 개발이 진행되겠지만, 공부를 해가며 클라우드 기술과 접목 시켜 완성도 높은 산출물을 만들어내는 것이 목표입니다.
(예를 들어 로그 시스템 구축, 미들웨어 튜닝, 컨테이너라이징, 운영환경 별 설정 구분, 배포 자동화 등이 있습니다.)

# Skills Stack

공부의 큰 흐름을 제시하고 리마인드하기 위해 사용하는 기술 스택을 큼지막히 정리합니다. 자세한 설정과 원리는 별도의 글로 정리하겠습니다.

## Flask Structure
Micro Framework인 Flask는 Django처럼 어플리케이션 구조가 짜여져 있지 않습니다. 그렇기 때문에 Flask를 사용하는 개발자는 어플리케이션 구조를 만들어 관리해야합니다.
대부분 체계적인 구조화가 필요한 경우 다른 개발자 혹은 미래의 자신이 원하는 요소를 쉽게 찾을 수 있도록 직관적이고 보편적인 방법으로 설계해야합니다.
저는 아래와 같은 방식으로 구조화하였습니다.
```
├── app
│   ├── __init__.py       # create_app() 함수를 포함하는 파일입니다. Flask Instance를 생성합니다.
│   ├── models            # ORM Object들을 포함하는 디렉터리입니다.
│   │   └── __init__.py
│   └── services          # 실제 Business logic을 수행하는 파일들을 포함하는 디렉터리입니다.
│       ├── __init__.py
│       ├── account.py
│       └── auth.py
├── config.py  # DEBUG_MODE, DB주소 등의 구성을 관리하는 파일입니다. 이는 어플리케이션의 로직과는 무관합니다.
└── run.py     # 어플리케이션을 실행하는 역할만을 수행하는 파일입니다.
```

## Flask Blueprint
Blueprint는 Large Application에서 Component를 모듈화하여 체계적으로 구조화하는 것을 도와주는 기능입니다.
일반적으로 규모가 큰 어플리케이션에서 사용하여 구조화하는 데 사용하고, 규모가 작은 어플리케이션은 오히려 복잡성을 증가시킬 수 있습니다.
하지만, 개인적으로는 규모가 작은 어플리케이션에서도 기능의 역할을 명확하게 구분지을 수 있어서 충분히 사용해도 좋을 것 같다는 생각이 듭니다. https://flask.palletsprojects.com/en/2.0.x/blueprints/

## Flask RESTx
API를 생성하는 데 있어서 보편적으로 많이 사용되고 있고, 리소스와 행동을 직관적으로 표현할 수 있는 REST 형식으로 API를 개발하고자 합니다.
(그 외에 전송 바이트 크기를 최소화하는 직렬화 방식(ProtocolBuffer)을 사용하는 `grpc`, 여러 리소스를 한번의 요청으로 받아오는 `GraphQL` 등의 API 형식이 있습니다.)
Flask-RestX 를 사용하여 직관적으로 REST API를 개발할 수 있습니다. https://flask-restx.readthedocs.io/en/latest/

## Flask SQLAlchemy
프로그래밍 언어의 Object와 같은 방식으로 SQL문을 Handling할 수 있도록 ORM을 사용합니다. 그리고 ORM 기능을 수행하는 SQLAlchemy를 사용합니다.
특히 Flask-SQLAlchemy를 사용하면 일반 SQLAlchemy보다 engine을 생성, session 관리를 간단하게 할 수 있습니다. https://flask-sqlalchemy.palletsprojects.com/en/2.x/

## JWT (Json Web Token)
사용자를 식별하는 용도로 사용되는 Session, Cookie, Token방식 중 Token방식을 사용하고, 사용자 인증에 필요한 정보를 토큰 자체에 포함하고 있는 JWT를 사용합니다.
Session 방식을 사용하여 Redis를 사용해보는 시나리오도 공부를 하는 측면에서 도움이 될 듯 합니다. 하지만 우선 JWT를 사용하는 방식으로 구현해보겠습니다. http://www.opennaru.com/opennaru-blog/jwt-json-web-token/
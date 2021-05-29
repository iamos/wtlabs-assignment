# Readme

## Precondition

실행시 Docker와 Docker-compose 가 필요합니다.

```bash
$docker --version
Docker version 20.10.6, build 370c289

$docker-compose --version
docker-compose version 1.29.1, build c34c88b2
```

## 실행 방법

0. **요약**

    `docker-compose build && docker-compose up`

1. Docker 이미지 빌드

    `docker-compose.yaml`이 있는 디렉토리에서 `$docker-compose build`를 수행해주세요.

    ```bash
    $docker-compose build

    postgres uses an image, skipping
    Building api
    [+] Building 2.6s (12/12) FINISHED
    ...                                            0.0s
    => => naming to docker.io/wantedlab_backend/api:latest
    ```

2. Docker 컨테이너 실행

    `$docker-compose up` 커맨드를 수행하면 다음과 같이 `postgres`, `api` 컨테이너가 차례로 실행됩니다. (컨테이너 생성 순서가 중요합니다.)

    `api`가 먼저 실행된 후 컨테이너가 종료된다면 `$docker-compose up`을 다시 수행해주세요.

    ```bash
    $docker-compose up

    Creating network "wantedlabs_backend_default" with the default driver
    Creating wantedlabs_backend_postgres_1 ... done
    Creating wantedlabs_backend_api_1      ... done
    Attaching to wantedlabs_backend_postgres_1, wantedlabs_backend_api_1
    ...
    postgres_1  | 2021-05-27 08:39:57.295 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
    postgres_1  | 2021-05-27 08:39:57.295 UTC [1] LOG:  listening on IPv6 address "::", port 5432
    postgres_1  | 2021-05-27 08:39:57.298 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
    postgres_1  | 2021-05-27 08:39:57.302 UTC [49] LOG:  database system was shut down at 2021-05-27 08:39:57 UTC
    postgres_1  | 2021-05-27 08:39:57.306 UTC [1] LOG:  database system is ready to accept connections
    api_1       | [2021-05-27 17:39:58 +0900] [1] [INFO] Starting gunicorn 20.1.0
    api_1       | [2021-05-27 17:39:58 +0900] [1] [INFO] Listening at: http://0.0.0.0:8000 (1)
    api_1       | [2021-05-27 17:39:58 +0900] [1] [INFO] Using worker: sync
    api_1       | [2021-05-27 17:39:58 +0900] [7] [INFO] Booting worker with pid: 7
    api_1       | init_database()
    ```

## Database 설계

1. Company Table

    실제로 회사명 검색을 위한 인덱싱은 별도의 데이터(ElasticSearch 등)로 관리하는게 맞지만, 프로젝트의 간소성을 위해 Text Field로 구현했습니다.

    `StringColumn.contains()` 를 사용해 회사명 자동검색 API를 구현했습니다.
    | | id (INT)| name (TEXT)| locale_name (JSONB)|
    |-|-|-|-|
    | 설명 | Primary key | 검색을 위한 string | 다국어 지원을 위한 필드|
    | 예시 | 1 | "원티드랩, Wantedlab" | {"en": "Wantedlab","ko": "원티드랩"} |

2. Tag Table

    태그가 의미하는 바는 갖지만 그것을 표현하는 언어가 다른 데이터셋을 표현하기 위해 `JSONB type`을 사용했습니다.
    | | id (INT)| locale_tag (JSONB)|
    |-|-|-|
    | 설명 | Primary Key | 다국어 지원을 위한 필드 |
    | 예시 | 1 | { "en": "tag_1", "jp": "タグ_1", "ko": "태그_1"} |

3. CompanyTag Table

    Company-Tag M:N relation을 표현하기 위한 Table입니다.
    | | id (INT) | company_id (INT) | tag_id (INT) |
    |-|-|-|-|
    | 설명 | Primary Key | Foreign key | Foreign key |
    | 예시 | 156 | 64 | 28 |

## API 문서

API는 쿼리스트링에 `locale`(언어)을 받습니다.

`locale`과 일치하는 데이터가 없다면 한국어, 영어, 일본어중 데이터가 있는  값을 먼저 보여줍니다.

```json
# [GET] tag?q=tag_4&locale=en
{
    "company.id": 65,
    "company.name": "KFC Korea",
    "company.locale_name": {
        "ko": "KFC Korea"
    }
}
```
위 예시는 `locale=en`을 요청했지만 결과인 `"KFC KOREA"`는 `locale_name.en`대신 `locale_name.ko`를 결과로 내보냅니다.

### 회사명 자동완성

`GET localhost:5000/company?q=<query>&locale=<locale>`

locale과 일치하는 회사 이름을 최우선으로 보여줍니다.

```bash
Request
curl --request GET \
  --url 'http://localhost:5000/company?q=G&locale=jp'

Response
HTTP_200,
{
  "q": "G",
  "locale": "jp",
  "result": [
    {
      "company.id": 32,
      "company.name": "Luna Marketing Group",
      "company.locale_name": {
        "en": "Luna Marketing Group"
      }
    },
    ...
  ]
}
```

### 태그명으로 회사 검색

`GET http://localhost:5000/tag?q=<tag>&locale=<locale>`

`locale`과 일치하는 회사 이름을 최우선으로 보여줍니다. 그렇지 않으면 `ko`, `en`, `jp` 순으로 이름을 표시합니다.

```bash
Request
curl --request GET \
  --url 'http://localhost:5000/tag?q=tag_4&locale=en'

Response
HTTP_200,
{
  "q": "tag_4",
  "locale": "en",
  "result": [
    {
      "company.id": 64,
      "company.name": "GEOCM Co.",
      "company.locale_name": {
        "en": "GEOCM Co.",
        "jp": "GEOCM",
        "ko": "지오코리아(페루관광청)"
      }
    },
    {
      "company.id": 65,
      "company.name": "KFC Korea",
      "company.locale_name": {
        "ko": "KFC Korea"
      }
    },
    ...
  ]
}
```

### 회사 태그 정보 추가

`PUT localhost:5000/companytag`

Request Body에 JSON으로 다음과 같이 요청합니다.

한번에 여러 태그를 추가할 수 있도록 array로 받아서 새로 추가된 태그만 저장합니다.


```bash
Request
curl --request PUT \
  --url http://localhost:5000/companytag \
  --header 'Content-Type: application/json' \
  --data '{
    "company_id": 6,
    "tag_id": [20, 21, 22]
}'

Response
HTTP_200; 성공
HTTP_500; database commit중 에러
```

### 회사 태그 정보 삭제

`DELETE localhost:5000/companytag`

Request Body에 JSON으로 다음과 같이 요청합니다.

한번에 하나의 태그만 삭제하도록 구현했습니다.

```bash
Request
curl --request DELETE \
  --url http://localhost:5000/companytag \
  --header 'Content-Type: application/json' \
  --data '{
    "company_id": 6,
    "tag_id": 22
}'

Reponse
HTTP_204; 삭제 성공
HTTP_404; 없는 태그 지울 때
```

## 기능 명세

* 회사명 자동완성
  * 회사명의 일부만 들어가도 검색이 되어야 합니다.
* 태그명으로 회사 검색
  * 태그로 검색 관련된 회사가 검색되어야 합니다.
  * 다국어로 검색이 가능해야 합니다.
  * 일본어 태그로 검색을 해도 한국 회사가 노출이 되어야 합니다.
  * タグ_4로 검색 했을 때, 원티드랩 회사 정보가 노출이 되어야 합니다.
  * 동일한 회사는 한번만 노출이 되어야합니다.
* 회사 태그 정보 추가
* 회사 태그 정보 삭제

## 제약사항

* Python flask로 개발해야 합니다.
* 별도의 화면(frontend)는 필요없습니다. (api만 개발하시면 됩니다.)
* ORM 사용해야 합니다.
* 결과는 JSON 형식이어야 합니다.
* database는 자유입니다.
* database table 갯수는 제한없습니다.
* 요구사항에 맞게 자유롭게 개발하시면 됩니다.
* 필요한 조건이 있다면 추가하셔도 좋습니다.
* 전체 기능을 완성하지 못해도 괜찮습니다.
* Docker로 개발하면 가산점이 있습니다.
* Test code가 있으면 가산점이 있습니다.
* 다국어에 대한 확장성을 고려해야 합니다.

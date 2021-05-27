# Readme

## Precondition

실행시 Docker와 Docker-compose 가 필요합니다.

```bash
$docker --version
Docker version 20.10.6, build 370c289

$docker-compose --version
docker-compose version 1.29.1, build c34c88b2
```

실행 방법
`$docker-compose build`

```bash
$docker-compose build

postgres uses an image, skipping
Building api
[+] Building 2.6s (12/12) FINISHED
 => [internal] load build definition from api.Dockerfile                                                                                     0.0s
 => => transferring dockerfile: 41B                                                                                                          0.0s
 => [internal] load .dockerignore                                                                                                            0.0s
 => => transferring context: 2B                                                                                                              0.0s
 => [internal] load metadata for docker.io/library/python:3.9.5-buster                                                                       2.4s
 => [auth] library/python:pull token for registry-1.docker.io                                                                                0.0s
 => [1/6] FROM docker.io/library/python:3.9.5-buster@sha256:d9dbd09e20abe942d84fef5b736f5ed7ee638e3204e0c0b14345d3754026156d                 0.0s
 => => resolve docker.io/library/python:3.9.5-buster@sha256:d9dbd09e20abe942d84fef5b736f5ed7ee638e3204e0c0b14345d3754026156d                 0.0s
 => [internal] load build context                                                                                                            0.0s
 => => transferring context: 2.96kB                                                                                                          0.0s
 => CACHED [2/6] RUN ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime && echo Asia/Seoul > /etc/timezone && date                        0.0s
 => CACHED [3/6] COPY requirements.txt /wantedlab_backend/requirements.txt                                                                   0.0s
 => CACHED [4/6] RUN pip3 install -r /wantedlab_backend/requirements.txt                                                                     0.0s
 => [5/6] COPY sources /wantedlab_backend/sources                                                                                            0.0s
 => [6/6] WORKDIR /wantedlab_backend                                                                                                         0.0s
 => exporting to image                                                                                                                       0.0s
 => => exporting layers                                                                                                                      0.0s
 => => writing image sha256:dd1f41a4d5234924786fb5dc6113a920b99192e1a4ab8dee37f843568f77fa61                                                 0.0s
 => => naming to docker.io/wantedlab_backend/api:latest
```

`$ docker-compose up`

```bash
$docker-compose up

Creating network "wantedlabs_backend_default" with the default driver
Creating wantedlabs_backend_postgres_1 ... done
Creating wantedlabs_backend_api_1      ... done
Attaching to wantedlabs_backend_postgres_1, wantedlabs_backend_api_1
postgres_1  | The files belonging to this database system will be owned by user "postgres".
postgres_1  | This user must also own the server process.
postgres_1  |
postgres_1  | The database cluster will be initialized with locale "en_US.utf8".
postgres_1  | The default database encoding has accordingly been set to "UTF8".
postgres_1  | The default text search configuration will be set to "english".
postgres_1  |
postgres_1  | Data page checksums are disabled.
postgres_1  |
postgres_1  | fixing permissions on existing directory /var/lib/postgresql/data ... ok
postgres_1  | creating subdirectories ... ok
postgres_1  | selecting dynamic shared memory implementation ... posix
postgres_1  | selecting default max_connections ... 100
postgres_1  | selecting default shared_buffers ... 128MB
postgres_1  | selecting default time zone ... UTC
postgres_1  | creating configuration files ... ok
postgres_1  | running bootstrap script ... ok
postgres_1  | performing post-bootstrap initialization ... sh: locale: not found
postgres_1  | 2021-05-27 08:39:56.122 UTC [30] WARNING:  no usable system locales were found
postgres_1  | ok
postgres_1  | syncing data to disk ... initdb: warning: enabling "trust" authentication for local connections
postgres_1  | You can change this by editing pg_hba.conf or using the option -A, or
postgres_1  | --auth-local and --auth-host, the next time you run initdb.
postgres_1  | ok
postgres_1  |
postgres_1  |
postgres_1  | Success. You can now start the database server using:
postgres_1  |
postgres_1  |     pg_ctl -D /var/lib/postgresql/data -l logfile start
postgres_1  |
postgres_1  | waiting for server to start....2021-05-27 08:39:56.960 UTC [35] LOG:  starting PostgreSQL 13.3 on x86_64-pc-linux-musl, compiled by gcc (Alpine 10.2.1_pre1) 10.2.1 20201203, 64-bit
postgres_1  | 2021-05-27 08:39:56.961 UTC [35] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
postgres_1  | 2021-05-27 08:39:56.966 UTC [36] LOG:  database system was shut down at 2021-05-27 08:39:56 UTC
postgres_1  | 2021-05-27 08:39:56.969 UTC [35] LOG:  database system is ready to accept connections
postgres_1  |  done
postgres_1  | server started
postgres_1  | CREATE DATABASE
postgres_1  |
postgres_1  |
postgres_1  | /usr/local/bin/docker-entrypoint.sh: ignoring /docker-entrypoint-initdb.d/*
postgres_1  |
postgres_1  | 2021-05-27 08:39:57.179 UTC [35] LOG:  received fast shutdown request
postgres_1  | waiting for server to shut down....2021-05-27 08:39:57.182 UTC [35] LOG:  aborting any active transactions
postgres_1  | 2021-05-27 08:39:57.183 UTC [35] LOG:  background worker "logical replication launcher" (PID 42) exited with exit code 1
postgres_1  | 2021-05-27 08:39:57.184 UTC [37] LOG:  shutting down
postgres_1  | 2021-05-27 08:39:57.193 UTC [35] LOG:  database system is shut down
postgres_1  |  done
postgres_1  | server stopped
postgres_1  |
postgres_1  | PostgreSQL init process complete; ready for start up.
postgres_1  |
postgres_1  | 2021-05-27 08:39:57.295 UTC [1] LOG:  starting PostgreSQL 13.3 on x86_64-pc-linux-musl, compiled by gcc (Alpine 10.2.1_pre1) 10.2.1 20201203, 64-bit
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
api_1       | 	ADD Company('원티드랩')
api_1       | 	ADD Company('원트')
api_1       | 	ADD Tag(4)
api_1       | 	ADD Tag(16)
api_1       | 	ADD Tag(20)
api_1       | 	ADD CompanyTag(1,4)
api_1       | 	ADD CompanyTag(2,4)
api_1       | 	ADD CompanyTag(1,16)
```

## Database 설계

1. Company
2. Tag
3. CompanyTag

## API 문서


## 기능 명세

회사명 자동완성
    회사명의 일부만 들어가도 검색이 되어야 합니다.
태그명으로 회사 검색
    태그로 검색 관련된 회사가 검색되어야 합니다.
    다국어로 검색이 가능해야 합니다.
    일본어 태그로 검색을 해도 한국 회사가 노출이 되어야 합니다.
    タグ_4로 검색 했을 때, 원티드랩 회사 정보가 노출이 되어야 합니다.
    동일한 회사는 한번만 노출이 되어야합니다.
회사 태그 정보 추가
회사 태그 정보 삭제

## 제약사항

Python flask로 개발해야 합니다.
별도의 화면(frontend)는 필요없습니다. (api만 개발하시면 됩니다.)
ORM 사용해야 합니다.
결과는 JSON 형식이어야 합니다.
database는 자유입니다.
database table 갯수는 제한없습니다.
요구사항에 맞게 자유롭게 개발하시면 됩니다.
필요한 조건이 있다면 추가하셔도 좋습니다.
전체 기능을 완성하지 못해도 괜찮습니다.
Docker로 개발하면 가산점이 있습니다.
Test code가 있으면 가산점이 있습니다.
다국어에 대한 확장성을 고려해야 합니다.

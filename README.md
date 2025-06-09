
### to run without docker
<pre><code>uvicorn src.main:app --reload</code></pre>


### with docker

## 🚀 Как запустить проект (после клонирования)

1. Установи Docker и Docker Compose:
   - [Установка Docker Desktop](https://www.docker.com/products/docker-desktop/)

2. Клонируй репозиторий:
```bash
git clone https://github.com/alibekn6/fastapi-hw
cd fastapi-hw

docker compose up --build
```

# Backend home work 1

## 🥉 Basic Level

### Tasks

- [x] Create a CRUD for your own application
- [x] Create and connect a front(IOS/Web) for your own application(take data from backend)

## 🥈 Medium Level

### Tasks

- [x] Create a dockerfile for your own application(FastAPI)
- [x] Connect your application to database(Postgresql)
- [ ] Connect CI/CD by Github Actions

## 🥇 Hard Level

### Tasks

- [x] Create JWT authentication and authorization
- [x] Create a docker compose file for your own application(FastAPI, Postgres)
- [x] Create Secured endpoints
  - [x] `/me` - get user info
  - [x] `/create_task` - create a task
  - [x] `/get_tasks` - get all my tasks
  - .etc

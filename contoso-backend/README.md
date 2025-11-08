# Contoso 费用报销系统

欢迎来到 Contoso 费用报销系统项目！这是一个全栈 Web 应用，包括一个使用 FastAPI 构建的 Python 后端和一个使用 Modern.js (React) 构建的前端。

- **`contoso-backend/`**: 后端 API 服务，负责处理业务逻辑、用户认证和数据存储。
- **`contoso-frontend/`**: 前端 Web 应用，提供用户交互界面。

---

## 快速开始：使用 Docker Compose (推荐)

这是启动完整本地开发环境最简单、最快捷的方式。它会同时启动后端 API、前端应用以及一个 PostgreSQL 数据库。

### 前提条件

- [Docker](https://www.docker.com/products/docker-desktop/) 已安装并正在运行。

### 设置步骤

**1. 配置后端环境变量**

`docker-compose` 需要一些环境变量来连接数据库和配置应用。

首先，复制示例 env 文件：

# 在项目根目录运行
cp contoso-backend/.env.db.example contoso-backend/.env.db
cp contoso-backend/.env.example contoso-backend/.env然后，你可以根据需要修改 `contoso-backend/.env.db` 和 `contoso-backend/.env` 里的值，但默认配置已经可以工作了。

**2. 启动服务**

在项目根目录运行以下命令：

docker compose up --build- `--build` 标志会确保在启动前构建最新的 Docker 镜像。
- 首次启动可能需要一些时间来下载镜像和安装依赖。

启动成功后，你可以通过以下地址访问应用：

- **前端应用**: [http://localhost:8080](http://localhost:8080)
- **后端 API 文档 (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)

**3. 停止服务**

当你完成开发时，按 `Ctrl + C`，然后运行以下命令来停止并移除容器：

docker compose down---

## 手动本地开发

如果你希望独立运行前端或后端服务，请按照以下指南操作。

### 运行后端 (FastAPI)

后端使用 [uv](https://github.com/astral-sh/uv) 进行包和环境管理。

**1. 环境设置**

进入后端目录，使用 `uv` 创建并激活虚拟环境，然后安装依赖。

# 进入后端目录
cd contoso-backend

# 创建并激活虚拟环境
uv venv
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
# source .venv/bin/activate  # macOS / Linux / Git Bash

# 使用 uv sync 安装依赖
uv sync**2. 配置环境变量**

在 `contoso-backend` 目录下创建一个 `.env` 文件，并填入必要的配置。你可以从 `.env.example` 复制。

# 至少需要包含以下内容
DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/dbname"
SECRET_KEY="your-secret-key"
ACCESS_TOKEN_EXPIRE_MINUTES="60"> **提示**: 你需要一个本地运行的 PostgreSQL 数据库，并将连接信息填入 `DATABASE_URL`。使用 Docker 是运行数据库的最简单方式。

**3. 运行开发服务器**

uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000### 运行前端 (Modern.js)

前端使用 `pnpm` 作为包管理器。

**1. 环境设置**

进入前端目录并安装依赖。

# 进入前端目录
cd contoso-frontend

# 安装依赖
pnpm install**2. 配置环境变量**

在 `contoso-frontend` 目录下创建一个 `.env` 文件，指定后端 API 的地址。

# .env 文件内容
API_BASE_URL=http://localhost:8000**3. 运行开发服务器**

pnpm dev服务器启动后，你可以在 [http://localhost:8080](http://localhost:8080) 访问前端页面。

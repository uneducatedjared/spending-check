# Contoso Backend

这个仓库包含 Contoso 应用的后端服务（FastAPI）。此文档概述项目架构、主要目录、运行方式、环境变量、认证流程及常见故障排查建议。

## 目录结构（简要）

- `pyproject.toml` - 项目依赖与元数据。
- `src/` - 后端源码根目录。
  - `main.py` - FastAPI 应用入口，包含中间件、路由注册和启动时行为（例如自动创建 DB 表）。
  - `config/`
    - `config.py` - 配置/环境变量读取（pydantic settings）。
    - `database.py` - SQLAlchemy 异步 engine / session 配置。
  - `endpoints/` - 路由声明（FastAPI routers）：
    - `auth.py` - 认证/注册相关接口。
    - `tickets.py` - 报销 Ticket 相关接口。
    - `employees.py` - 员工管理接口（仅雇主可见）。
  - `models/` - SQLAlchemy ORM 模型定义（User, Ticket 等）。
  - `repository/` - 与 DB 的 CRUD 封装（async SQLAlchemy session）。
  - `schemas/` - Pydantic 请求/响应模型（校验层）。
  - `services/` - 业务逻辑（例如 `auth.py`, `user_service.py`, ticket/employee 服务），将路由和 repository 解耦。
  - `utils/` - 通用工具（例如统一响应格式）。

## 高层架构与设计原则

- 路由（endpoints）仅负责 HTTP 层：解析请求、返回统一响应、捕获异常。业务逻辑放在 `services` 中。
- 数据访问集中在 `repository/crud.py`，使用 SQLAlchemy 的 `AsyncSession`。
- 配置使用 pydantic settings（在 `config/config.py`），通过环境变量注入运行时配置（数据库 URL、密钥等）。
- 认证使用 JWT（`python-jose`），密码使用 Passlib + Argon2 存储与验证。
- 错误处理：FastAPI 的 `HTTPException` 被统一异常处理器拦截并返回统一结构（见 `main.py` 的 handler）。

## 关键流程 — 注册 / 登录（register_or_login）

1. 前端提交 `email` 和 `password`（本项目前端使用单按钮“Login / Register”流程）：
   - 后端首先查找用户（通过 `crud.get_user_by_email`）。
   - 如果用户存在：
     - 检查 `is_suspended`，若被封禁返回 403。
     - 使用 `passlib` 验证密码；验证失败返回 400（错误密码）。
     - 验证通过则生成 JWT 并返回（`access_token` + 用户信息）。
   - 如果用户不存在：
     - 服务期望前端在第二步提供 `username` 和 `role`（`employee` 或 `employer`）。
     - 如果 `username` 或 `role` 缺失，服务会返回 404（`User not found`），提示前端收集更多信息。
     - 一旦收集到 `username` 和 `role`，后端会对密码进行哈希（Argon2 via Passlib），创建用户并返回 token。

> 设计理由：后端不允许把 `username` 或 `role` 写为 NULL（数据库列为 NOT NULL）。因此，若缺少这些注册字段，应在后端明确拒绝并要求前端补齐信息，避免数据库完整性错误。

## 配置与运行（开发）

先创建并激活 Python 虚拟环境，安装依赖：

```powershell
cd contoso-backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -e .
```

运行开发服务器（使用 uvicorn）：

```powershell
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

重要环境变量（常见）：
- `DATABASE_URL` - SQLAlchemy/AsyncPG 连接字符串，例如 `postgresql+asyncpg://user:pass@host:5432/dbname`。
- `SECRET_KEY` - 用于 JWT 的签名密钥。
- `ACCESS_TOKEN_EXPIRE_MINUTES` - token 过期时间（分钟）。

这些变量通常在 `config/config.py` 中被读取并封装为 `settings` 对象。

## Docker（生产）

仓库已包含一个示例 `Dockerfile`，用于构建生产镜像。构建并运行示例：

```powershell
docker build -t contoso-backend:latest -f contoso-backend/Dockerfile contoso-backend
docker run -it --rm -p 8000:8000 -e DATABASE_URL="postgresql+asyncpg://user:pass@db:5432/contoso" -e SECRET_KEY="..." contoso-backend:latest
```

推荐使用 `docker-compose` 在本地配合 Postgres 一起运行（我可以为你添加 docker-compose 文件）。

## 数据库与迁移

当前代码在 `startup` 事件中使用 SQLAlchemy 的 `Base.metadata.create_all` 自动创建表（便于快速启动）。如果你计划长期维护或演进 schema，建议引入 Alembic 来做结构化迁移：

- 安装并初始化 Alembic，新建 migration 脚本并在 CI 中执行迁移步骤（或在容器启动时运行 `alembic upgrade head`）。

## 调试与常见问题

- IntegrityError: null value in column "username" - 原因是尝试在没有 `username` 的情况下创建用户（数据库约束）。修复方法：确保前端在注册请求中提供 `username` 和 `role`，或按当前实现让后端返回 404 并由前端收集额外信息后再次提交。
- 连接到数据库失败：检查 `DATABASE_URL` 、网络、Postgres 是否允许连接以及 `libpq-dev` 是否已安装（容器或本地）。
- 密码验证失败：确保密码哈希与验证策略一致（后端使用 Argon2 via Passlib），前端**不应**在客户端重复哈希密码后再发给后端，除非后端期望接收预哈希值。
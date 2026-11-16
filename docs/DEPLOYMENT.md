# 部署说明

## 实际状态

PENDING：未取得 Render 账号权限，环境未配置 RENDER_API_KEY、RAILWAY_TOKEN、FLY_API_TOKEN；实际访问 Render services API 返回 HTTP 401。没有公网地址，也没有把 localhost 记为云部署。没有创建付费资源。

## Render 持久化部署

根目录 render.yaml 是准备好的 Blueprint。它使用 starter 付费实例和 1 GB 持久磁盘，免费临时文件系统不能保证 SQLite 重启持久化。请在 Render 页面确认当时价格。

1. GitHub 上传已完成；若要启用额外部署，再登录 Render 并授权读取指定仓库。
2. 选择 New → Blueprint，选择 address-book-application 仓库，检查配置与费用后创建。
3. 构建命令：`pip install -r requirements.txt`。
4. 启动命令：`waitress-serve --host=0.0.0.0 --port=$PORT --call app:create_app`。
5. 设置 SECRET_KEY 为长期稳定随机值，DATABASE_URL 为 `sqlite:////var/data/contacts.db`。磁盘挂载 `/var/data`；服务首次启动自动建表。Debug 未开启。
6. 使用平台实际分配的 HTTPS 地址，导入示例并验证 CRUD、收藏、多联系方式、搜索、Excel 导入导出。
7. 手动重启服务，再验证记录仍存在。没有做这个步骤就不能宣称持久化部署验收通过。
8. 记录真正的地址、日期和截图到 FINAL_ACCEPTANCE.md 以及博客。

本应用是单用户课程演示，没有身份隔离；公网演示只导入示例联系人。处理真实个人数据应加身份认证或放在受控网络。SQLite 单实例运行，不启动多个独立磁盘副本；备份时应停止写入或使用 SQLite 备份机制。

## 普通云服务器

使用 Python 3.11+ 虚拟环境安装 requirements.txt，以 Waitress 运行，绑定受控接口，经反向代理提供 HTTPS，数据库路径使用绝对持久目录。通过进程管理器设置 SECRET_KEY 和 DATABASE_URL；不要把密钥写进 Git。防火墙只开放必要端口。

生产启动示例（Linux）：

```bash
waitress-serve --host=0.0.0.0 --port=8000 --call app:create_app
```

需在运行环境设置变量，而不是复制一个真实密钥进文档。Windows 本地仍按 README 的 python app.py 启动。

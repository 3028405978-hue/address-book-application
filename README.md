# 青简通讯录 · Address Book Application

EE308FZ Software Engineering 个人 XP 课程项目。Flask + SQLite + 原生中文响应式页面，全部资源本地提供，无 CDN 依赖。

仓库：https://github.com/3028405978-hue/address-book-application

作业：https://bbs.csdn.net/topics/620593436

## 功能

- 新增、详情、编辑、确认删除；姓名必填，服务端校验及操作反馈。
- 姓名、任意电话、任意邮箱的子串搜索；`%` 和 `_` 作为普通字符。
- 收藏、取消收藏及收藏筛选，SQLite 持久化。
- 每位联系人的电话、邮箱、社交账号、地址均可动态增删多条。
- openpyxl 导入导出 `.xlsx`，逐行报告，支持中英文表头。
- 手机布局、空状态、CSRF 校验、HTML 自动转义、Excel 公式安全处理。

## Windows 11 安装与启动

安装 Python 3.11 或更新版本，勾选 Add Python to PATH。解压后进入本目录：

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```

浏览器访问 http://127.0.0.1:5000 。按 Ctrl+C 停止。

PowerShell 无需修改执行策略，直接使用：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

`start_windows.bat` 可在安装好 Python 后双击启动。Linux/macOS：`python3 -m venv .venv`，激活 `.venv/bin/activate` 后使用相同安装和启动命令。

## 数据库

首次启动自动建表，默认数据库为 `instance/contacts.db`，重启不丢失。交付包不附带运行数据库，新安装为空通讯录。导入根目录 `sample_contacts.xlsx` 可得到 5 条明确标注的虚构示例。

备份：停止服务后复制 `instance/contacts.db`。恢复：停止服务后还原该文件。删除该数据库会永久删除本地记录，请先导出备份。结构见 [数据库设计](docs/DATABASE.md)。

## Excel 约定

列顺序：Name、Phones、Emails、Social Accounts、Addresses、Notes、Favorite。每位联系人一行，多值字段使用 JSON 字符串数组，例如 `["00123", "13800000000"]`，保留分号、竖线及换行。手工 Excel 也可使用中英文分号分隔多值；若内容本身有分号请用 JSON。

支持中文表头：姓名、电话/电话号码、邮箱/电子邮箱、社交账号、地址/邮寄地址、备注、收藏/收藏状态。Name/姓名必须存在且不能重复映射同一字段；未知列忽略。收藏接受 True/False、1/0、yes/no、是/否；空值按未收藏。

完全相同的规范化记录（包含备注、收藏、各列表及其顺序）跳过；同名不同信息作为独立新联系人。不是按姓名覆盖。每类重复值去重、空白项去除，序列化后不能超过 Excel 单元格的 32767 个 UTF-16 单元。空行忽略；仅表头文件成功导入 0 条；缺表头或损坏文件拒绝。合法行入库，错误行单独报告；整个工作簿结构错误则回滚。

文件最大 5 MB、解压总大小最大 30 MB、单次最多 10000 数据行。每类联系方式最多 50 条、每条最多 1000 字符，备注最多 10000 字符。电话请使用文本单元格，避免 Excel 在导入前丢失前导零。公式单元格拒绝导入；导出内容明确写成字符串。

## 测试

```bat
python -m pytest -v
python -m compileall .
```

可选覆盖率：`python -m pytest --cov=app --cov=models --cov=routes --cov=services`。

已在 Linux / Python 3.12.14 实测：49 passed，0 failed；后端语句覆盖率 97%。浏览器 12 项检查通过。GitHub hosted Windows/Ubuntu、Python 3.11/3.12 四组 CI 已实际成功，运行链接见 docs/FINAL_DELIVERY.md；不冒充 Windows 11 桌面人工测试。证据见 [测试报告](docs/TEST_REPORT.md)。

## 目录

```text
app.py / config.py / models.py    工厂、配置、数据库模型
routes/                         CRUD、搜索、收藏、文件路由
services/                       输入处理和 Excel 服务
templates/ / static/             中文页面、CSS、JavaScript
tests/                          独立临时数据库测试
sample_contacts.xlsx            五条演示联系人
docs/                           报告、博客、截图、演示视频
.github/workflows/tests.yml      Linux/Windows × Python 3.11/3.12 CI
render.yaml                     持久化 Render 部署配置
```

代码规范：[CODE_STANDARD.md](CODE_STANDARD.md)。远程 main 已成功上传；最新提交数、Release、PR 及部署证据以 [FINAL_ACCEPTANCE.md](docs/FINAL_ACCEPTANCE.md) 为准。

## 配置与部署

默认 Waitress 仅监听 127.0.0.1，Debug 关闭。`DATABASE_URL` 设置数据库 URI；`SECRET_KEY` 可设置稳定随机密钥，不设置时每次进程启动随机生成，旧表单会在重启后失效。生产必须设置稳定环境密钥。

这是单用户本地通讯录，没有登录和用户隔离。公开课程演示只应使用示例数据；实际私人通讯录部署需配置访问认证。公网部署和持久磁盘要求见 [DEPLOYMENT.md](docs/DEPLOYMENT.md)。

## 交付材料

- [个人 CSDN 博客](docs/CSDN_BLOG.md)
- [真实演示 MP4](docs/video/demo.mp4)
- [演示说明](docs/DEMO_SCRIPT.md)
- [XP 实践](docs/XP_PRACTICES.md)
- [提交清单](docs/SUBMISSION_CHECKLIST.md)

作者身份信息、PSP 实际工时、CSDN 发布地址需要本人核实填写。项目由自动化开发助手执行实现与验证；博客为第一人称发布草稿，不能代替本人真实开发经历。

GitHub 文件整理范围见 [UPLOAD_GUIDE.md](docs/UPLOAD_GUIDE.md)。GitHub 写入权限已确认，已通过真实文档 PR 和 Actions 完成发布；未完成的 CSDN 与可选云部署另行保留状态。

正式版本：[v1.0.0 Release](https://github.com/3028405978-hue/address-book-application/releases/tag/v1.0.0) · [下载完整提交 ZIP](https://github.com/3028405978-hue/address-book-application/releases/download/v1.0.0/EE308_Address_Book_Submission_Final.zip) · [已合并 PR #1](https://github.com/3028405978-hue/address-book-application/pull/1) · [四组测试与发布成功](https://github.com/3028405978-hue/address-book-application/actions/runs/43888265296)。发布附件内含精确提交 SHA、数量和新测试日志。

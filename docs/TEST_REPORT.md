# 真实测试报告

验证日期：2026-11-16（北京时间；UTC 日期同为 2026-11-16）。系统 Linux，Python 3.12.14；Flask 3.1.2、Flask-SQLAlchemy 3.1.1、openpyxl 3.1.5、pytest 9.0.2。

## 自动化结果

实际执行命令：

```text
python -m pytest -v --cov=app --cov=models --cov=routes --cov=services --cov-report=term-missing --junitxml=docs/test-results.xml
python -m compileall .
```

49 collected，49 passed，0 failed，本轮最新重跑耗时 3.07 秒。后端 290 条语句，未覆盖 8 条，总覆盖率 97%。compileall 退出码 0。

| 模块 | 覆盖率 |
|---|---:|
| app.py | 95% |
| models.py | 100% |
| routes/contacts.py | 99% |
| routes/favorites.py | 100% |
| services/contact_methods.py | 100% |
| services/excel_service.py | 95% |

覆盖范围：联系人 CRUD、空白/超长姓名、详情、编辑增删方法、子记录删除、姓名/第二电话/第二邮箱搜索、字面通配符、收藏/取消及组合筛选、多种多值联系方式、重建应用后的 SQLite 持久化、空状态、CSRF 拒绝、XSS 转义、错误邮箱、无效编辑保留原值、重复空白规范化、超限上传、不存在 ID、Excel 下载、中文表头、逐行错误、全部字段往返、前导零/分号/竖线/换行、公式字符串安全导出、重复跳过、同名保留、损坏/空/错误扩展名文件、缺失/重复表头、仅表头、公式拒绝、错误数组、错误收藏状态、空行、空表导出、控制字符及字段长度限制。

证据：[pytest-output.txt](pytest-output.txt)、[test-results.xml](test-results.xml)、[compileall-output.txt](compileall-output.txt)。覆盖率统计只针对应用 Python，不包含前端 JS。

## 真实浏览器验证

Playwright + Chromium，运行 Waitress HTTP 服务，独立演示数据库，不使用 pytest 数据库。

12 项通过，0 失败，0 JavaScript 异常。包含从 UI 导入五条示例、真实新增/编辑/动态多值、收藏、第二邮箱搜索、实际文件下载、六条重复重新导入、取消删除及确认删除、390×844 手机首页与表单无横向溢出。完整条目见 [browser-results.json](browser-results.json)。桌面截图宽 1440px。

截图为真实页面；Excel 工作簿预览是从实际下载文件读取数据后渲染的只读预览，不冒充桌面 Excel；11-git-history.png 是标注清楚的本地检查点；新补充的 12-github-history.png、13-github-actions.png 来自真实 GitHub 网页。

初次浏览器断言失败：演示查询 study@example.com 同时命中了示例 lin.study@example.com，属于正确的子串匹配；改用唯一演示地址 su.study@example.com 后完整流程通过。

## 边界与未验证项

本机没有 Windows 11 桌面环境；但 GitHub hosted Windows/Ubuntu、Python 3.11/3.12 四组 CI 已实际成功，不能再写成仅配置。未进行并发负载测试、超大规模地址簿测试或公网端到端验证。可选云部署、GitHub Actions 的真实运行状态见最终验收报告。没有把任何未运行测试写成通过。

## 本轮 CI 证据

已核实 https://github.com/3028405978-hue/address-book-application/actions/runs/43884952886 的四个矩阵任务全部 success，每个任务的安装、pytest、compileall 步骤成功。原始 jobs 响应存入 [verified-initial-jobs.json](ci/verified-initial-jobs.json)，网页见截图 13-github-actions.png。PR 和最终 main 的新运行链接随后更新到 FINAL_DELIVERY.md。

# Address Book Application v1.0.0

本地发布候选说明。正式 GitHub Release 创建状态见 FINAL_ACCEPTANCE.md；本文件存在不表示远程已发布。

## 主要功能

- 中文响应式通讯录，新增、详情、编辑、确认删除与反馈。
- 姓名/全部电话/全部邮箱搜索，收藏切换与筛选。
- 四种联系方式均支持多个值，SQLite 持久化。
- 完整 XLSX 导入导出、中文表头、JSON 多值、重复跳过和逐行错误。
- 独立 SQLite pytest 测试、GitHub Actions 配置、示例 Excel、真实截图和演示 MP4。

## 验证

Linux / Python 3.12.14：49 passed，0 failed，后端语句覆盖率 97%，compileall 成功。Chromium 浏览器 12 项检查通过。Windows CI 尚待真实运行。

## 运行

Python 3.11+：`python -m pip install -r requirements.txt`，`python app.py`，打开 http://127.0.0.1:5000。Windows 完整步骤见 README。

## 已知范围

单用户本地应用；无用户登录、分页或多实例部署。正式 GitHub 上传、PR、Release 和公网部署分别验收，不能用本地测试替代。

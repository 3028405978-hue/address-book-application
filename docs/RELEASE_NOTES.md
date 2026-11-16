# Address Book Application v1.0.0

青简通讯录，EE308FZ Software Engineering 个人课程项目。

## 主要功能

- 中文响应式首页、新增、详情、编辑、确认删除及操作反馈。
- 按姓名、任意电话或邮箱搜索，收藏/取消与收藏筛选。
- 多电话、多邮箱、多社交账号和多地址，SQLite 持久化。
- openpyxl 完整 XLSX 导入导出、中英文表头、JSON 多值、重复跳过及逐行错误。
- 5 条演示联系人、测试、真实运行截图、MP4、个人博客草稿和全部课程文档。

## 真实验证

本轮本地重新运行：49 passed，0 failed，后端覆盖率 97%；compileall 成功。Chromium 真实浏览器 12 项通过，0 JavaScript 异常。

已核实的四组 CI：https://github.com/3028405978-hue/address-book-application/actions/runs/43884952886，Ubuntu / Windows × Python 3.11 / 3.12 全成功。正式 Release 已在 main 四组测试通过后重新测试、编译、ZIP 独立解压测试，49 项全部通过；附件保留原始日志和精确提交信息。如后续仅补充发布证据，同样通过检查后才更新最终标签和附件。

## 安装

Python 3.11+：`python -m venv .venv`，激活环境，`python -m pip install -r requirements.txt`，`python app.py`。打开 http://127.0.0.1:5000。Windows 11 详细步骤见 README。

## 附件

- EE308_Address_Book_Submission_Final.zip：完整项目、文档、示例、截图、视频和发布时验证证据。
- 同名 .sha256：文件校验值。
- FINAL_DELIVERY_RUNTIME.json：准确 main SHA、提交数、Actions URL、测试数及覆盖率。

## 已知范围与个人待办

单用户本地通讯录，没有用户登录、分页和多实例部署。Windows hosted CI 不等同 Windows 11 桌面人工验收。CSDN 尚未公开发布、PSP 真实个人工时需本人填写、可选云部署尚未授权；这些状态不伪造。

正式发布：[v1.0.0](https://github.com/3028405978-hue/address-book-application/releases/tag/v1.0.0)。真实已合并 PR：[PR #1](https://github.com/3028405978-hue/address-book-application/pull/1)。公开 ZIP 已实际下载并通过校验。

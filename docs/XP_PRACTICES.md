# XP 实践记录

本项目按单人独立作业组织，实际代码和验证由自动化开发助手执行。没有结对编程、多人分工、他人审核或虚构讨论。

| 实践 | 本次实际证据 |
|---|---|
| Simple Design | Flask 工厂、两个蓝图、两个数据库模型；HTML/CSS/JS，不引入前端大型框架 |
| Small Releases | 本地按持久化/核心行为、Excel/页面、测试/CI、输入修复、文档证据分阶段提交；远程发布状态另见验收报告 |
| Testing | 49 项 pytest 测试使用临时 SQLite；Excel 往返测试逐字段比较；12 项浏览器检查 |
| Refactoring | 将校验集中到 clean_record；增加控制字符和输入长度检查；修正字体兼容的导入导出符号 |
| Continuous Integration | 提供 GitHub Actions 的 Linux/Windows、Python 3.11/3.12 矩阵；本轮已核实四组 CI 成功，见 FINAL_DELIVERY.md |

实际步骤：先实现模型、CRUD、搜索、收藏；再实现多值 Excel 和中文页面；随后编写回归测试；根据测试夹具错误修正初始化；浏览器检查后调整演示检索条件；补充可导出性校验并重新运行全部测试，最后整理文档和发布材料。

这不是严格先写测试的 TDD：主要功能先实现，之后补充测试并据此修正。首轮测试 38 失败、5 通过的原因是夹具访问空首页未生成 CSRF token；改为先访问新增表单后 43 通过，再补充 6 个边界校验测试，最终 49 通过。失败与修复经过真实发生。

本地 commit 的作者 `EE308 Project` 是工具使用的通用署名，不冒充学生真实姓名。正式提交前应由本人核实作者身份和课程诚信要求。

本轮收尾已真实核实 GitHub main 与 CI：https://github.com/3028405978-hue/address-book-application/actions/runs/43884952886。docs/final-submission 只修改文档、证据与打包发布流程，不重写应用。

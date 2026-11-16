# 最终验收清单

本清单区分已验证事实和尚未完成的外部步骤，不推算教师分数。

| # | 验收项 | 状态 | 证据 |
|---|---|---|---|
| 1 | 核心功能正常 | PASS | 本轮 pytest 49/49、浏览器 12 项检查 |
| 2 | GitHub main 包含完整项目 | PASS | https://github.com/3028405978-hue/address-book-application，重新克隆且 Git tree 与原项目相同 |
| 3 | 至少 3 次真实提交 | PASS | 本轮核实起点已有 7 次，区分原始本地 6 次 |
| 4 | 正式 Release | PASS | [v1.0.0](https://github.com/3028405978-hue/address-book-application/releases/tag/v1.0.0)，ZIP、SHA256、运行信息附件均实际公开 |
| 5 | 真实 PR | PASS | [PR #1 已合并](https://github.com/3028405978-hue/address-book-application/pull/1)，四组检查成功后合并 |
| 6 | Actions 已核实 | PASS | [四组成功运行](https://github.com/3028405978-hue/address-book-application/actions/runs/43884952886) |
| 7 | README 和文档同步 | PASS | 本轮移除过时认证失败/CI未运行状态，保留未完成项 |
| 8 | 唯一个人博客草稿 | PASS | [CSDN_BLOG.md](CSDN_BLOG.md) |
| 9 | GitHub 历史截图真实 | PASS | [真实 GitHub 网页](screenshots/12-github-history.png) |
| 10 | 截图和视频齐全 | PASS | 14 张证据图、50.36 秒真实运行视频 |
| 11 | PSP 准备且不伪造工时 | PASS | [PSP.md](PSP.md)，Planning 至 Summary 及合计 |
| 12 | 新测试有真实日志 | PASS | [TEST_REPORT.md](TEST_REPORT.md)、pytest-output.txt、JUnit XML |
| 13 | 最终 ZIP 独立解压可运行 | PASS | [实际附件](https://github.com/3028405978-hue/address-book-application/releases/download/v1.0.0/EE308_Address_Book_Submission_Final.zip)，Actions 内独立解压再测 49/49，本地下载后 CRC 与全文件 SHA256 校验通过 |
| 14 | 人工步骤已列出 | PASS | [FINAL_DELIVERY.md](FINAL_DELIVERY.md) |
| 15 | CSDN 公开发布 | PENDING | 需本人核实正文并上传公开媒体和博客 |
| 16 | PSP 实际个人工时 | PENDING | 本人填写，助手不编造 |
| 17 | 可选公网部署 | PENDING | 无云账号授权，不将 localhost 当公网 |

当前统计：PASS 14，PENDING 3，FAIL 0。三项待办分别为 CSDN 公开发布、本人真实 PSP 工时、可选公网部署；没有程序功能失败。Windows CI 为 GitHub hosted Windows 环境成功，不冒充 Windows 11 桌面人工验证。

个人项目，不适用双人分工、贡献比例、多人审核；老师未提供原始仓库，不编造 Fork。

发布证据：PR #1 合并提交 [63dcad3](https://github.com/3028405978-hue/address-book-application/commit/63dcad3737fada52fdb5364044f7b9d9d925c769)，main 四组 CI 及 release job 均成功：[运行记录](https://github.com/3028405978-hue/address-book-application/actions/runs/43888265296)。此后仅同步发布证据，最终 SHA 与提交数以 ZIP 的 docs/FINAL_DELIVERY_RUNTIME.json 为准。

# 最终交付索引

核实日期：2026-11-16（北京时间）。GitHub 发布、PR、测试与文件交付已经实际完成。未完成的个人发布步骤继续保持 PENDING。

| 信息 | 当前已核实结果 |
|---|---|
| GitHub 仓库 | https://github.com/3028405978-hue/address-book-application |
| 收尾核实起点 main SHA | fac58238d8e01afa55e8b5af1673b0edf01c9ccb |
| 收尾核实起点 GitHub 提交数 | 7；原始本地历史另有 6 次，不能混算 |
| 最终发布提交 SHA / 数量 | 以 Release 附件 FINAL_DELIVERY_RUNTIME.json 中 main_commit_sha / commit_count 为精确值；同一提交无法在自身内容中包含自身 SHA |
| Release | PASS，[正式 v1.0.0](https://github.com/3028405978-hue/address-book-application/releases/tag/v1.0.0)，含 ZIP、SHA256 和运行信息附件 |
| 真实 PR | PASS，[PR #1](https://github.com/3028405978-hue/address-book-application/pull/1) 已合并；合并提交 [63dcad3](https://github.com/3028405978-hue/address-book-application/commit/63dcad3737fada52fdb5364044f7b9d9d925c769) |
| 已成功 Actions | [PR 四组成功](https://github.com/3028405978-hue/address-book-application/actions/runs/43888000056)，[main 四组及 Release 成功](https://github.com/3028405978-hue/address-book-application/actions/runs/43888265296) |
| 测试 | 本轮重新运行 49 passed，0 failed；后端语句覆盖率 97% |
| 测试环境 | Linux / Python 3.12.14；Actions 另验证 Ubuntu、Windows × Python 3.11、3.12 |
| 截图 | 14 张：12 张既有真实证据 + GitHub 历史网页和 Actions 网页各 1 张 |
| 演示视频 | docs/video/demo.mp4，H.264，1440×1000，50.36 秒；可完整解码 |
| 博客 | docs/CSDN_BLOG.md，唯一个人 Markdown 草稿 |
| CSDN 发布 | PENDING，尚未公开发布 |
| 云部署 | PENDING，可选加分，无已授权账号，不开通收费服务 |
| ZIP | PASS，[直接下载 EE308_Address_Book_Submission_Final.zip](https://github.com/3028405978-hue/address-book-application/releases/download/v1.0.0/EE308_Address_Book_Submission_Final.zip)；实际下载并校验通过 |

本人必须完成：核实实际 PSP 工时与身份/开发经历；将博客正文、图片、视频上传到 CSDN 并替换公开媒体 URL，发布并提交课程链接。没有要求本人补做本可自动完成的程序开发。

GitHub Actions release job 在四组测试成功后重新测试、编译、打包、独立解压再测，再发布 v1.0.0 和附件。公开状态必须以实际运行结论和 Release API 为准。后续若仅补充发布证据，会在测试通过后将发布标签快进到最终 main，并重新生成附件；不改写原提交，也不修改已通过验证的核心代码。

## 最后一次文档核实时的 main 快照

main SHA：`63dcad3737fada52fdb5364044f7b9d9d925c769`；实际提交数量：9。随后还有本次发布证据修订及其合并，因此这里是带明确时点的快照，不冒充最终同一提交的自引用 SHA。最终准确 SHA 和计数已由流水线写入 [Release 运行信息附件](https://github.com/3028405978-hue/address-book-application/releases/download/v1.0.0/FINAL_DELIVERY_RUNTIME.json)，也内置于 ZIP 的 docs/FINAL_DELIVERY_RUNTIME.json。实时 main 可核对 [GitHub API](https://api.github.com/repos/3028405978-hue/address-book-application/commits/main)。

最新 GitHub 历史截图对应 9 次提交检查点，Actions 截图对应 PR #1 合并后的成功运行。原始 API 证据在 docs/ci/，保留运行时点。

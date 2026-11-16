# GitHub 文件整理说明

本轮按用户要求不处理 GitHub CLI 授权，不执行远程上传。项目根文件夹为 `address-book-application`，所有需要上传的文件均已集中在该目录。

## 应上传的内容

- 根目录 Python 源码、requirements.txt、pytest.ini、README.md、CODE_STANDARD.md、render.yaml、start_windows.bat、sample_contacts.xlsx。
- routes/、services/、templates/、static/、tests/ 完整目录。
- docs/ 完整目录：包含个人 CSDN 博客、测试报告、Release 说明、最终验收清单、实际截图和 MP4。
- .github/workflows/tests.yml 与 .gitignore。手动上传时注意隐藏文件不要遗漏。

## 无需上传的内容

`.git/` 是本地 Git 元数据；`.venv/`、缓存、运行数据库、`.env` 不应上传。`address-book-history.bundle`、`git-history.txt`、`FILE_MANIFEST.sha256` 是 ZIP 内的交付与历史恢复材料，已由 .gitignore 排除；正常 Git 推送不会提交它们。bundle 用于恢复原提交历史，而不是伪造提交。

后续如使用网页上传，仅上传源码和文档会新增一条网页提交，不能自动保留原来的本地历史；如需保留历史，应恢复 bundle 后正常推送。暂不授权不影响项目本地运行、测试和课程材料准备。

## 核心文档位置

- 个人博客：docs/CSDN_BLOG.md
- 测试报告：docs/TEST_REPORT.md
- Release 说明：docs/RELEASE_NOTES.md
- 最终验收：docs/FINAL_ACCEPTANCE.md
- 提交清单：docs/SUBMISSION_CHECKLIST.md
- Windows 启动步骤：README.md

博客中的 PSP 工时、本人经历和公开图片/视频链接仍需本人核实，不以编造内容代填。

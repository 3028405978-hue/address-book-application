# GitHub 文件与下载说明

完整项目已经上传：https://github.com/3028405978-hue/address-book-application 。不再需要用户手动上传源码，也不再要求重复进行 GitHub CLI 授权。

应纳入版本管理的内容：根目录源码与配置、requirements.txt、pytest.ini、README、CODE_STANDARD、示例 Excel、routes/、services/、templates/、static/、tests/、scripts/、docs/、.github/。隐藏文件 `.gitignore` 和 `.github/workflows/tests.yml` 也已包含。

禁止上传：数据库、.env、令牌、虚拟环境、缓存、运行时 dist/。发布工作流会从受版本管理文件构建 ZIP，排除这些内容；新增运行证据与精确提交信息只进入附件，不通过提交回写造成循环。

最终 ZIP 名称：EE308_Address_Book_Submission_Final.zip。优先从 [Release](https://github.com/3028405978-hue/address-book-application/releases/tag/v1.0.0) 下载，该 Release 已正式公开，附件已实际下载并校验通过。源码也可用 GitHub Code → Download ZIP，后者不包含发布时新增的验证日志。

博客、测试报告、Release 说明、验收报告和最终交付索引分别位于 docs/CSDN_BLOG.md、TEST_REPORT.md、RELEASE_NOTES.md、FINAL_ACCEPTANCE.md、FINAL_DELIVERY.md。

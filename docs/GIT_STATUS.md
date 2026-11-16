# Git 与远程发布状态

远程仓库：https://github.com/3028405978-hue/address-book-application

本地远程 origin 已设置到用户指定仓库，没有重新创建仓库，也没有虚构 Fork。单人项目，提交使用工具的通用署名 EE308 Project。最终本地 main 共 6 次真实提交；附带 v1.0.0 本地标签。具体 SHA 见本包 git-history.txt。

已尝试 `git push -u origin main`，返回 `could not read Username ... terminal prompts disabled`。gh auth status 报告现有 GH_TOKEN 无效。正式上传、远程 Release 和 PR 因此尚未成功，地址待认证后填写。

本地截图 screenshots/11-git-history.png 捕获第四次提交检查点，含真实 git log 的 SHA、时间和信息；后续两次文档提交在截图之后，最终数以 git-history.txt 和实际 rev-list 为准。这不是 GitHub 网页截图。

## 恢复 Git 历史

最终 ZIP 包含 `address-book-history.bundle`，而非 .git 隐藏目录：

```bat
git clone address-book-history.bundle restored-address-book
cd restored-address-book
git remote set-url origin https://github.com/3028405978-hue/address-book-application.git
git log --oneline
git rev-list --count HEAD
```

bundle 保存已提交源码和真实历史；ZIP 中额外的打包清单和 git-history.txt 不属于最后一个提交的源码快照，属于交付证据。

## 认证后完成远程发布

不要把令牌粘贴到聊天或文档。在本机通过 GitHub CLI 或 Credential Manager 登录：

```bat
gh auth login
gh auth setup-git
git push -u origin main
git push origin v1.0.0
gh release create v1.0.0 --title "Address Book Application v1.0.0" --notes-file docs/RELEASE_NOTES.md
```

若环境注入失效 GH_TOKEN，需在本机移除失效环境变量或通过安全配置更新后再认证。不使用 force push；远程若已变化应先 fetch 检查。

如需补做真实 PR：从 main 新建 `docs/manual-verification` 分支，实际补充 Windows 运行记录或本人 PSP 核实结果，提交并推送，然后 `gh pr create --base main --head docs/manual-verification --title "docs: record manual submission verification" --body-file docs/PR_BODY.md`。只有存在真实差异时才创建，不创建空 PR。PR 提交和合并后应重新记录 commit 数量。

本轮交付范围更新：用户明确暂不处理 GitHub CLI 授权；本轮仅完成本地开发、测试、文档及打包。GitHub 上传、PR 和正式 Release 延后，不阻塞本地交付。

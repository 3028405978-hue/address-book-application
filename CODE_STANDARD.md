# 代码规范

1. Python 使用四空格缩进，模块/函数使用 snake_case，类使用 PascalCase，常量使用 UPPER_CASE。
2. Flask app factory 负责配置、数据库初始化和蓝图注册；路由处理 HTTP；services 负责转换与校验；models 只定义持久化结构。
3. SQLAlchemy 绑定参数处理输入，禁止拼接用户 SQL；Jinja 默认转义，禁止把用户内容标为 safe。
4. 所有写操作为 POST，必须带会话 CSRF token；删除前使用确认框。GET 不修改数据。
5. 值校验集中在 clean_record，创建、编辑、Excel 导入复用；事务提交前校验，失败回滚。
6. 多值通过 ContactMethod 一对多存储，用 values(kind) 统一读取。不要在数据库用分号拼接。
7. 前端不使用 innerHTML 拼接用户内容，动态表单通过 DOM API 构建。按钮具备可读名称，布局支持手机。
8. 测试采用 pytest fixture 的 tmp_path SQLite 数据库，绝不指向用户数据库。
9. Git 提交围绕可说明的功能阶段，提交信息使用 feat/test/fix/docs。严禁把 .env、数据库、虚拟环境和缓存入库。
10. 文档中区分本地验证、远程 CI、公开部署；不把计划写成已完成事实。

手工审查：已核对姓名校验、多值编辑替换、子记录级联删除、CSRF、模板转义、上传限制及 Excel 公式单元格处理。未声称接受过第二人代码审核。

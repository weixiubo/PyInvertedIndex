# 贡献指南

感谢你对本项目的关注！欢迎任何形式的贡献。

## 如何贡献

### 报告Bug

如果你发现了bug，请创建一个Issue，并包含以下信息：

- Bug的详细描述
- 复现步骤
- 期望的行为
- 实际的行为
- Python版本和操作系统信息

### 提出新功能

如果你有新功能的想法，请先创建一个Issue讨论：

- 功能的详细描述
- 使用场景
- 可能的实现方案

### 提交代码

1. **Fork本仓库**

2. **创建特性分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **编写代码**
   - 遵循现有的代码风格
   - 添加必要的注释和文档字符串
   - 确保代码通过所有测试

4. **运行测试**
   ```bash
   pytest test_inverted_index.py -v
   ```

5. **提交更改**
   ```bash
   git add .
   git commit -m "Add: 简短描述你的更改"
   ```

6. **推送到你的Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **创建Pull Request**
   - 清晰描述你的更改
   - 引用相关的Issue（如果有）

## 代码规范

### Python代码风格

- 遵循PEP 8规范
- 使用4个空格缩进
- 函数和方法添加文档字符串
- 变量和函数使用描述性命名

### 提交信息规范

使用清晰的提交信息：

- `Add: 添加新功能`
- `Fix: 修复bug`
- `Update: 更新现有功能`
- `Refactor: 重构代码`
- `Docs: 更新文档`
- `Test: 添加或修改测试`

## 开发环境设置

1. **克隆仓库**
   ```bash
   git clone https://github.com/your-username/inverted-index.git
   cd inverted-index
   ```

2. **安装依赖**（可选）
   ```bash
   pip install -r requirements.txt
   ```

3. **运行测试**
   ```bash
   pytest test_inverted_index.py -v
   ```

4. **运行演示**
   ```bash
   python demo.py
   ```

## 测试

所有新功能和bug修复都应该包含相应的测试用例。

运行测试：
```bash
# 运行所有测试
pytest test_inverted_index.py -v

# 运行特定测试
pytest test_inverted_index.py::TestInvertedIndex::test_search -v
```

## 文档

如果你的更改影响了用户接口或添加了新功能，请更新README.md。

## 问题和讨论

如有任何问题，欢迎：

- 创建Issue讨论
- 在Pull Request中提问
- 通过邮件联系维护者

## 行为准则

- 尊重所有贡献者
- 保持友好和专业
- 接受建设性的批评
- 关注项目的最佳利益

## 许可证

通过贡献代码，你同意你的贡献将在MIT许可证下发布。

---

再次感谢你的贡献！🎉


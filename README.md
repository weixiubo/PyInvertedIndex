# 倒排索引系统实现

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: PEP8](https://img.shields.io/badge/code%20style-PEP8-brightgreen.svg)](https://www.python.org/dev/peps/pep-0008/)

## 项目简介

本项目实现了一个完整的**倒排索引（Inverted Index）**系统，这是信息检索和搜索引擎的核心数据结构。系统支持文档索引构建、多种查询方式和索引持久化等功能。

**🌟 特点**：
- ✅ 纯Python实现，无需额外依赖
- ✅ 完整的单元测试覆盖
- ✅ 详细的代码注释和文档
- ✅ 支持多种查询方式
- ✅ 包含演示程序和交互式界面

## 倒排索引原理

### 什么是倒排索引？

倒排索引是一种将**词项（Term）**映射到**包含该词项的文档列表**的索引结构，与传统的"文档→词项"的正向索引相反。

**示例：**

假设有以下文档：
- doc1: "search engine"
- doc2: "inverted index"  
- doc3: "search index"

倒排索引结构：
```
search  → [doc1, doc3]
engine  → [doc1]
inverted → [doc2]
index   → [doc2, doc3]
```

### 核心组成部分

1. **词典（Dictionary）**: 存储所有唯一的词项
2. **倒排列表（Posting List）**: 每个词项对应的文档列表及位置信息
3. **文档存储**: 保存原始文档内容

### 数据结构

```python
{
    "词项1": {
        "文档ID1": [位置1, 位置2, ...],
        "文档ID2": [位置1, 位置2, ...],
    },
    "词项2": {
        ...
    }
}
```

## 功能特性

### ✅ 核心功能

- [x] **文档预处理**
  - 文本分词（基于正则表达式）
  - 转小写标准化
  - 停用词过滤
  
- [x] **索引构建**
  - 单文档添加
  - 批量文档索引
  - 位置信息记录
  
- [x] **多种查询方式**
  - 单词查询
  - AND查询（交集）
  - OR查询（并集）
  - NOT查询（差集）
  - 短语查询（位置相邻）
  
- [x] **统计分析**
  - 词频（TF - Term Frequency）
  - 文档频率（DF - Document Frequency）
  - 索引统计信息
  
- [x] **索引持久化**
  - JSON格式保存
  - 索引加载恢复

## 项目结构

```
.
├── inverted_index.py              # 核心倒排索引类
├── demo.py                        # 演示程序
├── interactive_search.py          # 交互式查询程序
├── test_inverted_index.py         # 单元测试
├── parse_reuters.py               # Reuters数据集解析器
├── performance_test.py            # 性能测试
├── README.md                      # 项目文档
├── LICENSE                        # MIT许可证
├── CONTRIBUTING.md                # 贡献指南
├── requirements.txt               # 依赖列表
├── data/                          # 数据目录
│   └── reut2-*.sgm               # Reuters-21578数据集
└── output/                        # 输出目录
    ├── inverted_index_data.json  # 索引数据文件
    └── performance_results.json  # 性能测试结果
```

## 安装和运行

### 环境要求

- Python 3.6+
- 无需额外依赖库（仅使用Python标准库）
- pytest（可选，用于运行测试）

### 快速开始

#### 1. 克隆仓库

```bash
git clone https://github.com/your-username/inverted-index.git
cd inverted-index
```

#### 2. 安装依赖（可选）

```bash
pip install -r requirements.txt
```

#### 3. 运行演示程序

```bash
python demo.py
```

演示程序会：
- 构建包含8个文档的倒排索引
- 展示完整的索引结构
- 演示各种查询功能
- 保存索引到文件

#### 4. 运行交互式查询程序

```bash
python interactive_search.py
```

交互式程序提供菜单式操作界面，支持：
- 实时查询
- 查看索引结构
- 统计信息查看

#### 5. 运行测试

```bash
pytest test_inverted_index.py -v
```

测试覆盖所有核心功能，包括：
- 文档添加和预处理
- 各种查询方式
- 统计功能
- 索引持久化

## 使用示例

### 基本使用

```python
from inverted_index import InvertedIndex

# 创建索引实例
index = InvertedIndex()

# 添加文档
documents = {
    "doc1": "Information retrieval is important",
    "doc2": "Search engines use inverted index",
    "doc3": "Inverted index enables fast search"
}

# 构建索引
index.build_from_documents(documents)

# 单词查询
result = index.search("index")
print(result)  # {'doc2': [3], 'doc3': [1]}

# AND查询
docs = index.search_and(["inverted", "index"])
print(docs)  # {'doc2', 'doc3'}

# 短语查询
docs = index.search_phrase("inverted index")
print(docs)  # {'doc2', 'doc3'}
```

### 高级查询

```python
# OR查询
docs = index.search_or(["search", "retrieval"])

# NOT查询（包含"search"但不包含"engines"）
docs = index.search_not(["search"], ["engines"])

# 词频统计
tf = index.get_term_frequency("index", "doc2")
df = index.get_document_frequency("index")

# 显示索引结构
index.display_index()

# 保存和加载
index.save_to_file("my_index.json")
index.load_from_file("my_index.json")
```

## 核心算法说明

### 1. 文档预处理

```python
def preprocess(text: str) -> List[str]:
    # 1. 转小写
    text = text.lower()
    # 2. 分词（提取字母数字组合）
    tokens = re.findall(r'\b[a-z0-9]+\b', text)
    # 3. 去停用词
    tokens = [t for t in tokens if t not in stop_words]
    return tokens
```

### 2. 索引构建

```python
for position, token in enumerate(tokens):
    # 记录词项在文档中的位置
    index[token][doc_id].append(position)
```

### 3. 短语查询算法

短语查询需要验证词项在文档中是否连续出现：

1. 获取短语中第一个词的所有文档
2. 对每个候选文档，检查后续词是否在连续位置出现
3. 返回满足条件的文档集合

## 查询类型详解

### AND查询（交集）

返回**同时包含所有查询词**的文档。

**算法**: 对所有词项的文档集合求交集

**示例**:
```
查询: "search" AND "engine"
结果: 同时包含这两个词的文档
```

### OR查询（并集）

返回**包含任一查询词**的文档。

**算法**: 对所有词项的文档集合求并集

**示例**:
```
查询: "search" OR "retrieval"
结果: 包含"search"或"retrieval"的所有文档
```

### NOT查询（差集）

返回**包含某些词但不包含另一些词**的文档。

**算法**: 从包含词集合中减去排除词集合

**示例**:
```
查询: "index" NOT "database"
结果: 包含"index"但不包含"database"的文档
```

### 短语查询

返回包含**完整短语**的文档（词必须连续出现）。

**算法**:
1. 检查所有词是否都在文档中
2. 验证词的位置是否连续

**示例**:
```
查询: "inverted index"
结果: 只返回这两个词连续出现的文档
```

## 性能特点

### 时间复杂度

- **索引构建**: O(n×m)，n为文档数，m为平均文档长度
- **单词查询**: O(1) - 哈希表查找
- **AND查询**: O(k×d)，k为查询词数，d为平均文档列表长度
- **短语查询**: O(d×p)，d为候选文档数，p为短语长度

### 空间复杂度

- **索引存储**: O(V×D)，V为词汇表大小，D为文档数
- 包含位置信息，空间占用较大但支持短语查询

## 应用场景

1. **搜索引擎**: 快速检索包含关键词的网页
2. **文档管理系统**: 全文检索
3. **日志分析**: 快速查找特定事件
4. **代码搜索**: 在代码库中搜索函数、变量
5. **电子邮件搜索**: 邮件内容检索

## 扩展方向

### 可能的改进

1. **更好的分词**
   - 支持中文分词（jieba）
   - 词干提取（Porter Stemmer）
   - 词形还原（Lemmatization）

2. **相关性排序**
   - TF-IDF权重计算
   - BM25排序算法
   - PageRank集成

3. **性能优化**
   - 压缩倒排列表
   - 跳表加速合并
   - 分布式索引

4. **功能增强**
   - 通配符查询
   - 模糊匹配
   - 拼写纠错
   - 同义词扩展

## 实验报告要点

### 1. 倒排索引原理

- 定义和作用
- 与正向索引的区别
- 数据结构设计

### 2. 实现细节

- 文档预处理流程
- 索引构建算法
- 查询处理方法

### 3. 功能演示

- 运行demo.py的输出结果
- 各种查询的示例
- 索引结构可视化

### 4. 性能分析

- 时间复杂度分析
- 空间复杂度分析
- 优化方向讨论

## 常见问题

**Q: 为什么需要停用词过滤？**

A: 停用词（如"the", "is", "a"）在几乎所有文档中都出现，对检索没有区分度，过滤它们可以减小索引大小并提高查询效率。

**Q: 位置信息有什么用？**

A: 位置信息支持短语查询和邻近查询，可以判断词是否连续出现或在一定距离内出现。

**Q: 如何处理大规模文档？**

A: 可以采用分块索引、压缩存储、倒排列表合并优化等技术。对于超大规模，需要分布式索引系统。

## 参考资料

1. **《信息检索导论》** - Manning, Raghavan, Schütze
2. **《搜索引擎：信息检索实践》** - Croft, Metzler, Strohman
3. [Elasticsearch官方文档](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
4. [Lucene倒排索引实现](https://lucene.apache.org/)

## 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与项目。

### 贡献者

感谢所有为本项目做出贡献的人！

## 作者

**魏秀博** - 华中师范大学 - 信息检索技术课程实验项目

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 致谢

- 感谢《信息检索导论》提供的理论基础
- 感谢Reuters-21578数据集
- 感谢所有开源贡献者

## 联系方式

如有问题或建议，欢迎：
- 创建 [Issue](https://github.com/your-username/inverted-index/issues)
- 提交 [Pull Request](https://github.com/your-username/inverted-index/pulls)
- 发送邮件至：your-email@example.com

---

**⭐ 如果这个项目对你有帮助，请给个Star！**

**祝实验顺利！如有问题欢迎交流。** 🎓



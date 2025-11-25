"""
倒排索引系统演示程序
展示倒排索引的构建和查询功能
"""

from inverted_index import InvertedIndex


def print_section(title):
    """打印分节标题"""
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80)


def print_search_results(title, doc_ids, index):
    """打印搜索结果"""
    print(f"\n{title}")
    print("-" * 60)
    if doc_ids:
        print(f"找到 {len(doc_ids)} 个文档:")
        for doc_id in sorted(doc_ids):
            content = index.documents[doc_id]
            # 截断过长的内容
            display_content = content if len(content) <= 100 else content[:100] + "..."
            print(f"  [{doc_id}] {display_content}")
    else:
        print("未找到匹配的文档")


def main():
    """主演示程序"""
    
    print_section("倒排索引系统演示")
    
    # 创建倒排索引实例
    index = InvertedIndex()
    
    # 准备示例文档集
    documents = {
        "doc1": "Information retrieval is the process of obtaining information system resources.",
        "doc2": "Search engines use inverted index for fast information retrieval.",
        "doc3": "An inverted index is a database index storing a mapping from content.",
        "doc4": "The inverted index data structure is a central component of search engines.",
        "doc5": "Information systems store and retrieve data efficiently using index structures.",
        "doc6": "Database management systems use various index structures for query optimization.",
        "doc7": "Full-text search requires inverted index to find documents quickly.",
        "doc8": "Modern search engines process millions of queries using inverted indexes.",
    }
    
    print("\n正在构建倒排索引...")
    print(f"文档数量: {len(documents)}")
    
    # 构建索引
    index.build_from_documents(documents)
    
    print("✓ 索引构建完成!")
    
    # 显示索引统计信息
    index.display_statistics()
    
    # 显示完整的倒排索引结构
    index.display_index()
    
    # ========== 演示各种查询功能 ==========
    
    print_section("查询功能演示")
    
    # 1. 单词查询
    print("\n【1】单词查询示例")
    term = "index"
    result = index.search(term)
    print(f"\n查询词: '{term}'")
    print(f"结果: {dict(result)}")
    print_search_results(f"包含 '{term}' 的文档:", set(result.keys()), index)
    
    # 2. AND查询
    print("\n\n【2】AND查询示例 (所有词都必须出现)")
    terms = ["inverted", "index"]
    result = index.search_and(terms)
    print(f"\n查询: {' AND '.join(terms)}")
    print_search_results(f"同时包含 {terms} 的文档:", result, index)
    
    # 3. OR查询
    print("\n\n【3】OR查询示例 (任一词出现即可)")
    terms = ["database", "search"]
    result = index.search_or(terms)
    print(f"\n查询: {' OR '.join(terms)}")
    print_search_results(f"包含 {terms} 中任一词的文档:", result, index)
    
    # 4. NOT查询
    print("\n\n【4】NOT查询示例 (包含某词但不包含另一词)")
    include = ["information"]
    exclude = ["database"]
    result = index.search_not(include, exclude)
    print(f"\n查询: 包含 {include} 但不包含 {exclude}")
    print_search_results(f"结果:", result, index)
    
    # 5. 短语查询
    print("\n\n【5】短语查询示例 (词必须连续出现)")
    phrase = "inverted index"
    result = index.search_phrase(phrase)
    print(f"\n查询短语: \"{phrase}\"")
    print_search_results(f"包含短语 \"{phrase}\" 的文档:", result, index)
    
    # 6. 词频统计
    print("\n\n【6】词频统计示例")
    term = "index"
    print(f"\n词项 '{term}' 的统计信息:")
    print(f"  文档频率 (DF): {index.get_document_frequency(term)} 个文档")
    for doc_id in sorted(index.documents.keys()):
        tf = index.get_term_frequency(term, doc_id)
        if tf > 0:
            print(f"  文档 {doc_id} 中的词频 (TF): {tf}")
    
    # 7. 复杂查询组合
    print("\n\n【7】复杂查询示例")
    print("\n查询: (search OR retrieval) AND index")
    docs_with_search_or_retrieval = index.search_or(["search", "retrieval"])
    docs_with_index = index.search_and(["index"])
    result = docs_with_search_or_retrieval & docs_with_index
    print_search_results("结果:", result, index)
    
    # 保存索引到文件
    print_section("保存索引")
    index.save_to_file("inverted_index_data.json")
    
    # 测试加载索引
    print_section("测试加载索引")
    new_index = InvertedIndex()
    new_index.load_from_file("inverted_index_data.json")
    print("✓ 索引加载成功!")
    print(f"验证: 加载的索引包含 {len(new_index.documents)} 个文档")
    
    print_section("演示完成")
    print("\n所有功能测试通过! ✓")
    print("\n提示: 查看 inverted_index_data.json 文件可以看到完整的索引结构")


if __name__ == "__main__":
    main()


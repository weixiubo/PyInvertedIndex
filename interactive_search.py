"""
交互式倒排索引查询系统
允许用户交互式地查询倒排索引
"""

from inverted_index import InvertedIndex


def print_menu():
    """打印菜单"""
    print("\n" + "="*60)
    print("倒排索引查询系统")
    print("="*60)
    print("1. 单词查询")
    print("2. AND查询 (多个词都必须出现)")
    print("3. OR查询 (任一词出现即可)")
    print("4. NOT查询 (包含某词但排除另一词)")
    print("5. 短语查询 (词必须连续出现)")
    print("6. 查看词频统计")
    print("7. 显示所有文档")
    print("8. 显示索引结构")
    print("9. 显示统计信息")
    print("0. 退出")
    print("="*60)


def display_results(doc_ids, index):
    """显示查询结果"""
    if not doc_ids:
        print("\n❌ 未找到匹配的文档")
        return
    
    print(f"\n✓ 找到 {len(doc_ids)} 个文档:")
    print("-" * 60)
    for doc_id in sorted(doc_ids):
        content = index.documents[doc_id]
        print(f"\n[{doc_id}]")
        print(f"{content}")
    print("-" * 60)


def main():
    """主程序"""
    # 创建索引并加载示例数据
    index = InvertedIndex()
    
    # 示例文档集
    documents = {
        "doc1": "Information retrieval is the process of obtaining information system resources.",
        "doc2": "Search engines use inverted index for fast information retrieval.",
        "doc3": "An inverted index is a database index storing a mapping from content.",
        "doc4": "The inverted index data structure is a central component of search engines.",
        "doc5": "Information systems store and retrieve data efficiently using index structures.",
        "doc6": "Database management systems use various index structures for query optimization.",
        "doc7": "Full-text search requires inverted index to find documents quickly.",
        "doc8": "Modern search engines process millions of queries using inverted indexes.",
        "doc9": "Python is a popular programming language for data science and machine learning.",
        "doc10": "Machine learning algorithms can process large datasets efficiently.",
    }
    
    print("正在构建倒排索引...")
    index.build_from_documents(documents)
    print(f"✓ 索引构建完成! 共 {len(documents)} 个文档\n")
    
    # 主循环
    while True:
        print_menu()
        choice = input("\n请选择操作 (0-9): ").strip()
        
        if choice == '0':
            print("\n感谢使用! 再见!")
            break
        
        elif choice == '1':
            # 单词查询
            term = input("\n请输入查询词: ").strip()
            if term:
                result = index.search(term)
                print(f"\n查询: '{term}'")
                if result:
                    print(f"倒排列表: {dict(result)}")
                display_results(set(result.keys()), index)
        
        elif choice == '2':
            # AND查询
            terms_input = input("\n请输入多个查询词 (空格分隔): ").strip()
            if terms_input:
                terms = terms_input.split()
                result = index.search_and(terms)
                print(f"\n查询: {' AND '.join(terms)}")
                display_results(result, index)
        
        elif choice == '3':
            # OR查询
            terms_input = input("\n请输入多个查询词 (空格分隔): ").strip()
            if terms_input:
                terms = terms_input.split()
                result = index.search_or(terms)
                print(f"\n查询: {' OR '.join(terms)}")
                display_results(result, index)
        
        elif choice == '4':
            # NOT查询
            include_input = input("\n请输入必须包含的词 (空格分隔): ").strip()
            exclude_input = input("请输入必须排除的词 (空格分隔): ").strip()
            if include_input or exclude_input:
                include_terms = include_input.split() if include_input else []
                exclude_terms = exclude_input.split() if exclude_input else []
                result = index.search_not(include_terms, exclude_terms)
                print(f"\n查询: 包含 {include_terms} 但不包含 {exclude_terms}")
                display_results(result, index)
        
        elif choice == '5':
            # 短语查询
            phrase = input("\n请输入查询短语: ").strip()
            if phrase:
                result = index.search_phrase(phrase)
                print(f"\n查询短语: \"{phrase}\"")
                display_results(result, index)
        
        elif choice == '6':
            # 词频统计
            term = input("\n请输入词项: ").strip()
            if term:
                df = index.get_document_frequency(term)
                print(f"\n词项 '{term}' 的统计:")
                print(f"文档频率 (DF): {df} 个文档")
                
                if df > 0:
                    print("\n各文档中的词频 (TF):")
                    for doc_id in sorted(index.documents.keys()):
                        tf = index.get_term_frequency(term, doc_id)
                        if tf > 0:
                            print(f"  {doc_id}: {tf} 次")
        
        elif choice == '7':
            # 显示所有文档
            print("\n所有文档:")
            print("-" * 60)
            for doc_id in sorted(index.documents.keys()):
                print(f"\n[{doc_id}]")
                print(f"{index.documents[doc_id]}")
            print("-" * 60)
        
        elif choice == '8':
            # 显示索引结构
            index.display_index()
        
        elif choice == '9':
            # 显示统计信息
            index.display_statistics()
        
        else:
            print("\n❌ 无效的选择，请重试")
        
        input("\n按回车键继续...")


if __name__ == "__main__":
    main()


"""
倒排索引系统实现
实现了完整的倒排索引功能，包括文档处理、索引构建和查询
"""

import re
import json
from collections import defaultdict
from typing import List, Dict, Set, Tuple


class InvertedIndex:
    """倒排索引核心类"""
    
    def __init__(self):
        """初始化倒排索引"""
        # 倒排索引：{词项: {文档ID: [位置列表]}}
        self.index = defaultdict(lambda: defaultdict(list))
        # 文档存储：{文档ID: 文档内容}
        self.documents = {}
        # 文档长度：{文档ID: 词项数量}
        self.doc_lengths = {}
        # 停用词集合
        self.stop_words = self._load_stop_words()
        
    def _load_stop_words(self) -> Set[str]:
        """加载停用词表"""
        # 常见英文停用词
        return {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'the', 'this', 'but', 'they', 'have',
            'had', 'what', 'when', 'where', 'who', 'which', 'why', 'how'
        }
    
    def preprocess(self, text: str) -> List[str]:
        """
        文本预处理
        1. 转小写
        2. 分词（提取字母数字组合）
        3. 去停用词
        """
        # 转小写
        text = text.lower()
        # 分词：提取字母和数字组合
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        # 去停用词
        tokens = [token for token in tokens if token not in self.stop_words]
        return tokens
    
    def add_document(self, doc_id: str, content: str):
        """
        添加文档到索引
        
        Args:
            doc_id: 文档唯一标识
            content: 文档内容
        """
        # 保存原始文档
        self.documents[doc_id] = content
        
        # 预处理文档
        tokens = self.preprocess(content)
        
        # 记录文档长度
        self.doc_lengths[doc_id] = len(tokens)
        
        # 构建倒排索引
        for position, token in enumerate(tokens):
            # 记录词项在文档中的位置
            self.index[token][doc_id].append(position)
    
    def build_from_documents(self, documents: Dict[str, str]):
        """
        从文档集合批量构建索引
        
        Args:
            documents: {文档ID: 文档内容} 字典
        """
        for doc_id, content in documents.items():
            self.add_document(doc_id, content)
    
    def search(self, term: str) -> Dict[str, List[int]]:
        """
        搜索单个词项
        
        Args:
            term: 搜索词项
            
        Returns:
            {文档ID: [位置列表]} 字典
        """
        # 预处理查询词
        processed_terms = self.preprocess(term)
        if not processed_terms:
            return {}
        
        term = processed_terms[0]
        return dict(self.index.get(term, {}))
    
    def search_and(self, terms: List[str]) -> Set[str]:
        """
        AND查询：返回包含所有词项的文档
        
        Args:
            terms: 查询词项列表
            
        Returns:
            文档ID集合
        """
        if not terms:
            return set()
        
        # 预处理所有查询词
        processed_terms = []
        for term in terms:
            tokens = self.preprocess(term)
            processed_terms.extend(tokens)
        
        if not processed_terms:
            return set()
        
        # 获取第一个词项的文档集合
        result = set(self.index.get(processed_terms[0], {}).keys())
        
        # 与其他词项的文档集合求交集
        for term in processed_terms[1:]:
            result &= set(self.index.get(term, {}).keys())
        
        return result
    
    def search_or(self, terms: List[str]) -> Set[str]:
        """
        OR查询：返回包含任一词项的文档

        Args:
            terms: 查询词项列表

        Returns:
            文档ID集合
        """
        result = set()

        # 预处理所有查询词
        for term in terms:
            tokens = self.preprocess(term)
            for token in tokens:
                result |= set(self.index.get(token, {}).keys())

        return result

    def search_not(self, include_terms: List[str], exclude_terms: List[str]) -> Set[str]:
        """
        NOT查询：返回包含include_terms但不包含exclude_terms的文档

        Args:
            include_terms: 必须包含的词项
            exclude_terms: 必须排除的词项

        Returns:
            文档ID集合
        """
        # 获取包含词项的文档
        if include_terms:
            result = self.search_and(include_terms)
        else:
            result = set(self.documents.keys())

        # 排除包含排除词项的文档
        exclude_docs = self.search_or(exclude_terms)
        result -= exclude_docs

        return result

    def search_phrase(self, phrase: str) -> Set[str]:
        """
        短语查询：返回包含完整短语的文档

        Args:
            phrase: 查询短语

        Returns:
            文档ID集合
        """
        # 预处理短语
        tokens = self.preprocess(phrase)
        if not tokens:
            return set()

        # 如果只有一个词，直接返回
        if len(tokens) == 1:
            return set(self.index.get(tokens[0], {}).keys())

        # 获取第一个词的文档列表
        first_term = tokens[0]
        candidate_docs = set(self.index.get(first_term, {}).keys())

        result = set()

        # 对每个候选文档检查短语是否连续出现
        for doc_id in candidate_docs:
            # 获取第一个词在文档中的位置
            positions = self.index[first_term][doc_id]

            # 检查每个位置
            for start_pos in positions:
                # 检查后续词是否在连续位置出现
                match = True
                for i, token in enumerate(tokens[1:], 1):
                    expected_pos = start_pos + i
                    if doc_id not in self.index[token] or \
                       expected_pos not in self.index[token][doc_id]:
                        match = False
                        break

                if match:
                    result.add(doc_id)
                    break

        return result

    def get_term_frequency(self, term: str, doc_id: str) -> int:
        """
        获取词项在文档中的频率

        Args:
            term: 词项
            doc_id: 文档ID

        Returns:
            词频
        """
        processed_terms = self.preprocess(term)
        if not processed_terms:
            return 0

        term = processed_terms[0]
        return len(self.index.get(term, {}).get(doc_id, []))

    def get_document_frequency(self, term: str) -> int:
        """
        获取包含词项的文档数量

        Args:
            term: 词项

        Returns:
            文档频率
        """
        processed_terms = self.preprocess(term)
        if not processed_terms:
            return 0

        term = processed_terms[0]
        return len(self.index.get(term, {}))

    def display_index(self):
        """显示倒排索引结构"""
        print("\n" + "="*80)
        print("倒排索引结构")
        print("="*80)

        # 按字母顺序排序词项
        sorted_terms = sorted(self.index.keys())

        for term in sorted_terms:
            postings = self.index[term]
            doc_count = len(postings)
            print(f"\n词项: '{term}' (出现在 {doc_count} 个文档中)")

            # 显示每个文档的信息
            for doc_id in sorted(postings.keys()):
                positions = postings[doc_id]
                freq = len(positions)
                print(f"  └─ 文档 {doc_id}: 词频={freq}, 位置={positions}")

    def display_statistics(self):
        """显示索引统计信息"""
        print("\n" + "="*80)
        print("索引统计信息")
        print("="*80)
        print(f"文档总数: {len(self.documents)}")
        print(f"词项总数: {len(self.index)}")
        print(f"平均文档长度: {sum(self.doc_lengths.values()) / len(self.doc_lengths) if self.doc_lengths else 0:.2f}")

        # 最常见的词项
        term_doc_counts = [(term, len(postings)) for term, postings in self.index.items()]
        term_doc_counts.sort(key=lambda x: x[1], reverse=True)

        print("\n最常见的词项 (按文档频率):")
        for term, count in term_doc_counts[:10]:
            print(f"  {term}: {count} 个文档")

    def save_to_file(self, filename: str):
        """保存索引到文件"""
        data = {
            'index': {term: dict(postings) for term, postings in self.index.items()},
            'documents': self.documents,
            'doc_lengths': self.doc_lengths
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"\n索引已保存到: {filename}")

    def load_from_file(self, filename: str):
        """从文件加载索引"""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.index = defaultdict(lambda: defaultdict(list))
        for term, postings in data['index'].items():
            for doc_id, positions in postings.items():
                self.index[term][doc_id] = positions

        self.documents = data['documents']
        self.doc_lengths = data['doc_lengths']

        print(f"\n索引已从文件加载: {filename}")


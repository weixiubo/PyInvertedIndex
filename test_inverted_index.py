"""
倒排索引系统单元测试
验证所有核心功能的正确性
"""

import unittest
from inverted_index import InvertedIndex


class TestInvertedIndex(unittest.TestCase):
    """倒排索引测试类"""
    
    def setUp(self):
        """每个测试前的准备工作"""
        self.index = InvertedIndex()
        self.test_docs = {
            "doc1": "Information retrieval is important",
            "doc2": "Search engines use inverted index",
            "doc3": "Inverted index enables fast search",
            "doc4": "Database systems use index structures"
        }
        self.index.build_from_documents(self.test_docs)
    
    def test_document_addition(self):
        """测试文档添加"""
        self.assertEqual(len(self.index.documents), 4)
        self.assertIn("doc1", self.index.documents)
        self.assertIn("doc2", self.index.documents)
    
    def test_preprocessing(self):
        """测试文本预处理"""
        text = "The Quick BROWN fox"
        tokens = self.index.preprocess(text)
        # 应该转小写，去掉停用词"the"
        self.assertIn("quick", tokens)
        self.assertIn("brown", tokens)
        self.assertIn("fox", tokens)
        self.assertNotIn("the", tokens)
    
    def test_single_term_search(self):
        """测试单词查询"""
        result = self.index.search("index")
        self.assertIn("doc2", result)
        self.assertIn("doc3", result)
        self.assertIn("doc4", result)
        self.assertNotIn("doc1", result)
    
    def test_and_query(self):
        """测试AND查询"""
        result = self.index.search_and(["inverted", "index"])
        self.assertIn("doc2", result)
        self.assertIn("doc3", result)
        self.assertNotIn("doc1", result)
        self.assertNotIn("doc4", result)
    
    def test_or_query(self):
        """测试OR查询"""
        result = self.index.search_or(["search", "database"])
        self.assertIn("doc2", result)
        self.assertIn("doc3", result)
        self.assertIn("doc4", result)
        self.assertNotIn("doc1", result)
    
    def test_not_query(self):
        """测试NOT查询"""
        result = self.index.search_not(["index"], ["database"])
        self.assertIn("doc2", result)
        self.assertIn("doc3", result)
        self.assertNotIn("doc4", result)  # 包含database，应被排除
    
    def test_phrase_query(self):
        """测试短语查询"""
        result = self.index.search_phrase("inverted index")
        self.assertIn("doc2", result)
        self.assertIn("doc3", result)
        self.assertNotIn("doc1", result)
    
    def test_term_frequency(self):
        """测试词频统计"""
        tf = self.index.get_term_frequency("index", "doc2")
        self.assertEqual(tf, 1)
        
        # 测试不存在的词
        tf = self.index.get_term_frequency("nonexistent", "doc1")
        self.assertEqual(tf, 0)
    
    def test_document_frequency(self):
        """测试文档频率"""
        df = self.index.get_document_frequency("index")
        self.assertEqual(df, 3)  # doc2, doc3, doc4
        
        df = self.index.get_document_frequency("information")
        self.assertEqual(df, 1)  # 只在doc1
    
    def test_empty_query(self):
        """测试空查询"""
        result = self.index.search("")
        self.assertEqual(len(result), 0)
        
        result = self.index.search_and([])
        self.assertEqual(len(result), 0)
    
    def test_case_insensitive(self):
        """测试大小写不敏感"""
        result1 = self.index.search("INDEX")
        result2 = self.index.search("index")
        self.assertEqual(result1, result2)
    
    def test_position_tracking(self):
        """测试位置信息记录"""
        result = self.index.search("index")
        # 检查位置信息是否正确记录
        self.assertIsInstance(result["doc2"], list)
        self.assertTrue(len(result["doc2"]) > 0)
    
    def test_stop_words_removal(self):
        """测试停用词过滤"""
        # "is"是停用词，不应该在索引中
        result = self.index.search("is")
        self.assertEqual(len(result), 0)
    
    def test_phrase_query_order(self):
        """测试短语查询的顺序敏感性"""
        # "inverted index" 应该找到
        result1 = self.index.search_phrase("inverted index")
        self.assertTrue(len(result1) > 0)
        
        # "index inverted" 不应该找到（顺序相反）
        result2 = self.index.search_phrase("index inverted")
        self.assertEqual(len(result2), 0)


class TestIndexPersistence(unittest.TestCase):
    """测试索引持久化功能"""
    
    def test_save_and_load(self):
        """测试保存和加载索引"""
        # 创建并构建索引
        index1 = InvertedIndex()
        docs = {
            "doc1": "test document one",
            "doc2": "test document two"
        }
        index1.build_from_documents(docs)
        
        # 保存索引
        filename = "test_index.json"
        index1.save_to_file(filename)
        
        # 加载索引
        index2 = InvertedIndex()
        index2.load_from_file(filename)
        
        # 验证加载的索引
        self.assertEqual(len(index2.documents), 2)
        self.assertEqual(index2.documents["doc1"], "test document one")
        
        # 验证查询功能
        result = index2.search("test")
        self.assertIn("doc1", result)
        self.assertIn("doc2", result)
        
        # 清理测试文件
        import os
        if os.path.exists(filename):
            os.remove(filename)


def run_tests():
    """运行所有测试"""
    print("="*80)
    print("运行倒排索引系统单元测试")
    print("="*80)
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试
    suite.addTests(loader.loadTestsFromTestCase(TestInvertedIndex))
    suite.addTests(loader.loadTestsFromTestCase(TestIndexPersistence))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 打印总结
    print("\n" + "="*80)
    print("测试总结")
    print("="*80)
    print(f"运行测试数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✓ 所有测试通过!")
    else:
        print("\n✗ 部分测试失败")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()


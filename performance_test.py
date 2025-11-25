#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Performance testing for inverted index with Reuters-21578 dataset
"""

import time
import json
from inverted_index import InvertedIndex
from parse_reuters import load_reuters_documents

def test_index_building(doc_counts=[100, 500, 1000, 2000, 5000]):
    """
    Test index building time for different document counts
    
    Args:
        doc_counts: List of document counts to test
        
    Returns:
        Dict with performance results
    """
    print("="*80)
    print("Testing Index Building Performance")
    print("="*80)
    
    results = {
        'doc_counts': [],
        'build_times': [],
        'vocab_sizes': [],
        'total_terms': []
    }
    
    # Load all documents we might need
    max_docs = max(doc_counts)
    print(f"\nLoading up to {max_docs} documents from Reuters-21578...")
    all_documents = load_reuters_documents('data', max_docs=max_docs)
    
    for count in doc_counts:
        print(f"\n{'='*60}")
        print(f"Testing with {count} documents")
        print(f"{'='*60}")
        
        # Create new index
        index = InvertedIndex()
        
        # Measure build time
        start_time = time.time()
        
        for i, doc in enumerate(all_documents[:count]):
            index.add_document(doc['id'], doc['text'])
        
        build_time = time.time() - start_time
        
        # Get statistics
        vocab_size = len(index.index)
        total_terms = sum(len(docs) for docs in index.index.values())
        
        results['doc_counts'].append(count)
        results['build_times'].append(build_time)
        results['vocab_sizes'].append(vocab_size)
        results['total_terms'].append(total_terms)
        
        print(f"  Build time: {build_time:.3f} seconds")
        print(f"  Vocabulary size: {vocab_size:,} terms")
        print(f"  Total postings: {total_terms:,}")
        print(f"  Avg time per doc: {build_time/count*1000:.2f} ms")
    
    return results

def test_query_performance(num_docs=1000):
    """
    Test query performance for different query types
    
    Args:
        num_docs: Number of documents to use for testing
        
    Returns:
        Dict with query performance results
    """
    print("\n" + "="*80)
    print(f"Testing Query Performance ({num_docs} documents)")
    print("="*80)
    
    # Build index
    print(f"\nBuilding index with {num_docs} documents...")
    documents = load_reuters_documents('data', max_docs=num_docs)
    
    index = InvertedIndex()
    for doc in documents:
        index.add_document(doc['id'], doc['text'])
    
    print(f"Index built: {len(index.index):,} terms")
    
    # Test queries
    test_cases = [
        ('Single term', 'market', lambda: index.search('market')),
        ('Boolean AND', 'market AND trade', lambda: index.search('market AND trade')),
        ('Boolean OR', 'market OR trade', lambda: index.search('market OR trade')),
        ('Boolean NOT', 'market NOT trade', lambda: index.search('market NOT trade')),
        ('Phrase query', '"stock market"', lambda: index.search_phrase('stock market')),
    ]
    
    results = {
        'query_types': [],
        'query_times': [],
        'result_counts': []
    }
    
    print("\nQuery Performance:")
    print(f"{'Query Type':<20} {'Query':<25} {'Time (ms)':<12} {'Results':<10}")
    print("-" * 70)
    
    for query_type, query, query_func in test_cases:
        # Warm up
        query_func()
        
        # Measure time (average of 10 runs)
        times = []
        for _ in range(10):
            start = time.time()
            result = query_func()
            times.append((time.time() - start) * 1000)  # Convert to ms
        
        avg_time = sum(times) / len(times)
        result_count = len(result) if result else 0
        
        results['query_types'].append(query_type)
        results['query_times'].append(avg_time)
        results['result_counts'].append(result_count)
        
        print(f"{query_type:<20} {query:<25} {avg_time:>10.3f} ms {result_count:>8}")
    
    return results

def save_results(build_results, query_results, output_file='output/performance_results.json'):
    """Save performance test results to JSON file"""
    results = {
        'index_building': build_results,
        'query_performance': query_results
    }

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n✓ Results saved to {output_file}")

if __name__ == '__main__':
    # Test index building with different document counts
    build_results = test_index_building([100, 500, 1000, 2000, 5000])
    
    # Test query performance with 1000 documents
    query_results = test_query_performance(1000)
    
    # Save results
    save_results(build_results, query_results)
    
    print("\n" + "="*80)
    print("Performance testing completed!")
    print("="*80)


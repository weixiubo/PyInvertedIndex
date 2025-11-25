#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parse Reuters-21578 SGML files and extract document content
"""

import re
import os
from typing import List, Dict

def parse_reuters_sgml(file_path: str) -> List[Dict[str, str]]:
    """
    Parse a Reuters SGML file and extract documents
    
    Args:
        file_path: Path to the SGML file
        
    Returns:
        List of documents, each as a dict with 'id', 'title', and 'body'
    """
    with open(file_path, 'r', encoding='latin-1', errors='ignore') as f:
        content = f.read()
    
    documents = []
    
    # Find all REUTERS tags
    reuters_pattern = r'<REUTERS[^>]*>(.*?)</REUTERS>'
    reuters_matches = re.findall(reuters_pattern, content, re.DOTALL)
    
    for i, reuters_content in enumerate(reuters_matches):
        # Extract NEWID
        newid_match = re.search(r'NEWID="(\d+)"', content.split('</REUTERS>')[i])
        doc_id = newid_match.group(1) if newid_match else str(i)
        
        # Extract TITLE
        title_match = re.search(r'<TITLE>(.*?)</TITLE>', reuters_content, re.DOTALL)
        title = title_match.group(1).strip() if title_match else ""
        
        # Extract BODY
        body_match = re.search(r'<BODY>(.*?)</BODY>', reuters_content, re.DOTALL)
        body = body_match.group(1).strip() if body_match else ""
        
        # Only include documents with content
        if title or body:
            text = f"{title} {body}".strip()
            documents.append({
                'id': f'reuters_{doc_id}',
                'title': title,
                'body': body,
                'text': text
            })
    
    return documents

def load_reuters_documents(data_dir: str, max_docs: int = None) -> List[Dict[str, str]]:
    """
    Load Reuters documents from all SGML files
    
    Args:
        data_dir: Directory containing SGML files
        max_docs: Maximum number of documents to load (None for all)
        
    Returns:
        List of documents
    """
    all_documents = []
    
    # Find all SGML files
    sgm_files = sorted([f for f in os.listdir(data_dir) if f.endswith('.sgm')])
    
    for sgm_file in sgm_files:
        file_path = os.path.join(data_dir, sgm_file)
        print(f"Parsing {sgm_file}...")
        
        documents = parse_reuters_sgml(file_path)
        all_documents.extend(documents)
        
        # Check if we've reached the limit
        if max_docs and len(all_documents) >= max_docs:
            all_documents = all_documents[:max_docs]
            break
    
    print(f"Loaded {len(all_documents)} documents")
    return all_documents

if __name__ == '__main__':
    # Test parsing
    data_dir = '.'
    
    # Load first 100 documents for testing
    documents = load_reuters_documents(data_dir, max_docs=100)
    
    # Print sample
    if documents:
        print("\n" + "="*80)
        print("Sample document:")
        print("="*80)
        doc = documents[0]
        print(f"ID: {doc['id']}")
        print(f"Title: {doc['title'][:100]}...")
        print(f"Body: {doc['body'][:200]}...")
        print(f"Total text length: {len(doc['text'])} characters")


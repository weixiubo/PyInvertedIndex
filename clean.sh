#!/bin/bash
# 清理临时文件和缓存

echo "清理Python缓存文件..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
find . -type f -name "*.pyd" -delete

echo "清理pytest缓存..."
rm -rf .pytest_cache

echo "清理输出文件..."
rm -f inverted_index_data.json
rm -f output/*.json 2>/dev/null
rm -f output/*.txt 2>/dev/null

echo "清理IDE配置..."
rm -rf .vscode
rm -rf .idea
find . -type f -name "*.swp" -delete
find . -type f -name "*.swo" -delete
find . -type f -name "*~" -delete

echo "清理完成！✓"


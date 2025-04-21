# 檢查當前環境
import sys
print(f"Python version: {sys.version}")
print(f"Platform: {sys.platform}")

# 檢查 fastembed 的依賴
import pkg_resources
fastembed_dist = pkg_resources.working_set.by_key['fastembed']
print(f"fastembed version: {fastembed_dist.version}")
print("\nDependencies:")
for req in fastembed_dist.requires():
    print(f"- {req}")
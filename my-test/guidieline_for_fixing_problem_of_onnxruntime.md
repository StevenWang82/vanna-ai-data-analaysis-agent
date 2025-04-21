# ONNX Runtime 在 Windows 環境的安裝指南

## 問題描述
在 Python 中匯入 ONNX Runtime 時，可能會遇到以下錯誤：
- `DLL load failed while importing onnxruntime_pybind11_state`
- 關於不支援 Windows 版本的警告訊息 (因更新至24H2 -OS-build 26100.3775)

## 認識 ONNX Runtime
ONNX Runtime 是一個機器學習推論引擎，在 Vanna.AI 專案中主要由 `fastembed` 用於向量嵌入（vector embeddings）運算。這是 `qdrant-client[fastembed]` 套件的重要依賴項目。

## 版本相容性
根據 `fastembed` 依賴項分析：
```
onnxruntime!=1.20.0,>=1.17.0; python_version >= "3.10" and python_version < "3.13"
```
這表示：
- 需要 1.17.0 或更高版本 > 時測1.21.0版本，可解決此問題
- 排除 1.20.0 版本（已知問題）
- 支援 Python 3.10-3.12 版本

## 解決步驟

### 1. 清除現有安裝
```bash
pip uninstall -y onnxruntime onnxruntime-gpu
pip cache purge
```

### 2. 安裝正確版本
```bash
pip install onnxruntime==1.21.0
```

### 3. 更新專案依賴
在您的 Jupyter notebook 或 Python 腳本中：
```python
# 安裝必要套件
!pip install onnxruntime==1.21.0
!pip install vanna
!pip install "qdrant-client[fastembed]"
!pip install google-generativeai 
!pip install vertexai 
```

### 4. 處理警告訊息（如有需要）
如果遇到 Windows 版本相容性警告：
```python
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='onnxruntime')
```

## 故障排除建議

如果問題持續：
1. 安裝最新版本的 Visual C++ Redistributable
2. 添加環境變數：
   ```python
   import os
   os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'
   ```
3. 嘗試純 CPU 版本：
   ```bash
   pip install onnxruntime-cpu
   ```

## 系統需求
- Windows 10 或 11
- Python 3.10-3.12
- 最新版本的 Visual C++ Redistributable

## 補充說明
- 套件安裝後務必重新啟動 Jupyter kernel
- 建議使用虛擬環境以避免套件衝突
- 版本 1.21.0 已在 Windows 11 上測試並確認可正常運作

## 常見問題解答（FAQ）
Q: 為什麼要選擇 1.21.0 版本？
A: 此版本經過測試，能夠穩定運行於 Windows 11 環境，且避開了已知問題版本。

Q: 安裝後出現 Windows 版本警告怎麼辦？
A: 這個警告不影響實際功能，可以安全忽略或使用上述的警告過濾方式處理。

## 參考資源
- [Vanna.AI 官方文件](https://vanna.ai/docs/)
- [ONNX Runtime 官方文件](https://onnxruntime.ai/)
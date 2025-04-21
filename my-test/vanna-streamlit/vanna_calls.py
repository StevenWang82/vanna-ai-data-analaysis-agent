import streamlit as st
import os
from dotenv import load_dotenv

from vanna.qdrant import Qdrant_VectorStore
from qdrant_client import QdrantClient
from vanna.google import GoogleGeminiChat

# --- Define your Custom Vanna Class (Include FastEmbed) ---
#     (這個類別定義應該放在 setup_vanna 函數之外，在你的 .py 檔案頂部)
class MyVanna(Qdrant_VectorStore, GoogleGeminiChat):
    def __init__(self, config=None):
        # 分別初始化父類別，傳遞它們需要的 config 部分
        qdrant_config = {'client': config.get('client')} if config and 'client' in config else {}
        google_config = {'api_key': config.get('google_api_key'), 'model': config.get('google_model')} if config and 'google_api_key' in config else {}
        # FastEmbed 通常可以接受完整的 config，或使用預設值
        Qdrant_VectorStore.__init__(self, config=qdrant_config)
        GoogleGeminiChat.__init__(self, config=google_config)

# --- Concise setup_vanna for Streamlit ---
@st.cache_resource(ttl=3600) # 快取 Vanna 設定一小時
def setup_vanna():
    # 1. 從 st.secrets 獲取配置 (提供預設值)
    gemini_key = st.secrets.get("GEMINI_API_KEY")
    gemini_model = st.secrets.get("GEMINI_MODEL")
    q_host = st.secrets.get("QDRANT_HOST")
    q_port = st.secrets.get("QDRANT_PORT")
    q_key = st.secrets.get("QDRANT_API_KEY") # 可以是 None
    q_https = st.secrets.get("QDRANT_HTTPS")
    db_driver = st.secrets.get("DB_DRIVER")
    db_server = st.secrets.get("DB_SERVER")
    db_database = st.secrets.get("DB_DATABASE")
    db_user = st.secrets.get("DB_USERNAME") # 可以是 None
    db_pass = st.secrets.get("DB_PASSWORD") # 可以是 None

    # 2. 驗證必要配置是否存在
    if not all([gemini_key, db_server, db_database]):
        st.error("Missing required secrets: GEMINI_API_KEY, DB_SERVER, DB_DATABASE")
        st.stop() # 如果缺少關鍵配置則停止

    # 3. 初始化 Qdrant Client (簡化錯誤處理)
    try:
        q_client = QdrantClient(host=q_host, port=q_port, api_key=q_key, https=q_https)
    except Exception as e:
        st.error(f"Qdrant connection failed: {e}")
        st.stop()

    # 4. 準備 Vanna 配置並初始化
    vanna_config = {
        'client': q_client,                 # Qdrant client
        'google_api_key': gemini_key,       # Gemini key
        'google_model': gemini_model,       # Gemini model
        # 'model': 'BAAI/bge-small-en-v1.5' # 可選: 明確指定 FastEmbed 模型
    }
    try:
        vn = MyVanna(config=vanna_config)
    except Exception as e:
        st.error(f"Vanna initialization failed: {e}")
        st.stop()

    # 5. 建立資料庫連接字串
    conn_str = f"DRIVER={{{db_driver}}};SERVER={db_server};DATABASE={db_database};"
    if db_user and db_pass:
        conn_str += f"UID={db_user};PWD={db_pass};"
    else: # 假設 Windows 驗證
        conn_str += "Trusted_Connection=yes;"
    # 添加建議的連接選項 (根據需要調整)
    conn_str += "Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=30;"

    # 6. 連接到資料庫 (簡化錯誤處理)
    try:
        vn.connect_to_mssql(odbc_conn_str=conn_str)
    except Exception as e:
        st.error(f"MSSQL connection failed: {e}")
        st.stop()

    # 7. 返回設定好的 Vanna 實例
    return vn

@st.cache_data(show_spinner="Generating sample questions ...")
def generate_questions_cached():
    vn = setup_vanna()
    return vn.generate_questions()


@st.cache_data(show_spinner="Generating SQL query ...")
def generate_sql_cached(question: str):
    vn = setup_vanna()
    return vn.generate_sql(question=question, allow_llm_to_see_data=True)

@st.cache_data(show_spinner="Checking for valid SQL ...")
def is_sql_valid_cached(sql: str):
    vn = setup_vanna()
    return vn.is_sql_valid(sql=sql)

@st.cache_data(show_spinner="Running SQL query ...")
def run_sql_cached(sql: str):
    vn = setup_vanna()
    return vn.run_sql(sql=sql)

@st.cache_data(show_spinner="Checking if we should generate a chart ...")
def should_generate_chart_cached(question, sql, df):
    vn = setup_vanna()
    return vn.should_generate_chart(df=df)

@st.cache_data(show_spinner="Generating Plotly code ...")
def generate_plotly_code_cached(question, sql, df):
    vn = setup_vanna()
    code = vn.generate_plotly_code(question=question, sql=sql, df=df)
    return code


@st.cache_data(show_spinner="Running Plotly code ...")
def generate_plot_cached(code, df):
    vn = setup_vanna()
    return vn.get_plotly_figure(plotly_code=code, df=df)


@st.cache_data(show_spinner="Generating followup questions ...")
def generate_followup_cached(question, sql, df):
    vn = setup_vanna()
    return vn.generate_followup_questions(question=question, sql=sql, df=df)

@st.cache_data(show_spinner="Generating summary ...")
def generate_summary_cached(question, df):
    vn = setup_vanna()
    return vn.generate_summary(question=question, df=df)
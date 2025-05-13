import streamlit as st
import pandas as pd
from collections import Counter
import jieba
import re

st.set_page_config(page_title="主观题关键词分析工具", layout="wide")

st.title("📊 主观题关键词分析工具")

uploaded_file = st.file_uploader("请上传包含主观题内容的 Excel 文件（.xlsx）", type=["xlsx"])

def extract_keywords(texts, stopwords):
    all_words = []
    for text in texts:
        if pd.isna(text):
            continue
        text = re.sub(r'[^一-龥]', '', str(text))  # 只保留中文
        words = jieba.lcut(text)
        words = [w for w in words if w not in stopwords and len(w) > 1]
        all_words.extend(words)
    return Counter(all_words)

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("📄 数据预览：", df.head())

    # 选择主观题列
    text_column = st.selectbox("请选择主观题文本所在的列", df.columns)

    # 加载常见停用词（可自定义扩展）
    stopwords = set(["的", "了", "和", "是", "我", "也", "就", "在", "要", "会", "能", "不", "一个", "如何", "问题", "比较", "目前"])

    # 提取关键词
    keyword_counts = extract_keywords(df[text_column], stopwords)

    if keyword_counts:
        result_df = pd.DataFrame(keyword_counts.items(), columns=["关键词", "频次"])
        result_df.index += 1
        result_df.reset_index(inplace=True)
        result_df.rename(columns={"index": "序号"}, inplace=True)

        st.success("✅ 分析完成，结果如下：")
        st.dataframe(result_df)

        # 下载链接
        csv = result_df.to_csv(index=False, encoding="utf-8-sig")
        st.download_button("📥 下载关键词分析结果", data=csv, file_name="关键词分析结果.csv", mime="text/csv")
    else:
        st.warning("⚠️ 没有提取到关键词，请检查上传文件或文本内容。")

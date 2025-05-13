import streamlit as st
import pandas as pd
import jieba.analyse

# 简单的问题分类器
def classify_issue(text):
    if '招聘' in text:
        return '招聘问题'
    elif '留存' in text or '流失' in text:
        return '留存问题'
    elif 'M' in text and ('成长' in text or '能力' in text):
        return 'M成长问题'
    elif '带教' in text:
        return '带教能力问题'
    else:
        return '其他'

# 使用 TextRank 提取关键词
def extract_keywords(text, topK=5):
    return jieba.analyse.textrank(text, topK=topK, withWeight=False)

st.title("主观题关键词分析与自动分类工具")

uploaded_file = st.file_uploader("上传主观题Excel文件", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    if df.shape[1] > 1:
        st.warning("仅支持单列主观题分析，请上传只有一列主观题内容的表格")
    else:
        col_name = df.columns[0]
        df["关键词"] = df[col_name].astype(str).apply(lambda x: ", ".join(extract_keywords(x)))
        df["问题分类"] = df[col_name].astype(str).apply(classify_issue)
        st.dataframe(df)

        # 下载按钮
        st.download_button(
            label="下载分析结果",
            data=df.to_csv(index=False).encode('utf-8-sig'),
            file_name="主观题分析结果.csv",
            mime="text/csv"
        )
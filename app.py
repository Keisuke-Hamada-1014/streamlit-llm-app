from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
 
# .envファイルから環境変数を読み込む
load_dotenv()
 
# OpenAIのLLMを設定
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
 
# Streamlit UI
st.title("LLM機能を搭載したWebアプリ")
 
st.write("動作モードに応じて、LLMが質問に答えます。")
 
selected_mode = st.radio(
    "動作モードを選択してください。",
    ["一般的な質問", "テキスト修正"]
)
 
user_input = st.text_area("テキストを入力してください。")
 
if st.button("実行"):
    st.divider()
    st.write("実行中...")
 
    if not user_input:
        st.error("テキストを入力してください。")
    else:
        # Systemメッセージを処理モードに応じて切り替え
        if selected_mode == "一般的な質問":
            system_prompt = "あなたは優秀なAIアシスタントです。ユーザーの質問に正確に答えてください。"
        elif selected_mode == "テキスト修正":
            system_prompt = "あなたはプロの編集者です。ユーザーが入力した文章を適切に修正してください。"
        else:
            system_prompt = "あなたは親切なAIです。"
 
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input)
        ]
 
        try:
            result = llm(messages)
            st.success("LLMの回答：")
            st.write(result.content)
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
 
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# .envファイルから環境変数を読み込む
load_dotenv()

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

st.title("LLM機能を搭載したWebアプリ")
st.write("動作モードに応じて、LLMが真剣に答えます。")

selected_mode = st.radio(
    "動作モードを選択してください。",
    ["一般的な質問", "占いモード（たぶん当たる😎）"]
)
if selected_mode == "一般的な質問":
    input_text = st.text_area("質問を入力してください。")
else:
    input_birthdate = st.date_input("生年月日を選択してください")

# 関数とメッセージ定義
def path_number(year: int, month: int, day: int) -> int:
    digits = list(str(year) + f"{month:02d}" + f"{day:02d}")
    total = sum(int(d) for d in digits)
    while total > 9:
        total = sum(int(d) for d in str(total))
    return total

PATH_MESSAGES = {
    1: "あなたはリーダーシップが強く、自立心あふれるタイプです。たぶん",
    2: "あなたは協調性が高く、人の気持ちに寄り添える優しい心の持ち主です。たぶん",
    3: "あなたはクリエイティブで表現力が豊か。周囲を明るく照らします。たぶん",
    4: "あなたは堅実で計画的。安定を重視し、地道な努力が得意です。たぶん",
    5: "あなたは自由を愛し、変化を楽しむ冒険家タイプです。たぶん",
    6: "あなたは家庭的で世話好き。周囲から信頼される頼れる存在です。たぶん",
    7: "あなたは知的好奇心旺盛で、探求心・洞察力に優れています。たぶん",
    8: "あなたはビジネスセンスがあり、実利を追求する力があります。たぶん",
    9: "あなたは博愛精神にあふれ、人道的・慈愛に満ちた人です。たぶん",
}


if st.button("実行"):
    st.divider()

    if selected_mode == "一般的な質問":
        if not input_text:
            st.error("テキストを入力してください。")
        else:
            system_prompt = "あなたは優秀なAIアシスタントです。ユーザーの質問に正確に答えてください。"
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=input_text)
            ]
            try:
                result = llm(messages)
                st.success("LLMの回答：")
                st.write(result.content)
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")

    else:
        # ここから占いモード
        if not input_birthdate:
            st.error("生年月日を選択してください。")
        else:
            y, m, d = input_birthdate.year, input_birthdate.month, input_birthdate.day
            num = path_number(y, m, d)
            message = PATH_MESSAGES.get(num, "不明な生年月日です。")
            st.success("あなたの生年月日占い🔮")
            st.write(f"占い結果：{message}")
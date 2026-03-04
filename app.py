import streamlit as st
import openai

st.set_page_config(page_title="Ci-enエロ特化記事生成", layout="centered")

st.title("🔥 Ci-en新作紹介・生成エディタ")
st.caption("かずたまそふと流の紹介文を自動生成します")

# サイドバーでAPIキーを設定
with st.sidebar:
    st.header("API設定")
    api_key = st.text_input("OpenAI API Key", type="password")

# 入力フォーム
with st.form("article_form"):
    title = st.text_input("作品タイトル")
    cast = st.text_input("キャスト（声優）")
    illust = st.text_input("イラストレーター")
    scenario = st.text_input("シナリオ")
    audio_edit = st.text_input("音声編集")
    summary = st.text_area("作品のストーリー・性癖・コンセプト", height=200)
    dlsite_url = st.text_input("販売URL")
    
    submitted = st.form_submit_button("記事を生成する")

if submitted:
    final_api_key = st.secrets.get("OPENAI_API_KEY") or api_key
    
    if not final_api_key:
        st.error("APIキーを設定してください。")
    else:
        try:
            client = openai.OpenAI(api_key=final_api_key)
            
            # システムプロンプトの設定
            system_msg = """あなたは成人向け音声作品のプロデューサー「かずたまそふと」です。
以下の【執筆方針】を読み、ファンに語りかけるような「柔らかく、親しみやすい口調」でCi-en記事を作成してください。

【執筆方針】
1. 挨拶：冒頭は「こんにちは🫧 かずたまそふとです🫧」で始め、読者への感謝や近況をゆるく語る。
2. 口調：丁寧すぎず、友達やファンに話しかけるような親近感のある言葉遣いにする。「～です・ます」だけでなく、「～ですね」「～かもです」「～でした（笑）」などを混ぜる。
3. 制作裏話：苦労話も「いや～、実は今回大変で…」といった風に、制作の熱量を等身大で伝える。
4. クリエイター紹介：形式的な紹介ではなく「〇〇様の声、本当にすごくて感動しました…」「〇〇先生のイラスト、見た瞬間に声が出ました」といった、あなたの素直な感想として書く。
5. セリフと描写：ヒロインのセリフは印象的に。地の文も「……ぜひ、その耳で確かめてみてください👀」のように、読者の期待感を煽る書き方にする。
6. 締め：最後は「あなたの心に残るヒロインと物語に出会えますように。」で優しく結ぶ。

【参考にする過去記事の空気感】
「気づいたら収録日迫っていて爆速で台本書き上げました。もはや懐かしい記憶。」
「浴衣のデザインが秀逸すぎて声出ました。」
「声優さんってすごい。」

【出力ルール】
- Markdown形式を維持。
- セリフの色指定：**<span style="color: #2196f3">「セリフ」</span>**
- 重要な単語の色指定：<span style="color: #e57373">キーワード</span>
"""
            
            user_msg = f"""
タイトル: {title}
キャスト: {cast}
イラスト: {illust}
シナリオ: {scenario}
音声編集: {audio_edit}
内容詳細: {summary}
URL: {dlsite_url}
"""

            with st.spinner("AIが執筆中..."):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": user_msg}
                    ],
                    temperature=0.7
                )
                
            generated_html = response.choices[0].message.content
            
            st.subheader("生成結果プレビュー")
            st.markdown(generated_html, unsafe_allow_html=True)
            
            st.subheader("コピー用Markdownコード")
            st.code(generated_html, language="markdown")
            
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

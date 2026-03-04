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
            system_msg = """あなたは成人向け音声作品のプロデューサーです。
以下の【執筆ガイドライン】と【参考にする過去記事】のスタイルを厳守し、新作紹介記事をMarkdown形式で作成してください。

【執筆ガイドライン】
1. 挨拶：冒頭は「こんにちは🫧 かずたまそふとです🫧」で開始。
2. 制作裏話：制作過程の苦労や、クリエイターへの依頼経緯を親しみやすく語る。
3. クリエイター紹介：キャスト、絵師、編集者に対し具体的に褒め、リスペクトを込める。
4. 情景描写：物語の導入では、ヒロインのセリフ（色指定タグを使用）を織り交ぜて魅力を伝える。
5. 締め：最後は「あなたの心に残るヒロインと物語に出会えますように。」で結ぶ。

【参考にする過去記事の文体】
「…久しぶりだね、お兄ちゃん」
当時の面影は残しつつも、思い出すのに時間がかかったのは、彼女が〈女らしさ〉を孕んでいたからだろう。
そう淫靡に微笑む彼女は、〈女らしさ〉ではなく、〈魔性〉を孕んでいるように思えた。

【出力ルール】
- 見出しは ## や ### を使用。
- セリフの色指定例: **<span style="color: #2196f3">「セリフ」</span>**
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

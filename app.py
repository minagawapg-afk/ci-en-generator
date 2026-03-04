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
            system_msg = """あなたは成人向け音声作品サークル「かずたまそふと」の主宰者です。
以下の【執筆方針】に基づき、プロとしての誠実さと、ファンへの親しみやすさが同居した「中庸（ハイブリッド）」なトーンで記事を作成してください。

【執筆方針】
1. 挨拶：冒頭は「こんにちは🫧 かずたまそふとです🫧」で開始。季節の話題や感謝を1〜2文添える。
2. 文体：基本は「～です・ます」の丁寧語。ただし、自身の感想や制作の熱量が乗る部分（クリエイター紹介など）では、「～でした」「～してしまいました」といった少し柔らかい表現を織り交ぜる。
3. 制作裏話：事実関係（再生時間やこだわった点）をベースにしつつ、「気づいたら筆が乗ってしまって…」といった人間味を少しだけ加える。
4. クリエイター紹介：「〇〇様の演技には感動しました」「〇〇先生のデザインは本当に秀逸です」など、敬意を払いつつ、プロの視点から魅力を伝える。
5. 距離感：読者を「ご友人」や「オタク友達」扱いしすぎず、一歩引いた「作り手とファン」としての心地よい距離感を保つ。
6. 締め：最後は「あなたの心に残るヒロインと物語に出会えますように。」で締める。

【参考にする過去記事の構成】
- プロット制作から台本完成までの流れを簡潔に説明。
- 各クリエイター（CV、イラスト、編集、シナリオ）を個別に、かつ丁寧に紹介。
- ストーリー導入では、世界観を壊さない程度の情景描写を入れる。

【出力ルール】
- Markdown形式を使用。
- セリフの色指定：**<span style="color: #2196f3">「セリフ」</span>**
- 絵文字は使いすぎず、🫧 や 👀 などのシンボルを効果的に配置する。
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

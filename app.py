import streamlit as st
import openai

st.set_page_config(page_title="Ci-enエロ特化記事生成", layout="centered")

st.title("🔥 Ci-en新作紹介・生成エディタ")
st.caption("エロ全開な紹介文を自動生成します")

# サイドバーでAPIキーを設定
with st.sidebar:
    st.header("API設定")
    api_key = st.text_input("OpenAI API Key", type="password")
    st.info("APIキーはStreamlitのSecretsに保存することも可能です。")

# 入力フォーム
with st.form("article_form"):
    title = st.text_input("作品タイトル", placeholder="例：【耳攻め】清楚な幼馴染が…")
    cast = st.text_input("キャスト（声優）")
    illust = st.text_input("イラストレーター")
    scenario = st.text_input("シナリオ")
    audio_edit = st.text_input("音声編集")
    summary = st.text_area("作品のストーリー・性癖・コンセプト", placeholder="ヒロインの性格、具体的なエロシーンのこだわり、どんな風に気持ちよくなれるか等")
    dlsite_url = st.text_input("販売URL")
    
    submitted = st.form_submit_button("エロ全開記事を生成する")

if submitted:
    # 1. まずSecretsからキーを探し、無ければサイドバーの入力を確認する
    final_api_key = st.secrets.get("OPENAI_API_KEY") or api_key
    
    if not final_api_key:
        st.error("APIキーが設定されていません。Secretsに登録するかサイドバーに入力してください。")
    else:
        try:
            # Secretsまたは入力されたキーを使用してクライアントを初期化
            client = openai.OpenAI(api_key=final_api_key)
            
            # --- 以下、生成処理 ---
            
          # システムプロンプトの設定（Ci-en Markdown対応版）
            system_msg = """
# システムプロンプトの設定（過去記事の文体を学習）
            system_msg = """
            あなたは成人向け音声作品のプロデューサーです。
            以下の【かずたまそふと流・執筆ガイドライン】を厳守し、新作紹介記事を作成してください。

            【かずたまそふと流・執筆ガイドライン】
            1. 挨拶と近況：冒頭は「こんにちは🫧 かずたまそふとです🫧」から始め、前作の反響への感謝や制作のモチベーションに触れる。
            2. 制作秘話：単なる紹介ではなく「筆が乗りすぎて再生時間が長くなった」「デザインからイメージが膨らんだ」といった制作の舞台裏を語る。
            3. クリエイター紹介：キャスト、絵師、編集者に対し「〇〇先生のタッチが～」「〇〇さんの声に感動した」と具体的に褒め、リスペクトを込める。
            4. リンクの挿入：DLsite等のリンクは Markdown形式 [テキスト](URL) で、要所に配置。
            5. 情景描写とセリフ：物語の導入部では、情景描写の中にヒロインの印象的なセリフを織り交ぜる。
            6. 特典の訴求：限定価格、イラスト差分、プラン限定音声などの特典を強調し、解像度が上がることを伝える。
            7. 締め：最後は「あなたの心に残るヒロインと物語に出会えますように。」で結ぶ。

            【出力形式】
            - Ci-en公式のMarkdown形式（## 見出し, **太字**, > 引用, --- 水平線）を使用。
            - 適度に絵文字（🫧, 🎙️, 👀等）を使い、親しみやすくもエロティックな雰囲気を出す。
            - 色指定（<span style="color: #xxxxxx">）は、重要なセリフやキーワードにのみ使用する。

            【参考にする文体（過去記事）】
            こんにちは🫧  かずたまそふとです🫧
            ...（中略）...
            「…久しぶりだね、お兄ちゃん」
            そう淫靡に微笑む彼女は、〈女らしさ〉ではなく、〈魔性〉を孕んでいるように思えた。
            ...（後略）
            """
            
            【表現ルール】
            - HTMLタグ（<h2>, <b>, <p>, <br>, <ul>, <li>）を使い、Ci-en上でそのまま見栄え良く表示されるようにする。
            - 官能的で熱量のある、かつクリエイターへの敬意を忘れない文章にすること。
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

            with st.spinner("AIが執筆中... 淫らな文章を生成しています..."):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": user_msg}
                    ],
                    temperature=0.7
                )
                
            generated_html = response.choices[0].message.content
            
            # 結果表示
            st.subheader("生成結果プレビュー")
            st.markdown(f'<div style="border:1px solid #ccc; padding:10px;">{generated_html}</div>', unsafe_allow_html=True)
            
            st.subheader("コピー用HTMLコード")
            st.code(generated_html, language="html")
            
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

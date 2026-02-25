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
            
            # システムプロンプトの設定
            system_msg = """
            あなたは成人向け音声作品のプロモーションの達人です。
            ユーザーが入力した情報を元に、読者の性欲と購買意欲を最大化させるCi-en用記事を作成してください。
            
            【構成ルール】
            1. 導入：シチュエーションを想起させるエロい導入文から開始（読者の股間に響く表現を）。
            2. 販売リンク1：最初のURL提示。
            3. おすすめ対象：入力内容から性癖・ジャンルを分析し「こんなシチュエーション、ヒロインが好きな人におすすめ」という見出しで箇条書き。
            4. 制作陣紹介：キャスト、イラスト、シナリオ、音声編集を魅力的に紹介。
            5. あらすじ詳細：より深く、没入感を高めるストーリー説明。
            6. 販売リンク2：締めのURL提示。
            
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

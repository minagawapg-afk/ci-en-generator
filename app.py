import streamlit as st

st.set_page_config(page_title="Ci-en記事生成ツール", layout="centered")

st.title("🎨 Ci-en記事生成エディタ")
st.caption("情報を入力して、投稿用HTMLを生成します")

# サイドバーに設定項目を置くのもスッキリしておすすめです
with st.sidebar:
    st.header("基本設定")
    api_key = st.text_input("OpenAI API Key", type="password")

# メインの入力フォーム
with st.form("my_form"):
    title = st.text_input("作品タイトル", placeholder="例：【音声】ボクの幼馴染が○○する話")
    cast = st.text_input("キャスト（声優）", placeholder="例：桃色さくら")
    illust = st.text_input("イラストレーター", placeholder="例：山田太郎")
    
    # --- ここを追加 ---
    scenario = st.text_input("シナリオ", placeholder="例：海野幸子")
    audio_edit = st.text_input("音声編集", placeholder="例：スタジオ音吉")
    # ------------------
    
    summary = st.text_area("あらすじ・紹介文", placeholder="作品の魅力を自由に記入してください")
    dlsite_url = st.text_input("販売URL", placeholder="https://www.dlsite.com/...") # URL入力も追加しておくと便利です
    
    submitted = st.form_submit_button("HTMLを生成する")

if submitted:
    # プレビュー用の表示も修正
    preview_html = f"""
    <h2>{title}</h2>
    <p><b>CV:</b> {cast}</p>
    <p><b>Illust:</b> {illust}</p>
    <p><b>Scenario:</b> {scenario}</p>
    <p><b>Audio Edit:</b> {audio_edit}</p>
    <hr>
    <p>{summary}</p>
    <p><a href="{dlsite_url}">作品詳細はこちら</a></p>
    """
    
    st.subheader("生成結果プレビュー")
    st.markdown(preview_html, unsafe_allow_html=True)
    
    st.subheader("コピー用HTMLコード")
    st.code(preview_html, language="html")

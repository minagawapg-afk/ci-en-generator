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
    summary = st.text_area("あらすじ・紹介文", placeholder="作品の魅力を自由に記入してください")
    
    submitted = st.form_submit_button("HTMLを生成する")

if submitted:
    if not api_key:
        st.error("APIキーを入力してください")
    else:
        # ここに後でプロンプトを組み込みます
        # 現時点ではプレースホルダーを表示
        st.info("ここにAIが生成した文章が表示されるようになります。")
        
        # プレビュー用のHTML表示
        preview_html = f"<h2>{title}</h2><p>CV:{cast}</p><p>Illust:{illust}</p><hr><p>{summary}</p>"
        st.subheader("生成結果プレビュー")
        st.markdown(preview_html, unsafe_allow_html=True)
        
        st.subheader("コピー用HTMLコード")
        st.code(preview_html, language="html")

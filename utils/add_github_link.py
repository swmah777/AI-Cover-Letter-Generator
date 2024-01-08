def add_github_link(st, github_repo_url):
    # Large space to push the content to the bottom
    st.sidebar.markdown('<br>'*(10), unsafe_allow_html=True)


    github_button_markdown = f"""
    Github Repo: 
    <a href="{github_repo_url}" target="_blank">
        <img src="https://img.shields.io/github/stars/{github_repo_url.split('/')[-2]}/{github_repo_url.split('/')[-1]}?style=social" alt="GitHub Repo stars">
    </a>"""
    st.sidebar.markdown(github_button_markdown, unsafe_allow_html=True)
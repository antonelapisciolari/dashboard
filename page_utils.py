from variables import title, page_icon, companyIcon
def apply_page_config(st):
    st.set_page_config(
        page_title=title,
        page_icon=page_icon,  # You can use an emoji or a URL to an icon image
        layout="wide"  # Optional: You can set the layout as "centered" or "wide"
    )

    st.logo(
        companyIcon)
    

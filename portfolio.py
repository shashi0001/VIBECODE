import streamlit as st

st.set_page_config(page_title="My Portfolio", layout="centered")

st.title("👤 My Professional Portfolio")

# Upload display picture
profile_pic = st.file_uploader("Upload a Display Picture", type=["png", "jpg", "jpeg"])
if profile_pic:
    st.image(profile_pic, width=150)

# Skills
st.header("🛠️ Skills")
skills = st.text_area("List your skills:")
if skills:
    st.write(skills)

# Achievements
st.header("🏆 Achievements")
achievement = st.text_area("Describe an achievement:")
achievement_image = st.file_uploader("Upload an image for this achievement", type=["png", "jpg", "jpeg"])

if st.button("Add Achievement"):
    st.success("Achievement added!")
    if achievement:
        st.write(achievement)
    if achievement_image:
        st.image(achievement_image, width=300)

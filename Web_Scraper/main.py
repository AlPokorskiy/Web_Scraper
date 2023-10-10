import streamlit as st
import json
from io import StringIO
from bs4 import BeautifulSoup

st.title("HTML Scrapper")
st.text("In order to utilize this tool please read the following "
        "\n 1. Go to the desired LinkedIn or any other post page"
        "\n 2. Right click on the webpage and click Save-as "
        "\n 3. Save it somewhere where you can find that file such "
        "\n    as C:\\Users\\username\\Downloads or C:\Temp"
        "\n 4. Finally quickly browse for the file and select it here"
        "\n 5. Finally once the process is done you can save the file as "
        "\n   a JSONL formatted file and utilize it as needed")

st.write("Enter webpage info")
page_options = st.selectbox("Web page source", ("LinkedIn", "Twitter"))
tag_options = st.selectbox("Select tag you want to scrap by",
                           ("Marketing", "Sales", "Operations", "Tech", "SAAS", "AI", "Self Development",
                            "Leadership", "Growth Hacking", "Bio Hacking", "Fitness", "Health", "Travel",
                            "Business", "Finances"))
emojis = st.radio("Would you like to keep emojis?", ["Yes","No"])
# File upload
upload_file = st.file_uploader("Choose HTML File")


def extract_html(html_content):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all <span> tags with the attribute dir="ltr" and extract their inner content
    span_content = [span.get_text(separator=' ', strip=True) for span in soup.find_all('span', attrs={"dir": "ltr"})]

    post_content_only = [content for content in span_content if len(content.split()) > 10]

    return post_content_only


def save_jsonl(posts, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        for post in posts:
            # re-adjust this section to fit the OpenAI Prompt JSONL formatting
            if emojis == "Yes":
                file.write(json.dumps({"messages": [
                    {"role": "system", "content": "You are a helpful and chatbot, and you are great at writing posts."},
                    {"role": "user", "content": f"Please create a post for {tag_options} for {page_options} and include emojis"},
                    {"role": "assistant", "content": post}]}))

                file.write("\n")
            elif emojis == "No":
                file.write(json.dumps({"messages": [
                    {"role": "system", "content": "You are a helpful and chatbot, and you are great at writing posts."},
                    {"role": "user", "content": f"Please create a post for a {tag_options} for {page_options} "
                                                f"and without any emojis"},
                    {"role": "assistant", "content": post}]}))

                file.write("\n")


if __name__ == "__main__" and upload_file is not None:
    data = upload_file.getvalue()
    stringio = StringIO(upload_file.getvalue().decode("utf-8"))
    st.write("Name: ", upload_file.name)
    st.write("Status: Complete upload")

    content = stringio.read()

    btn_save = st.button("Save as JSONL", type="primary",
                         on_click=save_jsonl(extract_html(content), f"{tag_options}_dataset.jsonl"))
else:
    st.write("Status: Failed to upload, awaiting upload")

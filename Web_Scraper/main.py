import streamlit as st
import json
import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup

upload_file = st.file_uploader("Choose HTML File")

st.text("In order to utilize this tool please read the following "
        "\n 1. Go to the desired LinkedIn or any other post page"
        "\n 2. Right click on the webpage and click Save-as "
        "\n 3. Save it somewhere where you can find that file such "
        "\n    as C:\\Users\\username\\Downloads or C:\Temp"
        "\n 4. Finally quickly browse for the file and select it here"
        "\n 5. Finally once the process is done you can save the file as a JSONL formatted file and utilize it as needed")


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
            file.write(json.dumps({"post": post}))
            file.write("\n")


if __name__ == "__main__" and upload_file is not None:
    data = upload_file.getvalue()

    stringio = StringIO(upload_file.getvalue().decode("utf-8"))
    st.write("Name: ", upload_file.name)
    st.write("Status: Complete upload")

    content = stringio.read()

    btn_save = st.button("Save as JSONL", type="primary", on_click=save_jsonl(extract_html(content), "output.jsonl"))
else:
    st.write("Status: Failed to upload, awaiting upload")

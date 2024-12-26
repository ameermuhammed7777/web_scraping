import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_file_links(base_url, file_extensions=None):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching the URL: {e}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    file_links = set()
    for link in links:
        href = link.get('href')
        full_url = urljoin(base_url, href)
        if file_extensions:
            if any(full_url.endswith(ext) for ext in file_extensions):
                file_links.add(full_url)
        else:
            file_links.add(full_url)
    return file_links

def main():
    st.title("File Link Fetcher")
    st.write("Enter a URL to download pdf file links.")
    url = st.text_input("Enter URL", "")
    file_extensions = ['.pdf', '.xlsx', '.docx', '.zip', '.csv', '.jpg', '.mp4', '.rar', '.json', '.py']
    if st.button("Fetch File Links"):
        if url.strip() == "":
            st.error("Please enter a valid URL.")
        else:
            st.write("Fetching file links...")
            files = fetch_file_links(url, file_extensions)
            if not files:
                st.warning("No files found.")
            else:
                st.success("Files fetched successfully!")
                for file_url in files:
                    st.write(f"[{file_url}]({file_url})") 
                    
if __name__ == "__main__":
    main()

# ingestion/arxiv_utils.py
import feedparser
import requests
import os
from urllib.parse import quote
from ingestion.parser import extract_text_from_pdf, extract_assumptions

ARXIV_DOWNLOAD_DIR = "papers"
os.makedirs(ARXIV_DOWNLOAD_DIR, exist_ok=True)

def fetch_arxiv_papers(query="synthetic reasoning", max_results=5):
    encoded_query = quote(query)
    url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results={max_results}"
    headers = {"User-Agent": "ARS-Agent/1.0"}
    feed = feedparser.parse(url)

    papers = []
    for entry in feed.entries:
        paper_path = os.path.join(ARXIV_DOWNLOAD_DIR, f"{entry.id.replace('/','_')}.pdf")
        if not os.path.exists(paper_path):
            try:
                pdf_url = entry.link.replace('abs', 'pdf') + ".pdf"
                r = requests.get(pdf_url, headers=headers)
                with open(paper_path, "wb") as f:
                    f.write(r.content)
            except Exception as e:
                print(f"Failed to download {entry.id}: {e}")
                continue

        text = extract_text_from_pdf(paper_path)
        assumptions = extract_assumptions(text)
        papers.append({
            "id": entry.id,
            "title": entry.title,
            "link": entry.link,
            "assumptions": assumptions,
            "text": text
        })
    return papers

def fetch_local_papers():
    # Fallback to local PDFs
    papers = []
    for file in os.listdir(ARXIV_DOWNLOAD_DIR):
        if file.endswith(".pdf"):
            path = os.path.join(ARXIV_DOWNLOAD_DIR, file)
            text = extract_text_from_pdf(path)
            assumptions = extract_assumptions(text)
            papers.append({
                "id": file.replace(".pdf",""),
                "title": file,
                "link": "",
                "assumptions": assumptions,
                "text": text
            })
    return papers


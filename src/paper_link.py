import xml.etree.ElementTree as ET
import requests
import time

def add_url_by_Arxiv_search(library):
    count = 0
    succeed = 0
    for paper in library.entries:
        count += 1
        if 'url' not in paper:
            print(f"Missing URL for {paper['ID']}, \"{paper['title']}\". Searching for URL...")
            # search for URL
            title = paper['title']
            title_replaced = title.replace(" ", "+")
            query = f"http://export.arxiv.org/api/query?search_query=ti:{title_replaced}&sortBy=relevance&max_results=50"
            response = requests.get(query)
            root = ET.fromstring(response.content)
            entrys = root.findall('{http://www.w3.org/2005/Atom}entry')
            for entry in entrys:
                link = entry.find('{http://www.w3.org/2005/Atom}link')
                titlefound = entry.find('{http://www.w3.org/2005/Atom}title')
                if link is not None:
                    if title.lower() != titlefound.text.lower().replace("\n ", ""):
                        print(f"Title found for {paper['ID']} does not match: \"{titlefound.text}\", rejected.")
                    else:
                        paper['url'] = link.attrib['href']
                        succeed += 1
                        print(f"Found URL for {paper['ID']}, \"{paper['title']}\": {paper['url']}, title found: \"{titlefound.text}\", accepted.")
                        break
                else:
                    print(f"Could not find URL for {paper['ID']}.")
            else:
                print(f"Could not find URL for {paper['ID']}.")
        else:
            print(f"URL already exists for {paper['ID']}, \"{paper['title']}\".")
            succeed += 1
        print("\n")
    print(f"Found {succeed} URLs out of {count} papers.")

            
def add_url_by_Arxiv_number(library):
    count = 0
    succeed = 0
    for paper in library.entries:
        count += 1
        if 'url' not in paper:
            print(f"Missing URL for {paper['ID']}, \"{paper['title']}\". Searching for URL...")
            # search for URL
            if 'journal' in paper:
                journal = paper['journal']
                if 'arXiv' in journal:
                    arxiv_number = journal.split('arXiv:')[1].split(' ')[0]
                    print(f"Arxiv number found for {paper['ID']}: {arxiv_number}.")
                    paper['url'] = f"https://arxiv.org/abs/{arxiv_number}"
                    print(f"Found URL for {paper['ID']}, \"{paper['title']}\": {paper['url']}, accepted.")
                    succeed += 1
                else:
                    print(f"Arxiv number not found for {paper['ID']}.")
            else:
                print(f"Journal not found for {paper['ID']}.")
        else:
            print(f"URL already exists for {paper['ID']}, \"{paper['title']}\".")
            succeed += 1
        print("\n")
    print(f"Found {succeed} URLs out of {count} papers.")


def add_url_by_doi(library):
    count = 0
    succeed = 0
    for paper in library.entries:
        count += 1
        if 'url' not in paper:
            print(f"Missing URL for {paper['ID']}, \"{paper['title']}\". Searching for URL...")
            # search for URL
            if 'doi' in paper:
                doi = paper['doi']
                print(f"DOI found for {paper['ID']}: {doi}.")
                paper['url'] = f"https://doi.org/{doi}"
                print(f"Found URL for {paper['ID']}, \"{paper['title']}\": {paper['url']}, accepted.")
                succeed += 1
            else:
                print(f"DOI not found for {paper['ID']}.")
        else:
            print(f"URL already exists for {paper['ID']}, \"{paper['title']}\".")
            succeed += 1
        print("\n")
    print(f"Found {succeed} URLs out of {count} papers.")


def add_url_by_scholar_search(library, semantics_scholar_api_key = None):
        # Semantics Scholar Search
    count = 0
    succeed = 0

    if semantics_scholar_api_key is not None:
        headers = {
            "x-api-key": semantics_scholar_api_key
        }
    else:
        headers = {}

    for paper in library.entries:
        count += 1
        if 'url' not in paper:
            print(f"Missing URL for {paper['ID']}, \"{paper['title']}\". Searching for URL...")
            # search for URL
            title = paper['title']
            query = f"https://api.semanticscholar.org/graph/v1/paper/search/match?query={title}"
            while True:
                time.sleep(1)
                response = requests.get(query, headers=headers)
                if response.status_code == 200 or response.status_code == 404:
                    break
            if response.status_code == 404:
                print(f"Could not find URL for {paper['ID']}.\n")
                continue
            response_json = response.json()
            print(response_json)
            if response_json['data'] == []:
                print(f"Could not find URL for {paper['ID']}.\n")
                continue
            else:
                paperID = response_json['data'][0]['paperId']
                query_new = f"https://api.semanticscholar.org/graph/v1/paper/{paperID}?fields=url,openAccessPdf"
                while True:
                    time.sleep(1)
                    response_new = requests.get(query_new, headers=headers)
                    if response_new.status_code == 200 or response_new.status_code == 404:
                        break
                if response_new.status_code == 404:
                    print(f"Could not find URL for {paper['ID']}.\n")
                    continue
                response_new_json = response_new.json()
                scholar_url = response_new_json['url']
                if "openAccessPdf" in response_new_json and response_new_json['openAccessPdf'] is not None:
                    paper['url'] = response_new_json['openAccessPdf']['url']
                    print(f"Found URL for {paper['ID']}, \"{paper['title']}\": {paper['url']}, accepted.")
                else:
                    paper['url'] = scholar_url
                    print(f"Found URL for {paper['ID']}, \"{paper['title']}\": {paper['url']}, accepted.")
                succeed += 1
        else:
            print(f"URL already exists for {paper['ID']}, \"{paper['title']}\".")
            succeed += 1
        print("\n")
    print(f"Found {succeed} URLs out of {count} papers.")


def final_scan(library):
    print("\n\n Result of Url Search:")
    count = 0 
    found_count = 0
    for paper in library.entries:
        count += 1
        if 'url' in paper:
            found_count += 1
        else:
            print(f"\033[31mStill missing URL for {paper['ID']}, \"{paper['title']}\". Please add manually.\033[0m")
    if count == found_count:
        print(f"\033[32mAll URLs found for {count} papers. Good job!\033[0m")
    else:
        print(f"\033[31mFound {found_count} URLs out of {count} papers.\033[0m")
import requests
from bs4 import BeautifulSoup
from data import comprehensive_list
import csv
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

first_url = "https://www.aapc.com/codes/cpt-codes-range/"


def recurse_scraping(url: str) -> list:
    """
    Recursively do web scraping on each webpage that contains CPT code ranges, until reach
    the final page where no more code ranges are present.

    Return:
    List[str] that contains urls for the final pages containing CPT code ranges
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    list_code_ranges = soup.find_all("div", class_="list-code-range")
    comprehensive_list = []
    can_find = False  # Track if any <div class="col-md-4"> is found
    for index, list_code_range in enumerate(list_code_ranges, start=1):
        col_md_4_div = list_code_range.find("div", class_="col-md-4")
        if col_md_4_div:
            can_find = (
                True  # Set to True if at least one <div class="col-md-4"> is found
            )
            link_tag = col_md_4_div.find("a")
            if link_tag and link_tag.has_attr("href"):
                link = urljoin(url, link_tag["href"])  # Ensure the link is absolute
                # Recursively scrape the linked page
                comprehensive_list.extend(recurse_scraping(link))
            else:
                print("No href found in col-md-4 div")
        else:
            print(f"No col-md-4 div found in list-code-range {index}")

    # Find and handle pagination (next/other pages)
    pagination_div = soup.find("div", class_="col-md-12 pgbox")
    if pagination_div:
        next_page_link = pagination_div.find("a", text=">")  # Find the "Next" link
        if next_page_link and next_page_link.has_attr("href"):
            next_page_url = urljoin(url, next_page_link["href"])
            print(f"Found next page: {next_page_url}")
            comprehensive_list.extend(
                recurse_scraping(next_page_url)
            )  # Scrape the next page

    # If no <div class="col-md-4"> was found, append the current URL
    if not can_find:
        print(f"Stopping recursion at {url}, no more <div class='col-md-4'> found")
        comprehensive_list.append(url)

    return comprehensive_list


def get_CPT_code(url: str) -> str:
    """
    Helper function that takes url and return the corresponding CPT code
    """
    code = url.split("/")[-1]
    return code


def get_final_url(url: str) -> list:
    """
    Take the last pages that contains CPT code ranges, return a list
    containing the urls for individual CPT codes
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    list_code_ranges = soup.find_all("div", class_="list-code-range")
    final_list = []

    for index, list_code_range in enumerate(list_code_ranges, start=1):
        # Find the <a href...> within this list-code-range
        inner_link = list_code_range.find("a")
        if inner_link and inner_link.has_attr("href"):
            link = inner_link["href"]
            final_list.append(link)
        else:
            print("No href found in a")

    return final_list


def find_p(url: str):
    """
    Access the final pages containing CPT code description, get the description paragraph
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    # Find the <div> with class="tab-pane active"
    cpt_layterms_div = soup.find("div", class_="tab-pane active")
    # Check if the div exists, and then find only the first <p> tags inside it
    if cpt_layterms_div:
        paragraph = cpt_layterms_div.find("p")
        texts = paragraph.get_text(strip=True)
        return texts
    else:
        print("error")
        return None


def create_csv(filename="cpt_codes.csv"):
    """
    Use the comprehensive list to build cpt_codes.csv
    """
    # Check if file exists and is empty
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Code", "Description"])
        # Write the code and description (append)
        for final_page_url in comprehensive_list:
            final_page = get_final_url(url=final_page_url)
            for last_page_url in final_page:
                code_string = get_CPT_code(last_page_url)
                description = find_p(url=last_page_url)
                writer.writerow([code_string, description])
    print(f"Appended code and description to '{filename}'")


if __name__ == "__main__":
    create_csv()
    # # Write the comprehensive list to data.py
    # comprehensive_list = recurse_scraping(first_url)
    # with open("data.py", "w") as f:
    #     f.write(f"comprehensive_list = {comprehensive_list}")

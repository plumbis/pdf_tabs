#!/usr/bin/env python3

import re
import sys
import random
from bs4 import BeautifulSoup, Tag

def rewrite_links(soup):

    # The STP heading is a special cookie.
    # Hugo auto fixes the "-STP" links but this messes up our link rewrite
    # the easy fix is to just add an extra anchor
    stp = soup.find("a", id="Spanning-Tree-and-Rapid-Spanning-Tree-STP")
    if stp:
        stp.insert_after(soup.new_tag("a", id="Spanning-Tree-and-Rapid-Spanning-Tree"))

    # Generate anchors for all headers
    for h_size in [soup("h2"), soup("h3"), soup("h4"), soup("h5")]:
        for h in h_size:
            h.insert_after(soup.new_tag("a", id=h["id"]))

    # our URL is based on the PDF page we are.
    # look for our custom meta tag to determine which PDF this is.
    try:
        url = soup.find(attrs={"data-link": True})["data-link"]
    except:
        print("Unable to find \"data-link\" meta header. Check PDF source HTML file. Exiting.")
        exit(1)

    for a in soup.find_all(href=re.compile(url)):
        link_parts = a["href"].split("/")

        # if the last element is an anchor (#) with no text
        if link_parts[len(link_parts) - 1] == "#":

            # then the link is the part before that
            a["href"] = "#" + link_parts[len(link_parts) - 2]

        # it's anchor text
        else:
            a["href"] = link_parts[len(link_parts) - 1]

    return soup

def fix_tabs(soup):
    for book in soup.find_all("div", attrs={"class": "book-tabs"}):
        if book.find("div", attrs={"class": "book-tabs"}):
            print(book["data-book"])
            book.replace_with(fix_tabs(book))

        else:
            book_soup = BeautifulSoup("", "html.parser")
            for radio in book.find_all("input", attrs={"data-book": book["data-book"]}):
                div = book_soup.new_tag("div")
                div["class"] = "book-tabs"

                radio["name"] = random.randint(1,sys.maxsize)
                radio["checked"] = "checked"
                div.append(radio)

                label = book.find("label", attrs={"data-tab": radio["data-tab"]})
                label["for"] = radio["name"]
                div.append(label)

                inner = book.find("div", attrs={"data-tab": radio["data-tab"]})
                div.append(inner)
                book_soup.append(div)
            return book_soup

def main():

    #with open("public/cumulus-linux-42/pdf/index.html") as html_file:
    with open("clag.html") as html_file:
        soup = BeautifulSoup(html_file, "html.parser")

    soup = rewrite_links(soup)

    for tab_content in soup.find_all("div", attrs={"class": "book-tabs-content markdown-inner"}):
        if tab.find("div", attrs={"class": "book-tabs-content markdown-inner"}):

    # book_soup = BeautifulSoup("", "html.parser")

    #     for radio in book.find_all("input", attrs={"data-book": book["data-book"]}):
    #         div = soup.new_tag("div")
    #         div["class"] = "book-tabs"

    #         radio["name"] = random.randint(1,sys.maxsize)
    #         radio["checked"] = "checked"
    #         div.append(radio)

    #         label = book.find("label", attrs={"data-tab": radio["data-tab"]})
    #         label["for"] = radio["name"]
    #         div.append(label)

    #         inner = book.find("div", attrs={"data-tab": radio["data-tab"]})
    #         div.append(inner)
    #         book_soup.append(div)
    #     book.replace_with(book_soup)


    print(soup.prettify())

    # with open("test.html", "w") as file:
    #     file.write(str(soup))

if __name__ == "__main__":
    main()

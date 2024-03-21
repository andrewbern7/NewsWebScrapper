import requests
from bs4 import BeautifulSoup


def nbc_frontpage_extractor():
    URL = "https://www.nbcnews.com/us-news/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    # Find all <h2> tags with class "headline___1H5XD"
    headlines = soup.find_all("h2", class_="tease-card__headline tease-card__title tease-card__title--news relative")
    headlines += soup.find_all("h2", class_="styles_headline__ice3t")
    # Create a dictionary to store headline text and its corresponding link
    headline_links = {}
    article_count = 0
    # Extract headline text and link from each headline
    for headline in headlines:
        headline_text = headline.text.strip()
        link = headline.find('a')['href']
        headline_links[headline_text] = link
        article_count += 1

    # Print headline text and link
    #for headline, link in headline_links.items():
        # add back to test print("Headline:", headline)
        # add back to test print("Link:", link)

    print("Articles in the list: " + str(article_count))
    return headline_links


def articlepage_extractor(links_dict):
    for link in links_dict.values():
        page = requests.get(link)
        soup = BeautifulSoup(page.content, "html.parser")

        meta_tag = soup.find("meta", {"property": "og:title", })
        if meta_tag:
            content = meta_tag.get("content")
            print("Title:", content)
        else:
            print("Title not found...")

        # pulls meta description
        meta_description = soup.find("meta", {"name": "description"})
        if meta_description:
            content = meta_description.get("content")
            print("Meta Description:", content)
        else:
            print("Meta description not found...")

        article_content = soup.find("div", class_="article-body__content")
        if article_content:
            # Extract text content from all <p> tags within the article-body__content div
            article_text = "\n".join([p.get_text(strip=True) for p in article_content.find_all("p")])
            print(article_text)
        else:
            return None

        # You can extract more information from the article page here
        print("Link:", link)
        print()



def main():
    links_list = nbc_frontpage_extractor()
    articlepage_extractor(links_list)


if __name__ == "__main__":
    main()

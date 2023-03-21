
#!/usr/bin/env python3

"""
This Python program scrapes news articles from a given URL, up to a specified depth,
searching for a specified string within the content of each page. If the search string
is found, the article text is written to the output file with appropriate line breaks.
The program also prints the headline of each found article to the terminal. If the
elapsed time since the program started is greater than the specified run time, the
program exits and prints "scrape has timed out."

Usage:
    python scraper.py URL DEPTH SEARCH_STRING OUTPUT_FILE RUN_TIME

Arguments:
    URL (str): The starting URL to begin the web scraping process.
    DEPTH (int): The maximum depth of the web scraping process. The scraper follows
                 links from the starting URL up to the specified depth.
    SEARCH_STRING (str): The string to be searched for within the text content of each page.
    OUTPUT_FILE (str): The output file name where the article text will be saved as plain text.
    RUN_TIME (float): The maximum time in seconds the program is allowed to run.

Example:
    python scraper.py "https://www.example.com" 2 "search term" "output.txt" 300

Notes:
    - This program requires the 'requests' and 'beautifulsoup4' libraries to be installed.
    - The output file will include the search term, URL, and search depth at the beginning.
    - The terminal will display the headline of each found article as they are processed.
"""
import sys
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_articles(url, depth, search_string, output_file, run_time):
    """
    This function scrapes news articles from a given URL, up to a specified depth,
    searching for a given string within the content of each page. If the search string
    is found, the article text is written to the output file with appropriate line breaks.
    The function also prints the headline of each found article to the terminal. If the
    elapsed time since the program started is greater than the specified run time, the
    function exits and prints "scrape has timed out."

    Args:
        url (str): The starting URL to begin the web scraping process.
        depth (int): The maximum depth of the web scraping process. The scraper follows
                    links from the starting URL up to the specified depth.
        search_string (str): The string to be searched for within the text content of each page.
        output_file (str): The output file name where the article text will be saved as plain text.
        run_time (float): The maximum time in seconds the program is allowed to run.

    Example:
        scrape_articles("https://www.example.com", 2, "search term", "output.txt", 300)

    Notes:
        - This function requires the 'requests' and 'beautifulsoup4' libraries to be installed.
        - The output file will include the search term, URL, and search depth at the beginning.
        - The terminal will display the headline of each found article as they are processed.
    """


    def write_with_line_breaks(text, max_line_length, file):
        """
        This function writes the given text to the provided file, inserting a newline
        character at the nearest whitespace before the specified maximum line length.
        If there's no whitespace within the max_line_length limit, it inserts a newline
        at the max_line_length position.

        Args:
            text (str): The input text to be written to the file with line breaks.
            max_line_length (int): The maximum number of characters allowed in a line before
                                inserting a newline character.
            file (TextIO): The file object opened in write mode to which the text will be
                        written with the added line breaks.

        Example:
            with open("output.txt", "w", encoding="utf-8") as out_file:
                write_with_line_breaks("This is a sample text.", 10, out_file)
        """
        start = 0
        while start < len(text):
            end = start + max_line_length
            if end < len(text):
                while end > start and text[end] != ' ':
                    end -= 1
                if end == start:
                    end = start + max_line_length
            else:
                end = len(text)
            file.write(text[start:end] + "\n")
            start = end + 1

    start_time = time.time()
    visited_urls = set()
    urls_to_visit = [(url, 0)]

    try:
        with open(output_file, "w", encoding="utf-8") as out_file:
            out_file.write(f"Search Term: {search_string}\n")
            out_file.write(f"URL: {url}\n")
            out_file.write(f"Search Depth: {depth}\n")

            while urls_to_visit:
                current_url, current_depth = urls_to_visit.pop(0)

                if current_url in visited_urls or current_depth > depth:
                    continue

                visited_urls.add(current_url)

                try:
                    response = requests.get(current_url)
                    soup = BeautifulSoup(response.text, "html.parser")

                    for link in soup.find_all("a"):
                        href = link.get("href")
                        if href:
                            urls_to_visit.append((urljoin(url, href), current_depth + 1))

                    if search_string.lower() in soup.text.lower():
                        title = soup.title.string if soup.title else "No title found"
                        print(f"Found article: {title}")
                        article_text = soup.get_text()
                        write_with_line_breaks(article_text, 80, out_file)

                    elapsed_time = time.time() - start_time
                    if elapsed_time > run_time:
                        print("Scrape has timed out")
                        break

                except Exception as e:
                    print(f"Error processing URL {current_url}: {e}")

    except IOError as e:
        print(f"Error opening or writing to output file {output_file}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")



if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python scraper.py URL DEPTH SEARCH_STRING OUTPUT_FILE RUN_TIME")
        sys.exit(1)

    url_arg = sys.argv[1]
    depth_arg = int(sys.argv[2])
    search_string_arg = sys.argv[3]
    output_file_arg = sys.argv[4]
    run_time_arg = float(sys.argv[5])

    try:
        scrape_articles(url_arg, depth_arg, search_string_arg, output_file_arg, run_time_arg)
    except Exception as e:
        print(f"An error occurred while running the scraper: {e}")
        sys.exit(1)                
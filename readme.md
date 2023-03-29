# News Article Scraper

This Python program scrapes news articles from a given URL, up to a specified depth, searching for a specified string within the content of each page. If the search string is found, the article text is written to the output file with appropriate line breaks. The program also prints the headline of each found article to the terminal. If the elapsed time since the program started is greater than the specified run time, the program exits and prints "scrape has timed out."

## Requirements

- Python 3
- `requests` library
- `beautifulsoup4` library

To install the required libraries, run:

\```bash
pip install requests beautifulsoup4
\```

## Usage

Run the script using the following command:

\```bash
python scraper.py URL DEPTH SEARCH_STRING OUTPUT_FILE RUN_TIME
\```

### Arguments

- `URL`: The starting URL to begin the web scraping process.
- `DEPTH`: The maximum depth of the web scraping process. The scraper follows links from the starting URL up to the specified depth.
- `SEARCH_STRING`: The string to be searched for within the text content of each page.
- `OUTPUT_FILE`: The output file name where the article text will be saved as plain text.
- `RUN_TIME`: The maximum time in seconds the program is allowed to run.

### Example

\```bash
python webscrape.py "https://www.example.com" 2 "search term" "output.txt" 300
\```

## Notes

- The output file will include the search term, URL, and search depth at the beginning.
- The terminal will display the headline of each found article as they are processed.
- The script has basic error handling for file access exceptions and other unexpected exceptions.
- This script is compatible with Python 3.6 and later.

## License

This project is licensed under the MIT License.

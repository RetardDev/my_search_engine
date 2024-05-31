My Search Engine Project

This project is a search engine built using Django, NLTK, and Scrapy. It was created as a school project and demonstrates the integration of web scraping, natural language processing, and a web framework to build a functional search engine.
Getting Started

Follow these instructions to set up and run the project on your local machine.
Prerequisites

    Python installed on your machine.

Installation

    Clone the Repository

    Open your terminal and run:

```
git clone https://github.com/RetardDev/my_search_engine.git
cd my_search_engine
```

Create a Virtual Environment

Create and activate a virtual environment:

```
py -m venv virt_env
virt_env\Scripts\activate
```

Install Dependencies

Install the required Python packages:

```

pip install -r requirements.txt
```

Run the Django Development Server

Start the Django server:

```
    py manage.py runserver
```

Project Details

This project contains three main spiders in the spiders folder:

    keyword_spider
        Extracts keywords from webpages stored in the database.
        Uses Scrapy for web scraping and NLTK for filtering important words.

    site_spider
        Adds sites from a predefined list.
        The list is provided in a text file containing 1000 website URLs.

    webpage_spider
        Scrapes a site for links (a href) and saves them to the database.
        Also collects the title of each webpage.

Additional Information

    The credentials for the Django admin portal are provided in the admin.txt file.
    Ensure you follow all the setup instructions carefully for a smooth setup process.

Enjoy!

Feel free to explore and enhance the project. Contributions are welcome!

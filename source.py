import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# URLs of Economic Times and Moneycontrol news pages
et_url = "https://economictimes.indiatimes.com/markets/stocks/news"
mc_url = "https://www.moneycontrol.com/news/"

# Function to scrape market news from Economic Times
def scrape_market_news_et(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve page from Economic Times. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    news_section = soup.find_all('div', class_='eachStory')

    news_data = []
    
    for news in news_section:
        headline = news.find('h3').text.strip()
        link = news.find('a')['href']
        full_link = f"https://economictimes.indiatimes.com{link}"
        description = news.find('p').text.strip()

        date_tag = news.find('time')
        if date_tag and date_tag.has_attr('data-time'):
            pub_time = date_tag['data-time']
        else:
            pub_time = "Time not available"

        source = "Economic Times"

        news_data.append({
            'Headline': headline,
            'Link': full_link,
            'Description': description,
            'Published Time': pub_time,
            'Source': source
        })
    
    return news_data

# Function to scrape market news from Moneycontrol
def scrape_market_news_mc(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve page from Moneycontrol. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    news_section = soup.find_all('li', class_='clearfix')

    news_data = []

    for news in news_section:
        headline_tag = news.find('h2')
        if headline_tag:
            headline = headline_tag.text.strip()
        else:
            continue

        link_tag = news.find('a')
        if link_tag and link_tag.has_attr('href'):
            full_link = link_tag['href']
        else:
            full_link = "Link not available"
        
        description_tag = news.find('p')
        description = description_tag.text.strip() if description_tag else "No description available"

        date_tag = news.find('span', class_='time')
        pub_time = date_tag.text.strip() if date_tag else "Time not available"

        source = "Moneycontrol"

        news_data.append({
            'Headline': headline,
            'Link': full_link,
            'Description': description,
            'Published Time': pub_time,
            'Source': source
        })
    
    return news_data

# Function to scrape news from both sources and combine them
def scrape_news_from_both_sources(et_url, mc_url):
    et_news = scrape_market_news_et(et_url)
    mc_news = scrape_market_news_mc(mc_url)

    if et_news is None and mc_news is None:
        print("Failed to retrieve news from both sources.")
        return None

    # Combine the news from both sources
    combined_news = []
    if et_news:
        combined_news.extend(et_news)
    if mc_news:
        combined_news.extend(mc_news)

    # Convert the combined news into a DataFrame
    news_df = pd.DataFrame(combined_news)

    # Save the DataFrame to a CSV file
    news_df.to_csv(f'combined_market_news_{datetime.now().strftime("%Y-%m-%d")}.csv', index=False)

    print(f"Scraped {len(combined_news)} news articles from both sources.")
    
    return news_df

# Call the function to scrape and save the news data
news_df = scrape_news_from_both_sources(et_url, mc_url)

# Display the scraped data
if news_df is not None:
    print(news_df.head())

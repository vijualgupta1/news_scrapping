import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# URL of the Economics Times market news page
url = "https://economictimes.indiatimes.com/markets/stocks/news"

# Function to scrape data
def scrape_market_news(url):
    # Fetch the page content
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve page. Status code: {response.status_code}")
        return None
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the section where news articles are listed
    news_section = soup.find_all('div', class_='eachStory')
    
    # List to hold the scraped data
    news_data = []
    
    # Extracting information for each news article
    for news in news_section:
        # Extract headline
        headline = news.find('h3').text.strip()
        
        # Extract link to the full article
        link = news.find('a')['href']
        full_link = f"https://economictimes.indiatimes.com{link}"
        
        # Extract description or summary
        description = news.find('p').text.strip()
        
        # Extract publication date and time, if available
        date_tag = news.find('time')
        if date_tag and date_tag.has_attr('data-time'):
            pub_time = date_tag['data-time']  # Get the exact time from the 'data-time' attribute
        else:
            pub_time = "Time not available"
        
        # Set the source (static value for this site)
        source = "Economic Times"  # Static source value

        # Append the data as a dictionary to the list
        news_data.append({
            'Headline': headline,
            'Link': full_link,
            'Description': description,
            'Published Time': pub_time,  # Store the exact publication time
            'Source': source  # Add the source column
        })
    
    # Create a DataFrame for better presentation (optional)
    news_df = pd.DataFrame(news_data)
    
    # Save the DataFrame to a CSV file
    news_df.to_csv(f'market_news_{datetime.now().strftime("%Y-%m-%d")}.csv', index=False)
    
    print(f"Scraped {len(news_data)} news articles.")
    
    return news_df

# Call the function to scrape and save the data
news_df = scrape_market_news(url)

# Display the scraped data
if news_df is not None:
    print(news_df.head())

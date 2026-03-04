import feedparser
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')


def search_query(query, num_articles_per_query):

    rss_url = f"https://news.google.com/rss/search?q={query}"
    feed = feedparser.parse(rss_url)

    articles = []
    articles.extend(feed.entries[:num_articles_per_query]) # append the first 10 articles
    # to make it run faster, i could append a dictionary of the characteristics of each article, for all n, then extract that info later, but i think its ok rn

    return articles
    
# fix! RSS url is not normal URL, so no search? 
# but idk why u still cant get 'p' from a rss url tho ?!
def search_article_content(url):

    try:
        page = requests.get(url, timeout=10)
        page.raise_for_status()

        soup = BeautifulSoup(page.text, 'html.parser')

        paragraphs = soup.find_all('p')
        content = ' '.join([p.get_text() for p in paragraphs])
        return content.strip()
        
    except requests.exceptions.RequestException:
        print("An error has occured. Please try again, or contact the developer.")


def analyse_sentiment(text):

    analyser = SentimentIntensityAnalyzer()

    scores = analyser.polarity_scores(text)
    polarity = scores['compound']

    if polarity >= 0.5:
        sentiment = "Positive"
    elif polarity <= -0.5:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return sentiment, polarity



def main():
    
    stock = input("Enter your stock (e.g. AAPL): ")

    queries = [
        f"{stock}+stock",
        f"{stock}+price",
        f"{stock}+news",
        f"{stock}+market",
        f"{stock}+trade",
        f"{stock}+trends",
        f"{stock}+forecast",
        f"{stock}+analysis",
        f"{stock}+shares",
        f"{stock}+history"
    ]
    num_articles_per_query = 10
    total_articles = []
    
    # for each query, search for n articles
    for number, query in enumerate(queries):
        print(f"Searching for {stock}... ({number*num_articles_per_query}/{len(queries)*num_articles_per_query})\n")
        articles = search_query(query, num_articles_per_query)
        total_articles.extend(articles)

    # calculative cumulative overall sentiment and polarity
    total_sentiments = {
        "Positive": 0,
        "Negative": 0,
        "Neutral": 0
    }

    # print out each article and their info, including calculated polarity and sentiment
    # analyse overall sentiment and polarity
    for number, article in enumerate(total_articles, 1):
        sentiment, polarity = analyse_sentiment(article.title)

        print(f"Article {number}: {article.title}")
        print(f"Date: {article.published}")
        print(f"Link: {article.link}")
        print(f"Sentiment: {sentiment}, Polarity: {polarity:.2f}\n")

        total_sentiments[sentiment] += 1


    # overall sentiment and percentage
    total_num_articles = len(total_articles)
    overall_sentiment = max(total_sentiments, key=total_sentiments.get)
    overall_percentage = (total_sentiments.get(overall_sentiment)) / total_num_articles * 100
    
    # print overall summary
    print("\n---Summary Market Analysis---")
    print(f"Total articles analysed = {len(total_articles)}")
    for sentiment, number in total_sentiments.items():
        percentage = number / total_num_articles * 100
        print(f"{sentiment}: {number} ({percentage:.2f}%)")
    print(f"Overall sentiment: {overall_sentiment} ({overall_percentage:.2f}%)")



if __name__ == "__main__":
    main()
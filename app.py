import feedparser
import requests
from bs4 import BeautifulSoup

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

import streamlit as st


def search_query(query, num_articles_per_query):

    rss_url = f"https://news.google.com/rss/search?q={query}"
    feed = feedparser.parse(rss_url)

    articles = []
    articles.extend(feed.entries[:num_articles_per_query]) # append the first 10 articles
    # to make it run faster, i could append a dictionary of the characteristics of each article, for all n, then extract that info later, but i think its ok rn

    return articles


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


def run_analysis(stock, progress):
    
    queries = [
        f"{stock}+stock",
        f"{stock}+shares",
        f"{stock}+price",
        f"{stock}+news",
        f"{stock}+market",
        f"{stock}+trade",
        f"{stock}+trends",
        f"{stock}+forecast",
        f"{stock}+analysis",
        f"{stock}+history"
    ]
    num_articles_per_query = 10
    total_articles = []
    
    # for each query, search for n articles
    for number, query in enumerate(queries):
        progress.write(f"Sit tight! Searching for {stock}... ({number*num_articles_per_query}/{len(queries)*num_articles_per_query})\n")
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
    article_results = []
    for number, article in enumerate(total_articles, 1):
        sentiment, polarity = analyse_sentiment(article.title)

        article_results.append({
            "title": article.title,
            "date": article.get("published"),
            "link": article.link,
            "sentiment": sentiment,
            "polarity": polarity
        })

        total_sentiments[sentiment] += 1

    # overall sentiment and percentage
    total_num_articles = len(total_articles)
    overall_sentiment = max(total_sentiments, key=total_sentiments.get)
    overall_percentage = (total_sentiments.get(overall_sentiment)) / total_num_articles * 100
    
    return {
        'stock': stock, "total": total_num_articles,
        "sentiments": total_sentiments,
        "overall_sentiment": overall_sentiment,
        "overall_percentage": overall_percentage,
        "articles": article_results
    }



def main():
    st.title("Stock Sentiment Analyser")

    # session states
    if "running" not in st.session_state:
        st.session_state.running = False
    if "results" not in st.session_state:
        st.session_state.results = None

    stock_input = st.text_input("Enter a stock ticker:", disabled=st.session_state.running)
    analyse_button = st.button("Analyse", disabled=st.session_state.running)

    # run analysis
    if analyse_button and stock_input:
        st.session_state.running = True
        st.session_state.results = None

        progress = st.empty()
        results = run_analysis(stock_input, progress)

        st.session_state.results = results
        st.session_state.running = False

        st.rerun()
    
    # get results, diplay analysis summary
    if st.session_state.results:
        results = st.session_state.results
        
        st.write('____________')
        st.subheader("Market Summary")
        st.write(f"Stock: {results['stock']}")
        st.write(f"Total articles analysed: {results['total']}")
        st.write(f"Overall sentiment: {results['overall_sentiment']} ({results['overall_percentage']:.2f}%)")
        for sentiment, count in results['sentiments'].items():
            st.write(f"{sentiment}: {count} ({count / results['total'] * 100:.2f}%)")

        st.write('____________')

        # rerun button 
        if st.button("Analyse Another Stock"):
            st.session_state.results = None
            st.rerun()

        st.write('____________')
    
        # each article
        st.subheader("Articles")
        for number, article in enumerate(results['articles'], 1):
            article_c = st.container()
            article_c.write(f"Article {number}: {article['title']}")
            article_c.write(f"Date: {article['date']}")
            article_c.write(f"Sentiment: {article['sentiment']}, Polarity: {article['polarity']:.2f}")
            article_c.write(f"Link: {article['link']}")
            st.write('____________')



if __name__ == "__main__":
    main()



# todo
# make website look nice - centre format, colour scheme, buttons, bucket articles into nice blocks
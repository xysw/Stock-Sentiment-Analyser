# Stock-Sentiment-Analyser

A Python-based tool that quantifies the sentiment of financial news articles, to inform trading.

Scrapes recent news articles from Google RSS feeds, extracts relevant metadata, and sequentially passes data to the pretrained VADER model, a NLP model by NLTK. Determines the overall sentiment of a user-inputted stock from cumulative polarity scores of individual articles. This project was developed to learn how to apply NLP models to real applications and also learn how to extract data from the web using Feedparser and BeautifulSoup.

Deployed using Streamlit at: https://stock-sentiment-analyser.streamlit.app/ 

## Technologies
* Python 3.12.10
* Feedparser 6.0.12
* Requests 2.32.2
* nltk 3.8.1
* Streamlit 1.36.0

## Launch
### Streamlit page: https://stock-sentiment-analyser.streamlit.app/

### Run locally:
1. Clone the project
```
git clone https://github.com/xysw/stock-sentiment-analyser.git
cd stock-sentiment-analyser
```
3. Install dependencies
```
pip install -r requirements.txt
```
4. Run the application
```
streamlit run app.py
```
5. (Other: To run the terminal version of the app instead of the web version, run the sentiment_analyser.py file instead)

### Usage
1. Enter a stock ticker into the input field (e.g. AAPL)
2. Click "analyse"
3. Wait for the search to complete
4. Review the Market Summary and list of articles analysed
5. Click "Analyse another stock" to run a new query

## Limitations
* Sentiment analysis is performed at a headline level, access to full text is restricted by some news sources
* VADER is a rule-based sentiment analysis tool optimized for social media text, but may not perform as well on financial news

Hence, future exploration will be to extract full article text and pass it to various different NLP models, and compute aggregate sentiment. Alternatively, text could be extracted from different sources, such as social media, to better suit VADER's usage.

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os
from autoscraper import AutoScraper
import pandas as pd
import streamlit as st

header = st.container()
model_training = st.container()
feature = st.container()
with header:
    st.title('Amazon Product Reviews Analysis')
    st.text('Drop the URL of any product reviews page to check the analysis')

with model_training:
    st.header('Drop the link')

    sel_col, disp_col = st.columns(2)
    n_estimators = sel_col.text_input('Please drop the link of product reviews to see the analysis','https://www.amazon.com/Maybelline-SuperStay-Matte-Liquid-Lipstick/product-reviews/B074VD4X86/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews')


def scrape(x):
    amazon_url = "https://www.amazon.com/Maybelline-SuperStay-Matte-Liquid-Lipstick/product-reviews/B074VD4X86/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"

    wish_list = ['Love it!', '362 people found this helpful']

    scraper_1 = AutoScraper()
    result = scraper_1.build(amazon_url, wish_list)
    review_title_key = scraper_1.get_result_similar(amazon_url, grouped=True)
    keys = list(review_title_key.keys())
    title_key = keys[0]
    scraper_1.set_rule_aliases({title_key: 'Review_Title'})
    scraper_1.keep_rules([title_key])
    scraper_1.save('Amazon-Reviews')
    scraper_1.load('Amazon-Reviews')
    link = x
    result_1 = []
    for i in range(1, 20):
        result = scraper_1.get_result_similar(
            link+'&pageNumber='+str(i), group_by_alias=True)
        result_1.append(result['Review_Title'])
    reviews = []
    for i in range(len(result_1)):
        for j in range(len(result_1[i])):
            reviews.append(result_1[i][j])
    review_dict = {'prodct_review': reviews}
    df = pd.DataFrame(review_dict)
    df.to_csv('product_reviews.csv')
    return df


scrape(n_estimators)

nltk.download('vader_lexicon')


def parse_values(x):
    if x < 0:
        return 'negative'
    elif x == 0:
        return 'neutral'
    else:
        return 'positive'


sid = SentimentIntensityAnalyzer()
df1 = pd.read_csv('product_reviews.csv')
df1['prodct_review'].isnull().sum()
df1['scores'] = df1['prodct_review'].apply(
    lambda review: sid.polarity_scores(review))
df1['compound'] = df1['scores'].apply(lambda score_dict: score_dict['compound'])
df1['comp_score'] = df1['compound'].apply(parse_values)
df1.to_csv('sentiments_1.csv')

with feature:
    st.subheader('Bar Charts for Sentiment Analysis')
    pos_neg = df1['comp_score'].value_counts()
    st.bar_chart(pos_neg)
    st.subheader('Line Charts for Sentiment Analysis')
    pos_neg = df1['comp_score'].value_counts()
    st.line_chart(pos_neg)
    st.subheader('Line Charts for Sentiment Analysis')
    comp = df1['compound'].value_counts()
    # posit = [d.get('pos') for d in df1.scores]
    st.line_chart(comp)

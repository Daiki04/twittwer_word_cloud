import streamlit as st
from wordcloud import WordCloud
import MeCab
import Tweetl
from PIL import Image

CONSUMER_KEY = "GSqwcvv42kqYBxVEPTyONTd3c"
CONSUMER_SECLET = "lgQcF06jaLZs2YiUpDBHXSodE2leros03t5qSJzLoqNdRuC4DL"
ACCESS_TOKEN = "1318351090161754114-826FlEHp0q2KPvkgGvIehvtMx2kwlC"
ACCESS_TOKEN_SECRET = "3ticj5K5nVnzEcX0F5K0SusQp3S6lyz2AaxcNRexMGVbC"

def get_tweets_cranging(Account, num=100):
    tweet_getter = Tweetl.GetTweet(
        CONSUMER_KEY,
        CONSUMER_SECLET,
        ACCESS_TOKEN,
        ACCESS_TOKEN_SECRET
    )
    df_target = tweet_getter.get_tweets_target(Account, num)
    tweet_cleanser = Tweetl.CleansingTweets()
    cols = ["text"]
    df_clean = tweet_cleanser.cleansing_df(df_target, subset_cols=cols)
    return df_clean

def get_noun_words(Account, num=100):
    df = get_tweets_cranging(Account, num)
    contents = []
    for i in range(len(df)):
        content = df["text"][i].replace("|", "").replace("/", "").replace(" ", "")
        contents.append(content)
    tweet_texts = "".join(contents)
    mecab = MeCab.Tagger()
    parts = mecab.parse(tweet_texts)
    nouns = []
    for part in parts.split("\n")[:-2]:
        if "名詞" in part.split("\t")[4]:
            nouns.append(part.split("\t")[0])
    words = " ".join(nouns)
    return words


def main():
    st.title("Twitter Word Cloud App")
    Account = st.sidebar.text_input("アカウントID(@を除いたアカウントIDを入力)", " ")
    if Account != " ":
        words = get_noun_words(Account)
        font_path = "./GenShinGothic-Monospace-Bold.ttf"
        wc = WordCloud(width=1280, height=720, background_color="white", font_path=font_path)
        wc.generate(words)
        wc.to_file("show_img.jpg")
        image = Image.open('show_img.jpg')
        st.image(image, caption=f'Word Cloud')
    else:
        st.warning("サイドバーにアカウントIDを入力してください．")

if __name__ == "__main__":
    main()
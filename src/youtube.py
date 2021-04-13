from apiclient.discovery import build
from token_key import YOUTUBE_API_KEY


youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY,cache_discovery=False)
def youtubesearch(title):
    search_response = youtube.search().list(
    part='id',
#検索したい文字列を指定
    q=title + " vlog",
#視聴回数が多い順に取得
    order='viewCount',
    type='video',
    ).execute()
    # print(search_response)
    return f"https://www.youtube.com/watch?v={search_response['items'][0]['id']['videoId']}"
if __name__ == "__main__":
   print(youtubesearch("sagrada familia"))

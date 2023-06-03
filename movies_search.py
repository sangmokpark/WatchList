import csv
import chardet
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# 영화 데이터를 리스트로 초기화
movies = []

# 파일 인코딩 검출
with open("movies.csv", 'rb') as f:
    result = chardet.detect(f.read())
    
# CSV 파일에서 영화 데이터 로드
with open("movies.csv", "r", encoding=result['encoding']) as f:
    reader = csv.DictReader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        # 로드한 데이터를 딕셔너리 형태로 변환 후 리스트에 추가
        movie = {
            "title": row["title"],
            "cast": row["cast"].split(", "),
            "storyline": row["storyline"],
            "genre": row["genre"].split(", ")
        }
        movies.append(movie)

# NLTK에서 제공하는 영어 불용어(stopwords)를 다운로드
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")
stop_words = set(stopwords.words('english'))

# WordNetLemmatizer를 초기화
lemmatizer = WordNetLemmatizer()

# 입력받은 데이터와 유사한 영화 추천
def recommend_movies(cast, storyline, genre):
    recommended_movies = []
    for movie in movies:
        # cast, storyline, genre 모두 일치하는 경우
        if set(cast) == set(movie["cast"]) and storyline in movie["storyline"] and set(genre) == set(movie["genre"]):
            recommended_movies.append(movie["title"])
        else:
            # 일부 정보가 일치하는 경우
            tokens = word_tokenize(movie["storyline"].lower())
            # 불용어 제거
            filtered_tokens = [token for token in tokens if token not in stop_words]
            # Lemmatize
            lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
            # 입력받은 데이터에 있는 단어가 영화 설명에 포함되면 점수를 높임
            similarity_score = sum([1 for word in cast + genre + word_tokenize(storyline.lower()) if word in lemmatized_tokens])
            if similarity_score > 0:
                recommended_movies.append((movie["title"], similarity_score))

    # 점수에 따라 정렬 후 영화 제목만 반환
    recommended_movies = sorted(recommended_movies, key=lambda x: x[1], reverse=True)
    return [movie[0] for movie in recommended_movies]

# 사용자 입력 받기
cast = input("배우 이름을 입력하세요 (예: 톰 크루즈, 니콜 키드먼): ").split(",")
storyline = input("줄거리를 입력하세요: ")
genre = input("장르를 입력하세요 (예: 드라마, 미스터리, 로맨스): ").split(",")
#입력된 정보를 바탕으로 영화 추천
recommended_movies = recommend_movies(cast, storyline, genre)
#추천된 영화 출력
print(recommended_movies)
import requests, json

data = []
json_data = {}
open_file_path = "./moviedata.json"

# 1. top-ranked 영화
# 기존의 장르와 탑랭크 영화 데이터가 저장되어있던 json파일에서 영화정보에 카테고리 필드 추가
with open(open_file_path, "r") as json_file:
    json_data = json.load(json_file)
    # 영화정보에 카테고리 필드 추가
    for j_data in json_data:
        if j_data['model'] == 'movies.movie' :
            j_data['fields']['category'] = 'top-ranked'
        data.append(j_data)
print(len(data))



def getjson(max_page,url_category,category):

    # 한 페이지당 20개의 data로 총 5회 100개의 데이터를 가져옴
    for page_num in range(1,max_page):
        # 필요한 params
       # 카테고리별 영화를 가져옴.
        params = {'api_key' :'7e1a93bef30a77cdb9ffd78ee7ddc524', 'language' : 'ko', 'region':'KR', 'page' : page_num}
        # get요청으로 영화 데이터 가져오기

        res = requests.get('https://api.themoviedb.org/3/movie/'+url_category+'?', params = params)
        # 결과값 dicts 가져오기
        results = res.json()['results']
        # 하나씩 돌면서 데이터 추가 용이하게 변형시키기
        print
        for result in results:
            result['genres'] = result.pop('genre_ids')
            result.pop('video')
            result['category'] = category
            if result['backdrop_path'] == None:
                print(result['title'],result['backdrop_path'])
                result['backdrop_path'] = result['poster_path']
                print(result['backdrop_path'])
            temp = {"model":"movies.movie", "pk":result['id'], "fields":result}

            data.append(temp)
    print(len(data))


getjson(100,'top_rated','top-ranked')
getjson(20,'popular','popular')
getjson(20,'now_playing','nowplaying')
getjson(20,'upcoming','upcoming')


save_file_path = "./newmoviedata.json"
with open(save_file_path,'w') as outfile:
    json.dump(data,outfile, indent=4)


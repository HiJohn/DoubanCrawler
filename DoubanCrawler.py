import expanddouban
import bs4
# import codecs
import csv
import time


class Movie:
    """ 电影信息类 """

    def __init__(self, name, rate, location, category, info_link, cover_link):
        self.name = name
        self.rate = rate
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link

    def print_movie(self):
        result = "name:{},rate:{},location:{},category:{},info_link:{},cover_link：{}"
        print(result.format(self.name, self.rate, self.location, self.category, self.info_link, self.cover_link))

    def print_data(self):
        return "{},{},{},{},{},{}".format(self.name, self.rate, self.location, self.category, self.info_link,
                                          self.cover_link)


"""
return a string corresponding to the URL of douban movie lists given category and location.
"""
base = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,"
# list_locations = ["中国大陆","美国","香港","台湾","日本","韩国","英国","法国","德国","意大利","西班牙","印度","泰国","俄罗斯","伊朗"
#                   ,"加拿大","澳大利亚","爱尔兰","瑞典","巴西","丹麦"]
list_locations = ["中国大陆", "美国", "香港"]


# favorite_category = ["喜剧","爱情","动作"]


def get_movie_url(category, location):
    url = base + category + "," + location
    # print("url :"+url)
    return url


"""   类别 ，个数, """
category_dict = {}
"""  key : 地区， value :个数"""
category_area_dict = {}

"""
return a list of Movie objects with the given category and location.
"""
def get_movies(category, location):
    movie_list = []
    for loc in location:
        url = get_movie_url(category, loc)
        html = expanddouban.getHtml(url, True)
        soup = bs4.BeautifulSoup(html, "html.parser")

        content_div = soup.find(id="content").find(class_="list-wp").find_all("a", attrs={"class": "item"})

        """每个类别 每个地区 电影的数量 """
        category_area_dict[loc]=len(content_div)


        for element in content_div:
            # print(element)
            info_link = element.get("href")
            # print("info link :"+info_link)
            name = element.find("span", attrs={"class": "title"}).contents[0]
            rate = element.find("span", attrs={"class": "rate"}).contents[0]
            cover_link = element.find("img").get("src")
            m = Movie(name, rate, loc, category, info_link, cover_link)
            # print("movie:"+ m.print_data())
            movie_list.append(m)

        time.sleep(2)

    """ 按数量 排序 地区-数量 的字典 """
    sorted_dict_list = sorted(category_area_dict.items(), key=lambda x: x[1], reverse=True)
    """ 取前三 """
    sorted_dict_list = sorted_dict_list[0:3]
    """ 每个类别 电影个数 """
    total_len = len(movie_list)
    category_dict[category] = total_len

    # write_to_file(category,)

    return movie_list


def write_one_category(movies):
    with open("movies.csv", "w", encoding='utf-8-sig', newline='') as csv_file:
        movies_writer = csv.writer(csv_file, delimiter=',', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        for movie in movies:
            movies_writer.writerow([movie])


def get_movie_and_write_file():
    movie_list1 = get_movies("喜剧", list_locations)
    movie_list2 = get_movies("爱情", list_locations)
    movie_list3 = get_movies("动作", list_locations)

    write_one_category(movie_list1)
    write_one_category(movie_list2)
    write_one_category(movie_list3)

""" 在 category 中 排名前三的地区 """
def write_to_file(category,first_three,percents):
    with open('output.txt','a') as f:
        f.write("在电影分类 {} 中， 数量排名前三的地区以及所占比例是：{}，{}。"
                "{}，{}。"
                "{}，{}。 "
                .format(category,first_three[0],percents[0],first_three[1],percents[1],first_three[2],percents[2]))



# f = codecs.open("movies.csv","w","utf_8_sig")
# writer = csv.writer(f)
# writer.writerow(movie_list1)
# writer.writerow(movie_list2)
# writer.writerow(movie_list3)
# f.close()
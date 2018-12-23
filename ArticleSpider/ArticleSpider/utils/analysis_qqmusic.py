import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator


class BaseAnalysis(object):
    def __init__(self):
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        self.dfAll = pd.read_csv(filepath_or_buffer='../music_No_Title.csv', header=None, usecols=[2, 4], names=['playTimes', 'tags'], dtype={'playTimes': int, 'tags': str}) #, names=['1', '2', '3', '4', '5', '6']

    def show(self):
        pass


class AnalysisPlayTimes(BaseAnalysis):
    def __init__(self):
        super().__init__()
        # 小于10万
        times_less_10w = self.dfAll['playTimes'][self.dfAll.playTimes <= 100000].size
        # 10万到100万
        times_10w_to_100w = self.dfAll['playTimes'][(self.dfAll.playTimes > 100000) & (self.dfAll.playTimes <= 1000000)].size
        # 100万到500万
        times_100w_to_500w = self.dfAll['playTimes'][(self.dfAll.playTimes > 1000000) & (self.dfAll.playTimes <= 5000000)].size
        # 500万到1000万
        times_500w_to_1000w = self.dfAll['playTimes'][(self.dfAll.playTimes > 5000000) & (self.dfAll.playTimes <= 10000000)].size
        # 1000万到5000万
        times_1000w_to_5000w = self.dfAll['playTimes'][(self.dfAll.playTimes > 10000000) & (self.dfAll.playTimes <= 50000000)].size
        # 5000万到1亿
        times_5000w_to_1y = self.dfAll['playTimes'][(self.dfAll.playTimes > 50000000) & (self.dfAll.playTimes <= 100000000)].size
        # 大于1亿
        times_more_1y = self.dfAll['playTimes'][(self.dfAll.playTimes > 100000000)].size

        self.playTimes = np.array([times_less_10w, times_10w_to_100w, times_100w_to_500w, times_500w_to_1000w, times_1000w_to_5000w, times_5000w_to_1y, times_more_1y])
        self.index = ['<10w', '10w-100w', '100w-500w', '500w-1000w', '1000w-5000w', '5000w-1亿', '>1亿']

    def show(self):
        plt.xlabel('播放量')
        plt.ylabel('歌单数量')
        for index, size in zip(self.index, self.playTimes):
            plt.bar(index, size)
            plt.text(index, size + 10, str(size) + '个', ha='center')
        plt.show()


class AnalysisTags(BaseAnalysis):
    def __init__(self):
        super().__init__()
        self.tags = np.array(self.dfAll['tags'])

    def show(self):
        background_img = plt.imread('../images/qqmusic.jpg')
        img_color = ImageColorGenerator(background_img)
        music_cloud = WordCloud(
            background_color='white', mask=background_img, color_func=img_color, collocations=False,
            max_font_size=50
        )
        tags = self.deal_tags()
        music_img = music_cloud.generate(text=' '.join(tags))
        plt.imshow(music_img)
        axis = plt.gca()
        axis.set_axis_off()
        plt.show()

    def deal_tags(self):
        tags = []
        for each_tags in self.tags:
            if isinstance(each_tags, str):
                for tag in each_tags.split(','):
                    tags.append(tag)
        return tags


if __name__ == '__main__':
    a = AnalysisTags()
    a.show()

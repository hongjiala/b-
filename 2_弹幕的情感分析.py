import pandas as pd  # 数据分析库
from snownlp import SnowNLP  # 中文情感分析库
from wordcloud import WordCloud  # 绘制词云图
from pprint import pprint  # 美观打印
import jieba.analyse  # jieba分词
from PIL import Image  # 读取图片
import numpy as np  # 将图片的像素点转换成矩阵数据
import taichi as ti


# 情感分析打标
def sentiment_analyse(v_cmt_list):
	"""
	情感分析打分
	:param v_cmt_list: 需要处理的评论列表
	:return:
	"""
	score_list = []  # 情感评分值
	tag_list = []  # 打标分类结果
	pos_count = 0  # 计数器-积极
	neg_count = 0  # 计数器-消极
	for comment in v_cmt_list:
		tag = ''
		sentiments_score = SnowNLP(comment).sentiments
		if sentiments_score < 0.3:
			tag = '消极'
			neg_count += 1
		else:
			tag = '积极'
			pos_count += 1
		score_list.append(sentiments_score)  # 得分值
		tag_list.append(tag)  # 判定结果
	print('积极评价占比：', round(pos_count / (pos_count + neg_count), 4))
	print('消极评价占比：', round(neg_count / (pos_count + neg_count), 4))
	df['情感得分'] = score_list
	df['分析结果'] = tag_list
	# 把情感分析结果保存到excel文件
	df.to_excel('三国演义_情感评分结果.xlsx', index=None)
	print('情感分析结果已生成：三国演义_情感评分结果.xlsx')


def make_wordcloud(v_str, v_stopwords, v_outfile):
	"""
	绘制词云图
	:param v_str: 输入字符串
	:param v_stopwords: 停用词
	:param v_outfile: 输出文件
	:return: None
	"""
	print('开始生成词云图：{}'.format(v_outfile))
	try:
		stopwords = v_stopwords  # 停用词
		backgroud_Image = np.array(Image.open('谷爱凌背景图.png'))  # 读取背景图片
		wc = WordCloud(
			background_color="white",  # 背景颜色
			width=1500,  # 图宽
			height=1200,  # 图高
			max_words=1000,  # 最多字数
			font_path='/System/Library/Fonts/simkai.ttf',  # 字体文件路径，根据实际情况(Mac)替换
			# font_path="C:\Windows\Fonts\simhei.ttf",  # 字体文件路径，根据实际情况(Windows)替换
			stopwords=stopwords,  # 停用词
			mask=backgroud_Image,  # 背景图片
		)
		jieba_text = " ".join(jieba.lcut(v_str))  # jieba分词
		wc.generate_from_text(jieba_text)  # 生成词云图
		wc.to_file(v_outfile)  # 保存图片文件
		print('词云文件保存成功：{}'.format(v_outfile))
	except Exception as e:
		print('make_wordcloud except: {}'.format(str(e)))

if __name__ == '__main__':
	df = pd.read_csv('三国演义弹幕.csv')  # 读取excel
	v_cmt_list = df['弹幕内容'].values.tolist()  # 评论内容列表
	print('length of v_cmt_list is:{}'.format(len(v_cmt_list)))
	v_cmt_list = [str(i) for i in v_cmt_list]  # 数据清洗-list所有元素转换成字符串
	v_cmt_str = ' '.join(str(i) for i in v_cmt_list)  # 评论内容转换为字符串
	# 1、情感分析打分
	sentiment_analyse(v_cmt_list=v_cmt_list)
	# 2、用jieba统计弹幕中的top10高频词
	keywords_top50 = jieba.analyse.extract_tags(v_cmt_str, withWeight=True, topK=50)
	print('top50关键词及权重：')
	pprint(keywords_top50)

	# 3、画词云图
	make_wordcloud(v_str=v_cmt_str,
	               v_stopwords=['的', '啊', '她', '是', '了', '你', '我', '都', '也', '不', '在', '吧', '说', '就是', '这', '有'],  # 停用词
	               v_outfile='谷爱凌弹幕_词云图.jpg'  # 词云图文件名
	               )

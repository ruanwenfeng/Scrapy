import jieba.analyse
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import  re
# # 加载自定义分词字典
# # jieba.load_userdict("news.txt")
#
# # 语料
# corpos = '一个容易想到的思路，就是找到出现次数最多的词。如果某个词很重要，它应该在这篇文章中多次出现。于是，我们进行"词频"（Term Frequency，缩写为TF）统计。\
# 结果你肯定猜到了，出现次数最多的词是----"的"、"是"、"在"----这一类最常用的词。它们叫做"停用词"（stop words），表示对找到结果毫无帮助、必须过滤掉的词。\
# 假设我们把它们都过滤掉了，只考虑剩下的有实际意义的词。这样又会遇到了另一个问题，我们可能发现"中国"、"蜜蜂"、"养殖"这三个词的出现次数一样多。这是不是意味着，作为关键词，它们的重要性是一样的？\
# 显然不是这样。因为"中国"是很常见的词，相对而言，"蜜蜂"和"养殖"不那么常见。如果这三个词在一篇文章的出现次数一样多，有理由认为，"蜜蜂"和"养殖"的重要程度要大于"中国"，也就是说，在关键词排序上面，"蜜蜂"和"养殖"应该排在"中国"的前面。\
# 所以，我们需要一个重要性调整系数，衡量一个词是不是常见词。如果某个词比较少见，但是它在这篇文章中多次出现，那么它很可能就反映了这篇文章的特性，正是我们所需要的关键词。'
#
# tags = jieba.analyse.extract_tags(corpos)
#
# print(",".join(tags))
#
# # 创建词云
# wordcloud = WordCloud(font_path="D:\\PDM\\2.1\\simhei.ttf", background_color="black").generate(",".join(tags))
# plt.imshow(wordcloud)
# plt.axis("off")
# plt.show()
print(re.match(r"window.location.href='(https://www.qu.la/book/.*)", "window.location.href='https://www.qu.la/book/15/?wscckey=1531863923.3635323&wscckey=281cf7e618f3c45e_1531863932'").group(1))
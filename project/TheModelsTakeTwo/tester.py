import panphon
import panphon.sonority
import panphon.segment
ft = panphon.FeatureTable()




print(ft.word_fts('m')[0].match({'cont': -1}))



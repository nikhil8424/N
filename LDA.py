# install.packages(c("tm","topicmodels"))
library(tm)
library(topicmodels)
data <- read.csv("your_dataset.csv", stringsAsFactors = FALSE)
# Text column (edit if needed)
text <- data[[1]]
corpus <- Corpus(VectorSource(text))
corpus <- tm_map(corpus, content_transformer(tolower))
corpus <- tm_map(corpus, removeNumbers)
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, removeWords, stopwords("english"))
dtm <- DocumentTermMatrix(corpus)
lda <- LDA(dtm, k = 3)
# Output
print(terms(lda, 10))
print(posterior(lda)$topics)

#---------------------------
# install.packages(c("tm","syuzhet","wordcloud","RColorBrewer"))
library(tm)
library(syuzhet)
library(wordcloud)
library(RColorBrewer)
data <- read.csv("your_dataset.csv", stringsAsFactors = FALSE)
text <- data[[1]]
# Corpus cleaning
corpus <- Corpus(VectorSource(text))
corpus <- tm_map(corpus, content_transformer(tolower))
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, removeWords, stopwords("english"))
# Wordcloud
tdm <- TermDocumentMatrix(corpus)
m <- as.matrix(tdm)
freq <- sort(rowSums(m), decreasing = TRUE)
wordcloud(names(freq), freq, max.words = 100, colors = brewer.pal(8,"Dark2"))
# Sentiment
sent <- get_nrc_sentiment(text)
barplot(colSums(sent), col = rainbow(10), main="Sentiment")
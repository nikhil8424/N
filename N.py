#——simple web crawler——-
from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
import json
class LinkParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for (key, value) in attrs:
                if key == "href":
                    newUrl = parse.urljoin(self.baseUrl, value)
                    self.links.append(newUrl)
    def getLinks(self, url):
        self.links = []
        self.baseUrl = url   
        try:
            response = urlopen(url)
        except:
            return "", []
        if "text/html" in response.getheader("Content-Type"):
            htmlContent = response.read()
            htmlString = htmlContent.decode("utf-8", errors="ignore")
            self.feed(htmlString)
            response.close()
            return htmlString, self.links
        else:
            return "", []
def crawl(url, word):
    pagesToVisit = [url]
    visitedPages = []
    foundWord = []
    parser = LinkParser()
    while pagesToVisit:
        url = pagesToVisit.pop(0)
        if url not in visitedPages:
            try:
                print("Visiting:", url)
                visitedPages.append(url)
                data, links = parser.getLinks(url)
                if word.lower() in data.lower():
                    foundWord.append(url)
                for link in links:
                    if link not in visitedPages and link not in pagesToVisit:
                        pagesToVisit.append(link)
            except:
                print("Error while accessing:", url)
    return foundWord
if __name__ == "__main__":
    startUrl = "https://example.com"   # safer than Facebook
    searchWord = "example"
    result = crawl(startUrl, searchWord)
    print("\nPages containing the word:")
    print(json.dumps(result, indent=2))

#———edit and weight edit distance——
def edit_distance(s1, s2):
    m, n = len(s1), len(s2)
    # Create DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    # Base cases
    for i in range(m + 1):
        dp[i][0] = i   # delete all
    for j in range(n + 1):
        dp[0][j] = j   # insert all
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                cost = 0
            else:
                cost = 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # delete
                dp[i][j - 1] + 1,      # insert
                dp[i - 1][j - 1] + cost  # replace
            )
    return dp[m][n]
s1 = "kitten"
s2 = "sitting"
print("Edit Distance:", edit_distance(s1, s2))

def weighted_edit_distance(s1, s2, ins_cost=1, del_cost=1, rep_cost=2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
   # Base cases
    for i in range(m + 1):
        dp[i][0] = i * del_cost
    for j in range(n + 1):
        dp[0][j] = j * ins_cost
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                cost = 0
            else:
                cost = rep_cost
            dp[i][j] = min(
                dp[i - 1][j] + del_cost,       # delete
                dp[i][j - 1] + ins_cost,       # insert
                dp[i - 1][j - 1] + cost        # replace
            )
    return dp[m][n]
# Example
s1 = "kitten"
s2 = "sitting"
print("Weighted Edit Distance:", weighted_edit_distance(s1, s2))

#———soundex
def soundex(name):
    name = name.upper()
    first_letter = name[0]
    mappings = {
        "BFPV": "1",
        "CGJKQSXZ": "2",
        "DT": "3",
        "L": "4",
        "MN": "5",
        "R": "6"
    }
    def get_digit(char):
        for key in mappings:
            if char in key:
                return mappings[key]
        return "0"
    encoded = [get_digit(c) for c in name]
    result = [encoded[0]]
    for i in range(1, len(encoded)):
        if encoded[i] != encoded[i - 1]:
            result.append(encoded[i])
    result = [digit for digit in result if digit != "0"]
    result[0] = first_letter
    soundex_code = "".join(result)[:4].ljust(4, "0")
    return soundex_code
names = ["Robert", "Rupert", "Rubin", "Ashcraft", "Ashcroft"]
for n in names:
    print(n, "->", soundex(n))

#——n gram ———
def generate_ngrams(text, n):
    text = text.lower().replace(",", "").replace(".", "")
    words = text.split()
    ngrams = []
    for i in range(len(words) - n + 1):
        ngrams.append(tuple(words[i:i+n]))
    return ngrams
def jaccard(set1, set2):
    inter = len(set1.intersection(set2))
    union = len(set1.union(set2))
    if union == 0:
        return 0
    return inter / union
text1 = input("Enter first text: ")
text2 = input("Enter second text: ")
bigrams1 = generate_ngrams(text1, 2)
bigrams2 = generate_ngrams(text2, 2)
print("\n=== BIGRAMS ===")
print("Text 1:", bigrams1)
print("Text 2:", bigrams2)
trigrams1 = generate_ngrams(text1, 3)
trigrams2 = generate_ngrams(text2, 3)
print("\n=== TRIGRAMS ===")
print("Text 1:", trigrams1)
print("Text 2:", trigrams2)
bigram_set1 = set(bigrams1)
bigram_set2 = set(bigrams2)
trigram_set1 = set(trigrams1)
trigram_set2 = set(trigrams2)
print("\n=== JACCARD COEFFICIENT ===")
print("Bigram Jaccard:", jaccard(bigram_set1, bigram_set2))
print("Trigram Jaccard:", jaccard(trigram_set1, trigram_set2))

#————page rank——-
graph = {
    'A': ['B', 'C'],   # A → B, C
    'B': ['C'],        # B → C
    'C': ['A', 'D'],   # C → A, D
    'D': []            # D has no outgoing links (dangling node)
}
d = 0.85
PR = {'A': 1, 'B': 1, 'C': 1, 'D': 1}
def inbound_links(node, graph):
    incoming = []
    for page in graph:
        if node in graph[page]:
            incoming.append(page)
    return incoming
def compute_PR(node, PR_old):
    incoming = inbound_links(node, graph)
    sum_incoming = 0
    for i in incoming:
        outgoing = len(graph[i])
        if outgoing > 0:
            sum_incoming += PR_old[i] / outgoing
    return (1 - d) + d * sum_incoming
print("Iteration 0:", PR)
iterations = 5
PR_current = PR.copy()
for it in range(1, iterations + 1):
    PR_new = {}
    for node in PR_current:
        PR_new[node] = compute_PR(node, PR_current)
    PR_current = PR_new
    print(f"Iteration {it}:", PR_current)

#———similarty between two text doc
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import numpy as np
import nltk
from collections import defaultdict
nltk.download("punkt")
nltk.download("stopwords")
def process(file):
    raw = open(file, "r", encoding="utf-8").read()
    tokens = word_tokenize(raw)
    words = [w.lower() for w in tokens if w.isalpha()]
    porter = PorterStemmer()
    stemmed_tokens = [porter.stem(t) for t in words]
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [w for w in stemmed_tokens if w not in stop_words]
    count = defaultdict(int)
    for word in filtered_tokens:
        count[word] += 1
    return count
def cos_sim(a, b):
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0
    return dot_product / (norm_a * norm_b)
# Convert dictionaries to vectors and compute similarity
def getSimilarity(dict1, dict2):
    all_words = set(dict1.keys()).union(set(dict2.keys()))
    v1 = np.array([dict1.get(word, 0) for word in all_words])
    v2 = np.array([dict2.get(word, 0) for word in all_words])
    return cos_sim(v1, v2)
if __name__ == "__main__":
    dict1 = process("text1.txt")
    dict2 = process("text2.txt")
    similarity = getSimilarity(dict1, dict2)
    print("Similarity between two text documents:", similarity)

#——-stop word removal
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
stop_words = set(stopwords.words('english'))
def remove_stopwords(text):
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word.isalpha() and word not in stop_words]
    return " ".join(filtered_words)
text = '''Write a program for Pre-processing of a Text Document: stop word removal.
a. Direct text
b. reading text from a text file & importing it in a text file'''
processed_text = remove_stopwords(text)
print("=== DIRECT TEXT ===")
print("Original Text:\n", text)
print("\nAfter Stop Word Removal:\n", processed_text)
with open("input.txt", "r", encoding="utf-8") as file:
    file_text = file.read()
processed_file_text = remove_stopwords(file_text)
with open("output.txt", "w", encoding="utf-8") as file:
    file.write(processed_file_text)
print("\n=== FILE PROCESSING ===")
print("Stop word removal completed.")
print("Check output.txt file.")

#———-indexing and retrieveal
I import re
from collections import defaultdict
documents = {
    1: "Information retrieval is fast",
    2: "Retrieval models are important",
    3: "Information systems and retrieval"
}
def preprocess(text):
    text = text.lower()
    words = re.findall(r'\b[a-z]+\b', text)
    return words
def build_index(docs):
    index = defaultdict(set)
    for doc_id, text in docs.items():
        words = preprocess(text)
        for word in words:
            index[word].add(doc_id)
    return index
def display_index(index):
    print("\n=== INVERTED INDEX (Alphabetical) ===")
    for term in sorted(index.keys()):
        print(term, "->", sorted(index[term]))
def search(query, index):
    words = preprocess(query)
    result = None
    for word in words:
        if word in index:
            if result is None:
                result = index[word]
            else:
                result = result.intersection(index[word])
        else:
            return set()
    return result
index = build_index(documents)
display_index(index)
print("\nTotal Unique Terms:", len(index))
query = input("\nEnter search query: ")
result = search(query, index)
print("\n=== SEARCH RESULT ===")
if result:
    print("Documents containing query:", sorted(result))
else:
    print("No matching documents found.")

#———xml to csv
import csv
import requests
import xml.etree.ElementTree as ET
def load_rss(url, filename):
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, "wb") as f:
        f.write(response.content)
    print("RSS feed saved as:", filename)
def parse_xml(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    newsitems = []
    for item in root.findall(".//item"):
        news = {
            "guid": "",
            "title": "",
            "pubDate": "",
            "description": "",
            "link": ""
        }
        for child in item:
            tag = child.tag.split("}")[-1]  # remove namespace

            if tag in news:
                news[tag] = child.text
        newsitems.append(news)
    return newsitems
def save_to_csv(newsitems, filename):
    fields = ["guid", "title", "pubDate", "description", "link"]
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(newsitems)
    print("CSV file created:", filename)
def main():
    rss_url = "https://feeds.feedburner.com/50WordStories"
    xml_file = "news.xml"
    csv_file = "news.csv"
    load_rss(rss_url, xml_file)
    data = parse_xml(xml_file)
    save_to_csv(data, csv_file)
if __name__ == "__main__":
    main()

#——- bitwise
plays = {
    "Antony and Cleopatra": "Anthony is there Brutus is Caesar is with Cleopatra mercy worser",
    "Julius Caesar": "Anthony is there Brutus is Caesar but Calpurnia is",
    "The Tempest": "mercy worser",
    "Hamlet": "Caesar and Brutus are present with mercy and worser",
    "Othello": "Caesar is present with mercy and worser",
    "Macbeth": "Anthony is there Caesar mercy"
}
words = ["anthony","brutus","caesar","calpurnia","cleopatra","mercy","worser"]
def build_index(plays):
    index = {}
    for word in words:
        index[word] = set()
    for doc, text in plays.items():
        text = text.lower()
        for word in words:
            if word in text:
                index[word].add(doc)
    return index
# -------- DISPLAY INDEX --------
def display_index(index):
    print("\n=== INVERTED INDEX ===")
    for term in sorted(index.keys()):
        print(term, "->", index[term])
# -------- BOOLEAN OPERATIONS --------
def AND(a, b):
    return a & b
def OR(a, b):
    return a | b
def NOT(a, all_docs):
    return all_docs - a
# -------- MAIN --------
index = build_index(plays)
display_index(index)
all_docs = set(plays.keys())
# -------- QUERIES --------
print("\n=== QUERY RESULTS ===")
# 1. Brutus AND Caesar AND NOT Calpurnia
q1 = AND(AND(index["brutus"], index["caesar"]),
         NOT(index["calpurnia"], all_docs))
print("\nBrutus AND Caesar AND NOT Calpurnia:")
print(q1)
# 2. (Brutus AND Caesar) OR (Anthony AND NOT Cleopatra)
q2 = OR(
    AND(index["brutus"], index["caesar"]),
    AND(index["anthony"], NOT(index["cleopatra"], all_docs))
)
print("\n(Brutus AND Caesar) OR (Anthony AND NOT Cleopatra):")
print(q2)
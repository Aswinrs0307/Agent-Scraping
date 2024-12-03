# filename: read_article.py
with open("article_content.txt", "r", encoding="utf-8") as file:
    article_content = file.read()

print(article_content)
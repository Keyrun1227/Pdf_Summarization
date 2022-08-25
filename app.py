from flask import request,render_template
from flask import Flask
import PyPDF2
import nltk
import re
import heapq
import os

app=Flask(__name__)



@app.route('/')
def home():
    return render_template("home.html")
@app.route('/pdf', methods =['POST'])
def komali():
     submit=request.form['cat']
     if request.method=="POST":
        n=int(request.form['a'])
        file=request.files['filename']
        if file:
           a =PyPDF2.PdfFileReader(file)
           k=a.getNumPages()
           str=""
           for i in range(k):
               str+=a.getPage(i).extractText() 
           str= re.sub(r'\[[0-9]*\]', ' ', str)
           str = re.sub(r'\s+', ' ', str)
           formatted_article_text = re.sub('[^a-zA-Z]', ' ', str )
           formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
           sentence_list=nltk.sent_tokenize(str)
           stopwords=nltk.corpus.stopwords.words('english')    
           word_frequencies={}
           for word in nltk.word_tokenize(formatted_article_text):
               if word not in stopwords:
                   if word not in word_frequencies.keys():
                       word_frequencies[word]=1
                   else:
                       word_frequencies[word]+=1
           max_frequency=max(word_frequencies.values())
           for word in word_frequencies.keys():
               word_frequencies[word]=(word_frequencies[word]/max_frequency)
           sentence_scores={}
           for sent in sentence_list:
               for word in nltk.word_tokenize(sent.lower()):
                   if word in word_frequencies.keys():
                       if len(sent.split(' '))<30:
                           if sent not in sentence_scores.keys():
                               sentence_scores[sent]=word_frequencies[word]
                           else:
                               sentence_scores[sent]+=word_frequencies[word]  
           summary_sentences=heapq.nlargest(n,sentence_scores,key=sentence_scores.get)
           summary=''.join(summary_sentences)
           if submit=='summary':
               sol=summary
           elif submit=="sentence_list":
               sol=sentence_list 
           elif submit=="text":
               sol=str
           elif submit=="formatted_at":
               sol=formatted_article_text 
           elif submit=="stopwords":
               sol=stopwords 
           else:
               sol=word_frequencies
     return render_template('after.html',data=sol)

if __name__ == "__main__":
    app.run(debug=True)
    
    
    
    
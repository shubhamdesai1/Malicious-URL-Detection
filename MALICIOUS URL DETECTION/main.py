import re
# import nltk.tokenizer
# from transformers import AutoTokenizer
from urllib.parse import urlparse
from flask import Flask, render_template, render_template_string, request
from matplotlib.pyplot import text
from requests import post
import numpy as np
import pickle
from sklearn.metrics import accuracy_score
from tld import get_tld



list = []
app = Flask(__name__)
@app.route("/",methods=['GET','POST'])
def home(): 
    if request.method=='GET':
        return render_template("homepage.html")

    elif request.method=='POST':
        return render_template("homepage.html")




def hostname_length(url):
    list.clear()
    list.append(len(urlparse(url).netloc))
    print("hostname called & list is  ", list)

def path_length(url):
    list.append(len(urlparse(url).path))

def fd_length(url):
    urlpath= urlparse(url).path
    try:
        list.append(len(urlpath.split('/')[1]))
    except:
        list.append(0)

def tld_length(url):
    tld = get_tld(url,fail_silently=True)

    try:
        list.append(len(tld))
    except:
        list.append(-1)

def counts_dash(url):
    list.append(url.count('-'))


    

def count_atherate(url):
    list.append(url.count('@'))

def count_question_mark(url):
    list.append(url.count('?'))

def count_percent(url):
    list.append(url.count('%'))

def count_dot(url):
    list.append(url.count('.'))

def count_equal_to(url):
    list.append(url.count('='))

def count_http(url):
    list.append(url.count('http'))

def count_https(url):
    list.append(url.count('https'))

def count_www(url):
    list.append(url.count('www'))

def digit_count(url):
    digits = 0
    for i in url:
        if i.isnumeric():
            digits = digits + 1
    list.append(digits)

def letter_count(url):
    letters = 0
    for i in url:
        if i.isalpha():
            letters = letters + 1
    list.append(letters)

def no_of_dir(url):
    urldir = urlparse(url).path
    list.append(urldir.count('/'))

def having_ip_address(url):
    match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
    if match:
        list.append(-1)
    else:
        # print 'No matching pattern found'
        list.append(1)

def Tokens(f):
    tkns_BySlash = str(f.encode('utf-8')).split('/')	# make tokens after splitting by slash
    total_Tokens = []
    for i in tkns_BySlash:
        tokens = str(i).split('-')	# make tokens after splitting by dash
        tkns_ByDot = []
        for j in range(0,len(tokens)):
            temp_Tokens = str(tokens[j]).split('.')	# make tokens after splitting by dot
            tkns_ByDot = tkns_ByDot + temp_Tokens
        total_Tokens = total_Tokens + tokens + tkns_ByDot
    # total_Tokens = list(set(total_Tokens))	#remove redundant tokens
    total_Tokens = set(total_Tokens)	#remove redundant tokens

    if 'com' in total_Tokens:
        total_Tokens.remove('com')	#removing .com since it occurs a lot of times and it should not be included in our features
    return total_Tokens
    

def getscores(text):
    print("Text in getscore is : ", text)
    url = text
    print("URL afte rassiging varibale :", url)
    hostname_length(url)
    path_length(url)
    fd_length(url)
    tld_length(url)
    counts_dash(url)
    count_atherate(url)
    count_question_mark(url)
    count_percent(url)
    count_dot(url)
    count_equal_to(url)
    count_http(url)
    count_https(url)
    count_www(url)
    digit_count(url)
    letter_count(url)
    no_of_dir(url)
    having_ip_address(url)
    review_array = np.array([list])
    pickled_model = pickle.load(open('model2', 'rb'))
    score1 = pickled_model.predict(review_array)
    # accuracy1 = pickled_model.score(X_test,Y_test)
    var1 = score1[0]
    model2_score = var1
    pickled_model2 = pickle.load(open('model3', 'rb'))
    score2 = pickled_model2.predict(review_array)
    # accuracy2 = pickled_model2.score()
    var2 = score2[0]
    model3_score = var2
    url21= [text]
    loaded_vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
    loaded_model = pickle.load(open('model1.pkl', 'rb'))
    variable3 = loaded_model.predict(loaded_vectorizer.transform(url21))
    # accuracy3 = loaded_model.score()
    if (variable3[0] == 'bad'):
        var3 = 1
    elif (variable3[0] == 'good'):
        var3 = 0
    model1_score = var3
    final_score = var1 + var2 + var3
    all_score_list = [final_score, model1_score, model2_score, model3_score]
    return all_score_list
    
    


@app.route("/result", methods = ['POST','GET'])
def result():
    if request.method=='GET':
        return render_template("result.html")

    elif request.method=='POST':
        text = request.form['searchQueryInput']
        results = getscores(text) 
        if (results[0]<2):
            return render_template("result.html", value = results[0] , value2 = text, model1_score = results[1], model2_score = results[2], model3_score = results[3])
        elif(results[0] == 2):
            return render_template("result1.html", value = results[0] , value2 = text, model1_score = results[1], model2_score = results[2], model3_score = results[3])
        elif(results[0] == 3):
            return render_template("result2.html", value = results[0] , value2 = text, model1_score = results[1], model2_score = results[2], model3_score = results[3])

if __name__ == "__main__":
    app.run(debug=True)

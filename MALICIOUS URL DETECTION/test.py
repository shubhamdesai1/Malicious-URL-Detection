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
    # total_Tokens = set(total_Tokens)	#remove redundant tokens
    total_Tokens = list(set(total_Tokens))	#remove redundant tokens

    if 'com' in total_Tokens:
        total_Tokens.remove('com')	#removing .com since it occurs a lot of times and it should not be included in our features
    print(total_Tokens)
    return total_Tokens

import pickle


# X_predict1 = ["google.com/search=jcharistech"]
X_predict1 = ["https://www.youtube.com/watch?v=nnG0WDHCn3s"]
loaded_vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

    # load the model
loaded_model = pickle.load(open('model1.pkl', 'rb'))

    # make a prediction
print(loaded_model.predict(loaded_vectorizer.transform(X_predict1)))
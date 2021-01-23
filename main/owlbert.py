import random
import json
import pickle
import numpy as np
from datetime import date
import time

import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

from flask import Flask, render_template
import flask
app = Flask(__name__)


lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbotmodel.h5')

print(classes)
print(words)

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key = lambda x: x[1], reverse = True) 
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability' : str(r[1])})
    return return_list


def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

print("BOT is running....")
print("Start chatting!!")

'''
while True:
    message = input("YOU:: ")
    if(message == "EXIT"):
        print("Good Bye !!")
        break
    ints = predict_class(message)
    res = get_response(ints, intents)
    if('date' in message.lower() and 'time' in message.lower()):
        print("=>   ", "Date: ", today, ", Time: ", current_time, end="\n\n")
    elif('date' in message.lower()):
        print("=>   ", "Date: ", today, end="\n\n")
    elif('time' in message.lower()):
        print("=>   ", "Time: ", current_time, end="\n\n")
    else:
        print("=>   ",res,end="\n\n")
'''

@app.route('/')
def home():
   return render_template('index.html')


@app.route('/owlbert/chat/', methods=['GET','POST'])
def index():
    today = date.today()
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    json_data = flask.request.json
    message = json_data["message"]
    ints = predict_class(message)
    res = get_response(ints, intents)
    if('date' in message.lower() and 'time' in message.lower()):
        return f"Date:  {today} , Time:  {current_time}"
    elif('date' in message.lower()):
        return f"Date:  {today}"
    elif('time' in message.lower()):
        return f"Time:  {current_time}"
    else:
        return f"{res}"


if __name__ == '__main__':
   app.run()
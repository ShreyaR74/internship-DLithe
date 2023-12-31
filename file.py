#Imports
from flask import Flask, render_template, request, jsonify
import nltk
import datetime
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tflearn
import tensorflow as tf
import random
import json
import pickle
from IPython.core.display import display, HTML, Markdown
stemmer = LancasterStemmer()
with
open("C:\\Users\\Shreya\\Documents\\miniproject\\intents1.json",encoding="utf8")
as file:
data = json.load(file)
#Initializing empty lists
words = []
labels = []
docs_x = []
docs_y = []
#Looping through our data
for intent in data['intents']:
for pattern in intent['patterns']:
pattern = pattern.lower()
#Creating a list of words
wrds = nltk.word_tokenize(pattern)
words.extend(wrds)
docs_x.append(wrds)
docs_y.append(intent['tag'])
if intent['tag'] not in labels:
labels.append(intent['tag'])
stemmer = LancasterStemmer()
words = [stemmer.stem(w.lower()) for w in words if w not in "?"]
words = sorted(list(set(words)))
labels = sorted(labels)
training = []
output = []
out_empty = [0 for _ in range(len(labels))]
for x,doc in enumerate(docs_x):
bag = []
wrds = [stemmer.stem(w) for w in doc]
for w in words:
if w in wrds:
bag.append(1)
else:
bag.append(0)
output_row = out_empty[:]
output_row[labels.index(docs_y[x])] = 1
training.append(bag)
output.append(output_row)
#Converting training data into NumPy arrays
training = np.array(training)
output = np.array(output)
#Saving data to disk
with open("data.pickle","wb") as f:
pickle.dump((words, labels, training, output),f)
tf.compat.v1.reset_default_graph()
net = tflearn.input_data(shape = [None, len(training[0])])
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,len(output[0]), activation = "softmax")
net = tflearn.regression(net)
model = tflearn.DNN(net)
model.fit(training, output, n_epoch = 200, batch_size = 8, show_metric = True)
model.save("model.tflearn")
with
open("C:\\Users\\Shreya\\Documents\\miniproject\\intents1.json",encoding="utf8")
as file:
data = json.load(file)
with open("data.pickle","rb") as f:
words, labels, training, output = pickle.load(f)
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
#Function to process input
def bag_of_words(s, words):
bag = [0 for _ in range(len(words))]
s_words = nltk.word_tokenize(s)
s_words = [stemmer.stem(word.lower()) for word in s_words]
for se in s_words:
for i,w in enumerate(words):
if w == se:
bag[i] = 1
return np.array(bag)
tf.compat.v1.reset_default_graph()
net = tflearn.input_data(shape = [None, len(training[0])])
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,len(output[0]), activation = "softmax")
net = tflearn.regression(net)
#Loading existing model from disk
model = tflearn.DNN(net)
model.load("model.tflearn")
from flask import Flask,render_template
app = Flask(__name__,template_folder='templates')
@app.route('/')
def index():
return render_template('index.html')
@app.route('/get')
def get_bot_response():
global seat_count
message = request.args.get('msg')
if message:
message = message.lower()
results = model.predict([bag_of_words(message,words)])[0]
result_index = np.argmax(results)
tag = labels[result_index]
if results[result_index] > 0.5:
for tg in data['intents']:
if tg['tag'] == tag:
responses = tg['responses']
response = random.choice(responses)
else:
file1 = open("myfile.txt", "a") # append mode
file1.write(message)
file1.write("\n")
file1.close()
response = "I didn't quite get that, please try again later.....I will be able to
answer this question soon..."
return str(response)
return "Missing Data!"
if __name__ == "__main__":
app.run(debug=True, host='0.0.0.0', port=500
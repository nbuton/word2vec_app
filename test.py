from flask import Flask
from flask import render_template, request
import gensim
import webbrowser
import os
import sys
#import subprocess
import webview
import time
from multiprocessing import Process
import os
import smart_open

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


app = Flask(__name__,template_folder=resource_path('templates/'))
app.config["CACHE_TYPE"] = "null"

model = None

@app.route('/')
def accueil():
    charge_model()
    return render_template('index.html', titre="Bienvenue !")

@app.route('/analogie')
def analogie():
    return render_template('analogie.html')


@app.route('/send_txt', methods=['GET', 'POST'])
def send_txt():
    if request.method == 'POST':
        mots = test_word_to_vec(request.form["contenu"])
        return render_template('result.html',mots=mots,mot_recherche=request.form["contenu"])

@app.route('/send_txt2', methods=['GET', 'POST'])
def send_txt2():
    if request.method == 'POST':
        mots = analogie_word2vec(request.form["pos1"],request.form["pos2"],request.form["neg1"])
        return render_template('result2.html',mots=mots,pos1=request.form["pos1"],pos2=request.form["pos2"],neg1=request.form["neg1"])


def charge_model():
    global model
    if(model == None):
        model = gensim.models.KeyedVectors.load_word2vec_format(resource_path('frWac_non_lem_no_postag_no_phrase_200_cbow_cut100.bin'),binary=True)
        print("Je charge le modele")

def analogie_word2vec(pos1,pos2,neg1):
    global model
    try:
        resp = model.most_similar(positive=[pos1, pos2], negative=[neg1])
        return [r[0] for r in resp[:9]]
    except:
        return ["Mot non trouvé"]


def test_word_to_vec(mot):
    global model
    try:
        resp = model.most_similar(positive=[mot])
        return [r[0] for r in resp[:9]]
    except:
        return ["Mot non trouvé"]


def my_webbrowser():
    webview.create_window("","http://127.0.0.1:5000/")
    webview.start()

def start_server():
    app.run()#debug=True

if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000/")
    start_server()
    #p = Process(target=start_server)
    #p.start()
    #t = threading.Thread(target = start_server)
    #t.start()
    time.sleep(2)
    #my_webbrowser()
    #p.terminate()
    #sys.exit()
    #exit(0)

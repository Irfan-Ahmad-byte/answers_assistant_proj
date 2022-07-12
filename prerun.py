# sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
# sudo apt-get install ffmpeg espeak
import subprocess

subprocess.run('pip install -r req.txt', shell=True)
subprocess.run("python -m spacy download en_core_web_sm", shell=True)

import nltk

nltk.download("stopwords")
nltk.download("wordnet")


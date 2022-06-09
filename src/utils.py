import os
from pathlib import Path
import magic
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import re


def findEncoding(blob):
    m = magic.Magic(mime_encoding=True)
    encoding = m.from_buffer(blob)
    return encoding


def findStopWords(dir_name):

    dir_path = os.path.join(
        Path(__file__).resolve().parent.parent, dir_name)
    temp_path = os.getcwd()
    os.chdir(dir_path)

    stop_words = []

    for filename in os.listdir():
        encoding = findEncoding(open(filename, "rb").read())

        # may have used latin-1

        with open(file=filename, mode="r", encoding=encoding) as file:
            content = file.read()
            content = content.split("\n")
            for stop_word in content:
                stop_word = stop_word.split("|")[0].strip()
                stop_words.append(stop_word.lower())

    os.chdir(temp_path)
    return stop_words


stop_words = findStopWords(dir_name="StopWords")


def clean(content, stop_words):
    return list(set(content).difference(set(stop_words)))


def findWords(dir_name, filename):

    dir_path = os.path.join(
        Path(__file__).resolve().parent.parent, dir_name)
    temp_path = os.getcwd()
    os.chdir(dir_path)

    words = {}

    encoding = findEncoding(open(filename, "rb").read())
    with open(file=filename, mode="r", encoding=encoding) as file:
        content = file.read().split("\n")
        content = clean(content=content, stop_words=stop_words)
        for word in content:
            words[word.lower()] = True

    os.chdir(temp_path)
    return words


argument = {
    "dir_name": "MasterDictionary"
}

positive_words = findWords(**argument, filename="positive-words.txt")
negative_words = findWords(**argument, filename="negative-words.txt")


def sentimentalAnalysis(content):

    content = clean(content=content, stop_words=stop_words)

    positive_score = 0
    negative_score = 0

    for token in content:
        if positive_words.get(token):
            positive_score += 1
        if negative_words.get(token):
            negative_score += 1

    polarity_score = (positive_score - negative_score) / \
        (positive_score + negative_score + 0.000001)

    subjectivity_score = (positive_score - negative_score) / \
        (len(content) + 0.000001)

    return positive_score, negative_score, polarity_score, subjectivity_score


def countSyllables(word):
    word = word.lower()
    word = word.rstrip("es").rstrip("ed")
    count = 0
    vowels = ["a", "e", "i", "o", "u"]
    for ch in word:
        if ch in vowels:
            count += 1
    return count


def countComplex(content):

    # assuming content is words

    count = 0
    for token in content:
        if countSyllables(token) > 2:
            count += 1
    return count


def readabilityAnalysis(content):

    words = word_tokenize(content.lower())
    sentences = sent_tokenize(content)

    avg_sentence_len = len(words) / len(sentences)
    complex_word_count = countComplex(words)
    complex_words_percent = complex_word_count / len(words)
    fog_index = 0.4 * (avg_sentence_len + complex_words_percent)

    return avg_sentence_len, complex_words_percent, fog_index, complex_word_count


nltk_stop_words = stopwords.words("english")


def countCleanWords(content):

    # assume content is words

    content = clean(content=content, stop_words=nltk_stop_words)
    return len(content)


def findPersonalPronouns(content):

    # assuming content is complete para
    # assuming org content (wrt lowercase char)

    personal_pronouns = re.findall(
        r"(i|we|my|ours|us)", content.replace("US", "").lower())
    return len(personal_pronouns)


def findAvgWordLen(content):

    # assuming content is words

    count = 0
    for token in content:
        count += len(token)
    return count / len(content)


def findSyllableCountPerWord(content):

    # assuming content is words

    count = 0
    for token in content:
        count += countSyllables(token)
    return count / len(content)

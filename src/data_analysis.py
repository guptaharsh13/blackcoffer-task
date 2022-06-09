from nltk.tokenize import word_tokenize
from utils import sentimentalAnalysis, readabilityAnalysis, countCleanWords, findPersonalPronouns, findAvgWordLen, findSyllableCountPerWord
import os
from pathlib import Path
from openpyxl import Workbook
import concurrent.futures

# Don't forget to convert to lowercase


def analyseContent(content):

    words = word_tokenize(content.lower())

    positive_score, negative_score, polarity_score, subjectivity_score = sentimentalAnalysis(
        words)
    avg_sentence_len, complex_words_percent, fog_index, complex_word_count = readabilityAnalysis(
        content=content)

    avg_words_per_sentence = avg_sentence_len

    word_count = countCleanWords(content=words)

    syllable_count_per_word = findSyllableCountPerWord(words)

    personal_pronouns = findPersonalPronouns(content=content)

    avg_word_len = findAvgWordLen(content=words)

    return [positive_score, negative_score, polarity_score, subjectivity_score, avg_sentence_len, complex_words_percent, fog_index, avg_words_per_sentence, complex_word_count, word_count, syllable_count_per_word, personal_pronouns, avg_word_len]


def saveOutput(urls, analytics):

    wb = Workbook()
    sheet = wb.active

    data = [("URL_ID", "URL", "POSITIVE SCORE", "NEGATIVE SCORE", "POLARITY SCORE", "SUBJECTIVITY SCORE", "AVG SENTENCE LENGTH", "PERCENTAGE OF COMPLEX WORDS",
             "FOG INDEX", "AVG NUMBER OF WORDS PER SENTENCE", "COMPLEX WORD COUNT", "WORD COUNT", "SYLLABE PER WORD", "PERSONAL PRONOUNS", "AVG WORD LENGTH")]

    for url_id, url in urls.items():
        data.append((url_id, url, *analytics.get(url_id)))

    for i in data:
        sheet.append(i)

    output_file_path = os.path.join(
        Path(__file__).resolve().parent.parent, "Output.xlsx")

    wb.save(output_file_path)


def analyseFile(filename):
    with open(file=filename, mode="r") as file:
        content = file.read()
    return analyseContent(content=content)


def analyseFiles(dir_name, urls):

    # try-catch or default arguments

    dir_path = os.path.join(
        Path(__file__).resolve().parent.parent, dir_name)
    temp_path = os.getcwd()
    os.chdir(dir_path)

    analytics = {}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(analyseFile, filename): filename for filename in os.listdir()}

        for future in concurrent.futures.as_completed(fs=futures):
            filename = futures[future]
            analytics["".join(filename.split(".")[:-1])] = future.result()

    os.chdir(temp_path)

    saveOutput(urls=urls, analytics=analytics)

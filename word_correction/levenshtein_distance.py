import streamlit as st


def levenshtein_distance(s, t):
    m, n = len(s), len(t)
    current_row = range(m + 1)
    for i in range(1, n + 1):
        previous_row, current_row = current_row, [i] + [0] * m
        for j in range(1, m + 1):
            add, delete, change = previous_row[j] + \
                1, current_row[j - 1] + 1, previous_row[j - 1]
            if s[j - 1] != t[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)
    return current_row[m]


def load_vocab(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    words = sorted(set([line.strip().lower() for line in lines]))
    return words


vocabs = load_vocab(
    file_path='aio2024_streamlit_project/word_correction/data/vocab.txt')


def main():
    st.title("Word Correction using Levenshtein Distance")
    word = st.text_input('Word:')

    if st.button("Compute"):

        # compute levenshtein distance
        leven_distances = dict()
        for vocab in vocabs:
            leven_distances[vocab] = levenshtein_distance(word, vocab)

        # sorted by distance
        sorted_distences = dict(
            sorted(leven_distances.items(), key=lambda item: item[1]))
        correct_word = list(sorted_distences.keys())[0]
        st.write('Correct word: ', correct_word)

        col1, col2 = st.columns(2)
        col1.write('Vocabulary:')
        col1.write(vocabs)

        col2.write('Distances:')
        col2.write(sorted_distences)


if __name__ == "__main__":
    main()

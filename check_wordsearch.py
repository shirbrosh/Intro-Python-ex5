from wordsearch import count_word_in_matrix


def check_count_word_in_matrix():
    """A function that tests the function count_word_in_matrix from wordsearch-
    checks 3 different inputs and return True if the function works and False
    otherwise"""
    count_test = 0
    counter = 0
    counter = count_word_in_matrix("bee", "ebbeeb", counter)
    if counter == 1:
        count_test += 1
    counter = 0
    counter = count_word_in_matrix("dad", "dadadad", counter)
    if counter == 3:
        count_test += 1
    counter = 0
    counter = count_word_in_matrix("pepper", "ppepperppepper", counter)
    if counter == 2:
        count_test += 1
    if count_test == 3:
        return True
    else:
        return False


if __name__ == '__main__':
    check_count_word_in_matrix()

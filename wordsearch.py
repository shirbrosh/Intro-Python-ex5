import os
import sys

NUM_ARGS = 4
DIRECTION = ["u", "d", "r", "l", "w", "x", "y", "z"]


def check_input_args(args):
    """A function that receives the arguments as string inputs and looks for
    errors in the arguments, if there's an error a suitable message will be
    returned, and if not the value None will be returned"""
    if len(args) != NUM_ARGS:
        msg = "Error: the number of inputs is incorrect"
        return msg
    elif not os.path.exists(args[0]):
        msg = "Error: file 'words_file' does not exist"
        return msg
    elif not os.path.exists(args[1]):
        msg = "Error: file 'matrix_file' does not exist"
        return msg
    for char in args[3]:
        if char not in DIRECTION or char == " ":
            msg = "Error: the direction char is incorrect"
            return msg
    else:
        return None


def read_wordlist_file(filename):
    """A function that receives the words file and returns a list of all the
    words in the file"""
    file_name_open = open(filename)
    file_name_string = file_name_open.read()
    list_words = file_name_string.split('\n')
    list_words.remove("")
    return list_words


def read_matrix_file(filename):
    """A function that receives the matrix file and returns a list of lists
    each list is a row of letters in the matrix"""
    file_name_open = open(filename)
    list_matrix = []
    for line in file_name_open:
        list_row = line.strip().split(",")
        list_matrix.append(list_row)
    return list_matrix


def count_word_in_matrix(word, row_as_string, counter_word):
    """A function that counts how many times a word appears in matrix row"""
    while word in row_as_string:
        counter_word += 1
        index_word = row_as_string.index(word)
        row_as_string = row_as_string[index_word + 1:]
    return counter_word


def direction_r(word_list, matrix, dictionary):
    """A function that receives a words list and a matrix and creates a
    dictionary for each word from the words list that also appear in the matrix
    to the right direction, each key refers to the number of times the word
    appears in the matrix"""
    for word in word_list:
        counter_word = 0
        for row_matrix in matrix:
            row_as_string = "".join(row_matrix)
            counter_word = count_word_in_matrix(word, row_as_string,
                                                counter_word)
        if counter_word > 0:
            dictionary[word] = dictionary[word] + counter_word
    print(dictionary)
    return dictionary


def direction_l(word_list, matrix, dictionary):
    """A function that receives a words list and a matrix and creates a
    dictionary for each word from the words list that also appear in the
    matrix to the left direction, each key refers to the number of times
    the word appears in the matrix"""
    for word in word_list:
        counter_word = 0
        for row_matrix in matrix:
            row_as_string = "".join(row_matrix)
            row_as_string_reverse = row_as_string[::-1]
            counter_word = count_word_in_matrix(word, row_as_string_reverse,
                                                counter_word)
        if counter_word > 0:
            dictionary[word] = dictionary[word] + counter_word
    return dictionary


def direction_d(word_list, matrix, dictionary):
    """A function that receives a words list and a matrix and creates a
    dictionary for each word from the words list that also appear in the matrix
    to the "down" direction, each key refers to the number of times the word
    appears in the matrix"""
    matrix_transpose = [list(i) for i in zip(*matrix)]
    dictionary1 = direction_r(word_list, matrix_transpose, dictionary)
    return dictionary1


def direction_u(word_list, matrix, dictionary):
    """A function that receives a words list and a matrix and creates a
    dictionary for each word from the words list that also appear in the matrix
    to the "up" direction, each key refers to the number of times the word
    appears in the matrix"""
    matrix_transpose = [list(i) for i in zip(*matrix)]
    dictionary1 = direction_l(word_list, matrix_transpose, dictionary)
    return dictionary1


def turn_matrix_diagonal_down(matrix):
    """A function that receives a matrix (list of lists) and return a new
    matrix each row (list) is a diagonal (down right) from the original
    matrix"""
    diagonal_matrix = []
    # upper triangle
    i = 0
    while i < len(matrix[0]):
        j = 0
        diagonal_matrix_row = []
        for matrix_row in matrix:
            if j + i < len(matrix[0]):
                diagonal_matrix_row.append(matrix_row[j + i])
                j += 1
        i += 1
        diagonal_matrix.append(diagonal_matrix_row)
    # lower triangle
    j = 1
    while j < len(matrix):
        i = 0
        diagonal_matrix_row = []
        for matrix_row in range(j, len(matrix)):
            if i < len(matrix) - 1 and i < len(matrix[0]):
                diagonal_matrix_row.append(matrix[matrix_row][i])
                i += 1
        j += 1
        diagonal_matrix.append(diagonal_matrix_row)
    return diagonal_matrix


def direction_y(word_list, matrix, dictionary):
    """A function that receives a words list and a matrix and creates a
    dictionary for each word from the words list that also appear in the matrix
    to the diagonal down right direction, each key refers to the number of
    times the word appears in the matrix"""
    diagonal_matrix = turn_matrix_diagonal_down(matrix)
    dictionary1 = direction_r(word_list, diagonal_matrix, dictionary)
    return dictionary1


def direction_x(word_list, matrix, dictionary):
    """A function that receives a words list and a matrix and creates a
    dictionary for each word from the words list that also appear in the matrix
    to the diagonal up left direction, each key refers to the number of
    times the word appears in the matrix"""
    diagonal_matrix = turn_matrix_diagonal_down(matrix)
    dictionary1 = direction_l(word_list, diagonal_matrix, dictionary)
    return dictionary1


def matrix_up_side_down(matrix):
    """A function that receives a matrix and returns a new one composed from
    the rows (lists) of the original matrix in reverse order (the first row
    (list) will be the last in the new matrix)"""
    matrix_up_side_down_list = []
    for i in range(len(matrix) - 1, -1, -1):
        matrix_up_side_down_list.append(matrix[i])
    return matrix_up_side_down_list


def direction_w(word_list, matrix, dictionary):
    """A function that receives a words list and a matrix and creates a
    dictionary for each word from the words list that also appear in the matrix
    to the diagonal up right direction, each key refers to the number of
    times the word appears in the matrix"""
    matrix_up_side_down_list = matrix_up_side_down(matrix)
    dictionary1 = direction_y(word_list, matrix_up_side_down_list, dictionary)
    return dictionary1


def direction_z(word_list, matrix, dictionary):
    """A function that receives a words list and a matrix and creates a
    dictionary for each word from the words list that also appear in the matrix
    to the diagonal down left direction, each key refers to the number of
    times the word appears in the matrix"""
    matrix_up_side_down_list = matrix_up_side_down(matrix)
    dictionary1 = direction_x(word_list, matrix_up_side_down_list, dictionary)
    return dictionary1


def create_dictionary(word_list):
    """A function that creates a new dictionary each key is a word from
    word_list each key points to 0, which is the number of times the word
    appeared in the matrix so far"""
    dictionary = {}
    for word in word_list:
        dictionary[word] = 0
    return dictionary


def word_in_matrix_dictionary(word_list, dictionary):
    """A function that receives a word list and a dictionary and creates a new
    word list containing only the words that appear in the matrix"""
    new_word_list = []
    for word in word_list:
        if dictionary[word] == 0:
            del dictionary[word]
        else:
            new_word_list.append(word)
    return new_word_list


def find_words_in_matrix(word_list, matrix, directions):
    """A function that receives a words list, a matrix and directions to search
    the matrix, and returns a new list containing tuples- each tuple is a word
    appeared in the matrix in one of the directions to search and the number of
    times it appeared"""
    dictionary = create_dictionary(word_list)
    if "r" in directions:
        dictionary = direction_r(word_list, matrix, dictionary)
    if "l" in directions:
        dictionary = direction_l(word_list, matrix, dictionary)
    if "u" in directions:
        dictionary = direction_u(word_list, matrix, dictionary)
    if "d" in directions:
        dictionary = direction_d(word_list, matrix, dictionary)
    if "w" in directions:
        dictionary = direction_w(word_list, matrix, dictionary)
    if "x" in directions:
        dictionary = direction_x(word_list, matrix, dictionary)
    if "y" in directions:
        dictionary = direction_y(word_list, matrix, dictionary)
    if "z" in directions:
        dictionary = direction_z(word_list, matrix, dictionary)
    new_word_list = word_in_matrix_dictionary(word_list, dictionary)
    results = [(word, dictionary[word]) for word in new_word_list]
    return results


def write_output_file(results, output_filename):
    """A function that receives a list of tuples and an output file name and
    creates a file containing the values of the list- words that appear in the
    matrix and how many times """
    output_file = open(output_filename, "w+")
    for i in range(len(results)):
        word = str(results[i][0])
        count = str(results[i][1])
        output_file.write(word
                          + "," + count + "\n")
    output_file.close()


def main_game(args):
    """A function that receives a list of arguments and operates the game using
    the auxiliary functions"""
    if check_input_args(args) is not None:
        return
    result_list = find_words_in_matrix(read_wordlist_file(args[0]),
                                       read_matrix_file(args[1]), args[3])
    write_output_file(result_list, args[2])


if __name__ == '__main__':
    direction_r("")
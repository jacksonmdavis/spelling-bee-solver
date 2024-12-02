from flask import Blueprint, jsonify, request

api_bp = Blueprint('api', __name__)

@api_bp.route('/process', methods=['POST'])
def process():
    data = request.json
    # Process the input data here
    center_letter = data['center_letter'].lower()
    other_letters = data['other_letters'].lower()
    return solver(center_letter, other_letters)


def load_words(filename, center_letter, other_letters):
    center_letter = center_letter.lower()
    other_letters = other_letters.lower()

    all_letters = center_letter + other_letters

    with open(filename) as word_file:
        words = set(word.strip().lower() for word in word_file)
    
    words = [word for word in words if center_letter in word]
    words = [word for word in words if all(letter in all_letters for letter in word) and len(word) >= 4]
    # words = sorted(words, key=lambda x: (-len(x), x))
    return set(words)


def solver(center_letter, other_letters, debug=False):
    words_10k = load_words('word_list_10k.txt', center_letter, other_letters)
    words_30k = load_words('word_list_30k.txt', center_letter, other_letters) - words_10k
    words_wiki = load_words('word_list_wiki.txt', center_letter, other_letters) - words_10k - words_30k
    words_full = load_words('word_list_full.txt', center_letter, other_letters) - words_10k - words_30k - words_wiki

    if debug:
        return {'result': {'10k': list(words_10k), '30k': list(words_30k), 'wiki' : list(words_wiki), 'full': list(words_full)}}
    else:
        return jsonify({'result': {'10k': list(words_10k), '30k': list(words_30k), 'wiki' : list(words_wiki), 'full': list(words_full)}})

    # return jsonify({'result': {'10k': list(words_10k), '30k': list(words_30k), 'full': list(words_full)}})

if __name__ == '__main__':
    print(solver('l', 'orcyph', debug=True))
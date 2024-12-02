from flask import Blueprint, jsonify, request

api_bp = Blueprint('api', __name__)

@api_bp.route('/solver', methods=['POST'])
def process():
    """
    POST /solver
    Description:
        Finds words based on the center and other letters provided in the request.  Note that each returned list
        is a set that has already removed duplicates from the smaller lists so the full list can be ordered roughly
        by frequency of use in the English language.
    Request Body:
        {
            "center_letter": "a",   # Required, a single letter
            "other_letters": "bcdefg" # Required, other letters to use (6 letters for Spelling Bee)
        }
    Response:
        200 OK:
        {
            "result": {
                "10k": [...],       # Words from the 10k list
                "30k": [...],       # Words from the 30k list
                "wiki": [...],      # Words from the Wikipedia list
                "full": [...]       # Words from the full list
            }
        }
        400 Bad Request:
        {
            "error": "Invalid input"
        }
    """
    data = request.json

    if not data or 'center_letter' not in data or 'other_letters' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    center_letter = data['center_letter'].lower()
    other_letters = data['other_letters'].lower()
    result = solver(center_letter, other_letters)
    return jsonify(result)


def load_words(filename, center_letter, other_letters):
    center_letter = center_letter.lower()
    other_letters = other_letters.lower()

    all_letters = center_letter + other_letters

    with open(filename) as word_file:
        words = set(word.strip().lower() for word in word_file)
    
    words = [word for word in words if center_letter in word]
    words = [word for word in words if all(letter in all_letters for letter in word) and len(word) >= 4]

    return set(words)


def solver(center_letter, other_letters):
    words_10k = load_words('word_list_10k.txt', center_letter, other_letters)
    words_30k = load_words('word_list_30k.txt', center_letter, other_letters) - words_10k
    words_wiki = load_words('word_list_wiki.txt', center_letter, other_letters) - words_10k - words_30k
    words_full = load_words('word_list_full.txt', center_letter, other_letters) - words_10k - words_30k - words_wiki

    return {'result': {'10k': list(words_10k), '30k': list(words_30k), 'wiki' : list(words_wiki), 'full': list(words_full)}}

if __name__ == '__main__':
    print(solver('l', 'orcyph'))
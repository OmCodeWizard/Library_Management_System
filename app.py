from flask import Flask, jsonify, request
from models import InMemoryDatabase, Book

from utils import paginate_items, validate_request

app = Flask(__name__)
db = InMemoryDatabase()  # Use the InMemoryDatabase class to manage books and members.


books = []
members = []
auth_tokens = {}

def generate_token(user_id):
    return f"token-{user_id}"

def authenticate(token):
    return token in auth_tokens.values()

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Welcome to the Library Management API!",
        "routes": [
            {"endpoint": "/books", "methods": ["GET", "POST"]},
            {"endpoint": "/books/<int:book_id>", "methods": ["GET", "PUT", "DELETE"]},
            {"endpoint": "/members", "methods": ["GET", "POST"]},
            {"endpoint": "/members/<int:member_id>", "methods": ["GET", "PUT", "DELETE"]},
            {"endpoint": "/auth/login", "methods": ["POST"]},
            {"endpoint": "/auth/validate", "methods": ["GET"]}
        ]
    })

@app.route('/books', methods=['GET'])
def get_books():
    query_title = request.args.get('title', '').lower()
    query_author = request.args.get('author', '').lower()
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 5))

    # Filter books by title and author if search parameters are provided
    filtered_books = [book.to_dict() for book in db.get_books()]
    if query_title:
        filtered_books = [b for b in filtered_books if query_title in b['title'].lower()]
    if query_author:
        filtered_books = [b for b in filtered_books if query_author in b['author'].lower()]

    # Paginate the results
    paginated_books = paginate_items(filtered_books, page, limit)
    return jsonify(paginated_books), 200

@app.route('/books', methods=['POST'])
def add_book():
    required_fields = ['title', 'author', 'published_year']
    is_valid, error = validate_request(request.json, required_fields)
    if not is_valid:
        return jsonify({'error': error}), 400

    data = request.json
    new_book = Book(
        book_id=len(db.books) + 1,  # Auto-increment ID
        title=data['title'],
        author=data['author'],
        published_year=data['published_year']
    )
    db.add_book(new_book)
    return jsonify(new_book.to_dict()), 201

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = db.find_book_by_id(book_id)
    if book:
        return jsonify(book.to_dict()), 200
    return jsonify({'error': 'Book not found'}), 404

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.json
    book = db.find_book_by_id(book_id)
    if book:
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.published_year = data.get('published_year', book.published_year)
        return jsonify(book.to_dict()), 200
    return jsonify({'error': 'Book not found'}), 404

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = db.find_book_by_id(book_id)
    if book:
        db.delete_book(book_id)
        return jsonify({'message': 'Book deleted'}), 200
    return jsonify({'error': 'Book not found'}), 404

@app.route('/members', methods=['GET'])
def get_members():
    return jsonify(members)

@app.route('/members', methods=['POST'])
def add_member():
    data = request.json
    data['id'] = len(members) + 1
    members.append(data)
    return jsonify(data), 201

@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = next((m for m in members if m['id'] == member_id), None)
    if not member:
        return jsonify({'error': 'Member not found'}), 404
    return jsonify(member)

@app.route('/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    member = next((m for m in members if m['id'] == member_id), None)
    if not member:
        return jsonify({'error': 'Member not found'}), 404
    data = request.json
    member.update(data)
    return jsonify(member)

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    global members
    members = [m for m in members if m['id'] != member_id]
    return jsonify({'message': 'Member deleted'})

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    user_id = data.get('user_id')
    token = generate_token(user_id)
    auth_tokens[user_id] = token
    return jsonify({'token': token})

@app.route('/auth/validate', methods=['GET'])
def validate_token():
    token = request.headers.get('Authorization')
    if not authenticate(token):
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify({'message': 'Authorized'})

if __name__ == '__main__':
    app.run(debug=True)

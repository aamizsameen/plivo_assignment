from flask import Flask, jsonify, request, current_app
from flask_sqlalchemy import SQLAlchemy
import logging, os, sys
import uuid # Universally Unique Identifiers


app = Flask(__name__)


# Configure logging
logging.basicConfig(filename='/var/log/app.log', level=logging.DEBUG)

# Configure the MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWORD']}@{os.environ['MYSQL_HOST']}:{os.environ['MYSQL_PORT']}/{os.environ['MYSQL_DATABASE']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

# Define the Message model
class Message(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id = db.Column(db.String(255), nullable=False)
    sender_number = db.Column(db.String(20), nullable=False)
    receiver_number = db.Column(db.String(20), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()


# Endpoint to get messages for a given account_id
@app.route('/get/messages/<account_id>', methods=['GET'])
def get_messages(account_id):
    with current_app.app_context():
        result = Message.query.filter_by(account_id=account_id).all()
        messages_list = [{'message_id': msg.id, 'account_id': msg.account_id, 'sender_number': msg.sender_number,
                          'receiver_number': msg.receiver_number} for msg in result]
    return jsonify(messages_list)



# Endpoint to create a new message
@app.route('/create', methods=['POST'])
def create_message():
    with current_app.app_context():
        data = request.get_json()
        account_id = data.get('account_id')
        sender_number = data.get('sender_number')
        receiver_number = data.get('receiver_number')

        if not account_id or not sender_number or not receiver_number:
            return jsonify({'error': 'Missing required fields'}), 400

        new_message = Message(account_id=account_id, sender_number=sender_number, receiver_number=receiver_number)
        db.session.add(new_message)
        db.session.commit()

        # Fetch the attributes before the session is closed
        message_id = new_message.id
        account_id = new_message.account_id
        sender_number = new_message.sender_number
        receiver_number = new_message.receiver_number

    return jsonify({'message_id': message_id, 'account_id': account_id,
                    'sender_number': sender_number, 'receiver_number': receiver_number})



# Endpoint for searching messages based on the filters
@app.route('/search', methods=['GET'])
def search_messages():
    query_params = request.args

    if 'message_id' in query_params:
        message_ids = query_params.get('message_id').split(',')
        with current_app.app_context():
            result = Message.query.filter(Message.id.in_(message_ids)).all()

    elif 'account_id' in query_params:
        account_ids = query_params.get('account_id').split(',')
        with current_app.app_context():
            result = Message.query.filter(Message.account_id.in_(account_ids)).all()

    elif 'sender_number' in query_params:
        sender_numbers = query_params.get('sender_number').split(',')
        with current_app.app_context():
            result = Message.query.filter(Message.sender_number.in_(sender_numbers)).all()

    elif 'receiver_number' in query_params:
        receiver_numbers = query_params.get('receiver_number').split(',')
        with current_app.app_context():
            result = Message.query.filter(Message.receiver_number.in_(receiver_numbers)).all()

    else:
        return jsonify({'error': 'Invalid search parameters'}), 400

    messages_list = [{'message_id': msg.id, 'account_id': msg.account_id, 'sender_number': msg.sender_number,
                      'receiver_number': msg.receiver_number} for msg in result]

    return jsonify(messages_list)


# Error handler for 404 Not Found
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not Found'}), 404


# Error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

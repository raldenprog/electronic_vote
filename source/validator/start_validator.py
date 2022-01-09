from base64 import b64decode, b64encode
from flask import Flask
from flask import request, jsonify
from validator.config_validator import Config
from Crypto.PublicKey import RSA
from validator.helper import insert_message, update_private, check_sign, sign, decrypt_messages, get_keys
import requests

app = Flask(__name__)
app.config.from_object(Config)

PRIVATE_KEY = RSA.generate(2048)
PUBLIC_KEY = PRIVATE_KEY.publickey()


@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    sign_user = b64decode(data.get('sign').encode())
    sign_registrator = b64decode(data.get('sign_registrator').encode())
    message_user = b64decode(data.get('encrypted_message').encode())
    id_user = data.get('id')
    public_key_user_r = requests.get(f'http://0.0.0.0:13451/public/{id_user}')
    public_key_user = public_key_user_r.content.decode()
    public_key_registrator_r = requests.get(f'http://0.0.0.0:13451/public')
    public_key_registrator = public_key_registrator_r.content.decode()

    checked_user_sign = check_sign(message_user, RSA.importKey(public_key_user), sign_user)
    checked_registrator_sign = check_sign(message_user, RSA.importKey(public_key_registrator), sign_registrator)

    if checked_user_sign and checked_registrator_sign:
        message_user_str = data.get('encrypted_message')
        insert_message(id_user, message_user_str)
        sign_validator = sign(message_user, PRIVATE_KEY)
        return jsonify({
            'sign': b64encode(sign_validator).decode()
        })

    else:
        raise Exception('Подписи не верны!')


@app.route('/accept', methods=['POST'])
def accept():
    data = request.json
    id_user = data.get('id')
    private = data.get('private')
    update_private(id_user, private)
    return {}, 200


@app.route('/get_results', methods=['POST'])
def get_results():
    results = decrypt_messages()
    return jsonify(results), 200


@app.route('/get_keys_for_replicas', methods=['POST'])
def get_keys_for_replicas():
    results = get_keys()
    return jsonify(results), 200


if __name__ == "__main__":
    app.run(host=app.config.get('HOST'), port=app.config.get('PORT'))

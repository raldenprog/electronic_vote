from datetime import datetime
from base64 import b64decode, b64encode
from flask import Flask
from flask import request, jsonify
from registrator.config import Config
from Crypto.PublicKey import RSA
from registrator.helper import auth, save_public_key_user, public_key_by_id

from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256



app = Flask(__name__)
app.config.from_object(Config)

PRIVATE_KEY = RSA.generate(2048)
PUBLIC_KEY = PRIVATE_KEY.publickey()


def sign(encrypted_2_message, private):
    hash_encrypted_2_message = SHA256.new(encrypted_2_message)

    signature = pkcs1_15.new(private).sign(hash_encrypted_2_message)
    return signature


def check_sign(encrypted_2_message, public_key, sign):
    """Проверка подписи от пользоваетеля регистратором"""
    hash_encrypted_message = SHA256.new(encrypted_2_message)
    try:
        pkcs1_15.new(public_key).verify(hash_encrypted_message, sign)
    except:
        return False
    return True


@app.route('/public/<int:id_user>')
def get_public_by_id(id_user):
    return public_key_by_id(id_user)[0]


@app.route('/public')
def get_public():
    return PUBLIC_KEY.export_key()


@app.route('/auth', methods=['POST'])
def auth_route():
    data = request.json
    result = auth(data.get('username'), data.get('password'))
    if result:
        save_public_key_user(result.get('id'), data.get('public_key'))
        return jsonify(dict(result)), 200
    else:
        return {'error_message': 'Неверный логин или пароль'}, 401


@app.route('/status')
def status():
    return jsonify({
        'start': Config.START_VOTING.strftime('%d.%m.%y %H:%M:%S'),
        'accepting': Config.START_ACCEPTING_VOTE.strftime('%d.%m.%y %H:%M:%S'),
        'stop_voting': Config.STOP_VOTING.strftime('%d.%m.%y %H:%M:%S'),
    }), 200


@app.route('/vote', methods=['POST'])
def vote():

    date_time_now = datetime.now()

    if Config.START_VOTING > date_time_now:
        return {'error_message': 'Голосование еще не начато'}, 200
    elif Config.START_ACCEPTING_VOTE > date_time_now > Config.START_VOTING:
        data = request.json
        sign_user = b64decode(data.get('sign').encode())
        message_user = b64decode(data.get('encrypted_message').encode())
        public_key_user = public_key_by_id(data.get('id'))

        if public_key_user:
            checked = check_sign(message_user, RSA.importKey(public_key_user[0]), sign_user)
        else:
            return {'error_message': 'Участник не подтвердил возможность голосовать'}, 403

        if checked:
            sign_registrator = sign(message_user, PRIVATE_KEY)
            return jsonify({
                'sign': b64encode(sign_registrator).decode()
            }), 200
        else:
            return {'error_message': 'Бюллетень не подписан участником'}, 403

    elif Config.STOP_VOTING > date_time_now > Config.START_ACCEPTING_VOTE:
        return {'error_message': 'Голосование завершено, идет подтверждение голосов'}, 403
    elif date_time_now > Config.STOP_VOTING:
        return {'error_message': 'Голосование завершено'}, 200
    else:
        return {'error_message': 'Внутренняя ошибка сервера'}, 500


if __name__ == "__main__":
    app.run(host=app.config.get('HOST'), port=app.config.get('PORT'))

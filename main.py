from flask import Flask, make_response, jsonify
from data import db_session, promotion_api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    db_session.global_init("db/database.db")
    app.register_blueprint(promotion_api.blueprint)
    app.run(host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()

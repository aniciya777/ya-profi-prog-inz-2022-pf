import flask
from flask import jsonify, request, make_response

from . import db_session
from .promotion import Promotions

blueprint = flask.Blueprint(
    'promotion_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/promo', methods=['GET'])
def get_promo():
    db_sess = db_session.create_session()
    news = db_sess.query(Promotions).all()
    return jsonify(
        {
            'news':
                [item.to_dict(only=('id', 'name', 'description'))
                 for item in news]
        }
    )


@blueprint.route('/promo', methods=['POST'])
def create_promo():
    try:
        if not request.json:
            return make_response(jsonify({'error': 'Empty request'}), 400)
        elif not all(key in request.json for key in ['name']):
            return make_response(jsonify({'error': 'Bad request'}), 400)
        db_sess = db_session.create_session()
        prom = Promotions(
            name=request.json.get('name'),
            description=request.json.get('description')
        )
        db_sess.add(prom)
        db_sess.commit()
        return jsonify({'success': 'OK', 'id': prom.id})
    except BaseException as e:
        print(e)
        return make_response(jsonify({'error': 'Bad request'}), 400)


@blueprint.route('/promo/<int:promo_id>', methods=['GET'])
def get_one_promo(promo_id):
    db_sess = db_session.create_session()
    promo = db_sess.query(Promotions).get(promo_id)
    if not promo:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'news': promo.to_dict(only=(
                'id', 'name', 'description', 'prizes.id', 'prizes.description',
                'participants.id', 'participants.name'))
        }
    )


@blueprint.route('/promo/<int:promo_id>', methods=['PUT'])
def put_promo(promo_id):
    try:
        if not request.json:
            return make_response(jsonify({'error': 'Empty request'}), 400)
        db_sess = db_session.create_session()
        promo = db_sess.query(Promotions).get(promo_id)
        if not promo:
            return make_response(jsonify({'error': 'Not found'}), 404)
        if request.json.get('name'):
            promo.name = request.json.get('name')
        if 'description' in request.json:
            promo.description = request.json.get('description')
        db_sess.commit()
        return jsonify({'success': 'OK'})
    except BaseException as e:
        print(e)
        return make_response(jsonify({'error': 'Bad request'}), 400)


@blueprint.route('/promo/<int:promo_id>', methods=['DELETE'])
def delete_promo(promo_id):
    db_sess = db_session.create_session()
    promo = db_sess.query(Promotions).get(promo_id)
    if not promo:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(promo)
    db_sess.commit()
    return jsonify({'success': 'OK'})
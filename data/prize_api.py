import flask
from flask import jsonify, request, make_response

from . import db_session
from .promotion import Promotions
from .prize import Prizes

blueprint = flask.Blueprint(
    'prize_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/promo/<int:promo_id>/prize', methods=['POST'])
def create_prize(promo_id):
    try:
        if not request.json:
            return make_response(jsonify({'error': 'Empty request'}), 400)
        elif not all(key in request.json for key in ['description']):
            return make_response(jsonify({'error': 'Bad request'}), 400)
        db_sess = db_session.create_session()
        promo = db_sess.query(Promotions).get(promo_id)
        if not promo:
            return make_response(jsonify({'error': 'Not found'}), 404)
        prize = Prizes(
            description=request.json.get('description'),
            promotion=promo
        )
        db_sess.add(prize)
        db_sess.commit()
        return jsonify({'success': 'OK', 'id': prize.id})
    except BaseException as e:
        print(e)
        return make_response(jsonify({'error': 'Bad request'}), 400)


@blueprint.route('/promo/<int:promo_id>/prize/<int:prize_id>', methods=['DELETE'])
def delete_participant(promo_id, prize_id):
    db_sess = db_session.create_session()
    promo = db_sess.query(Promotions).get(promo_id)
    if not promo:
        return make_response(jsonify({'error': 'Not found'}), 404)
    prize = db_sess.query(Prizes).get(prize_id)
    if not prize or prize.promotion != promo:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(prize)
    db_sess.commit()
    return jsonify({'success': 'OK'})

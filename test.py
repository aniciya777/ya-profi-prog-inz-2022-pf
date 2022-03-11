import pytest
import requests
import os
from pprint import pprint

URL = 'http://127.0.0.1:8080/'
promo_ids = []
part_ids = []


def test_empty_promo():
    result = {
        "news": []
    }
    resp = requests.get(URL + '/promo')
    assert resp.status_code == 200 and resp.json() == result


def test_empty_new_promo():
    result = {'error': 'Empty request'}
    resp = requests.post(URL + '/promo')
    assert resp.status_code == 400 and resp.json() == result


def test_bad_new_promo():
    result = {'error': 'Empty request'}
    resp = requests.post(URL + '/promo', json={
    })
    assert resp.status_code == 400 and resp.json() == result


def test_new_promo():
    resp = requests.post(URL + '/promo', json={
        "name": "ЯПрофи",
        "description": "Я Профессионал"
    })
    assert resp.status_code == 200 and resp.json()['success'] == 'OK'
    promo_ids.append(resp.json()['id'])


def test_new_half_promo():
    resp = requests.post(URL + '/promo', json={
        "name": "ЯПрофи 2",
    })
    assert resp.status_code == 200 and resp.json()['success'] == 'OK'
    promo_ids.append(resp.json()['id'])


def test_put_promo():
    result = {'success': 'OK'}
    resp = requests.put(URL + f'/promo/{promo_ids[1]}', json={
        "name": "ЯПрофи new",
    })
    assert resp.status_code == 200 and resp.json() == result


def test_post_part():
    result = {'success': 'OK'}
    resp = requests.post(URL + f'/promo/{promo_ids[0]}/participant', json={
        "name": "Остапчук",
    })
    assert resp.status_code == 200 and resp.json()['success'] == 'OK'
    part_ids.append(resp.json()['id'])

def test_promo_1_list():
    resp = requests.get(URL + f'/promo/{promo_ids[0]}')
    assert resp.status_code == 200
    pprint(resp.json(), indent=4)

def test_del_part():
    result = {'success': 'OK'}
    resp = requests.delete(URL + f'/promo/{promo_ids[0]}/participant/{part_ids[0]}')
    assert resp.status_code == 200 and resp.json() == result


def test_del_1_promo():
    result = {'success': 'OK'}
    resp = requests.delete(URL + f'/promo/{promo_ids[0]}')
    assert resp.status_code == 200 and resp.json() == result


def test_del_2_promo():
    result = {'success': 'OK'}
    resp = requests.delete(URL + f'/promo/{promo_ids[1]}')
    assert resp.status_code == 200 and resp.json() == result


def test_del_2_dubl_promo():
    result = {'error': 'Not found'}
    resp = requests.delete(URL + f'/promo/{promo_ids[1]}')
    assert resp.status_code == 404 and resp.json() == result


from flask import Blueprint, jsonify, redirect, request
from flask_login import login_required, current_user
from models import Link
from app import db
from auth import token_required

shortner = Blueprint('shortner', __name__)

@shortner.route('/<short_url>')
def redirect_to_original_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first_or_404()
    return redirect(link.original_url) 

@shortner.route('/create_link', methods=['POST'])
@token_required
def create_link(current_user):
    if not current_user:
        return jsonify({'message' : 'Autentication failed. Cannot perform that function!'})

    data = request.get_json()
    original_url = data['original_url']
    link = Link(original_url=original_url)
    db.session.add(link)
    db.session.commit()

    return jsonify({'message' : "Created the new link successfully"})

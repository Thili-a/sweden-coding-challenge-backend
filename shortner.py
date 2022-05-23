from flask import Blueprint, jsonify, redirect, request
from models import Link
from app import db
from auth import token_required

shortner = Blueprint('shortner', __name__)

@shortner.route('/create_link', methods=['POST'])
@token_required
def create_link(current_user):
    if not current_user:
        return jsonify({'message' : 'Authentication failed. Cannot perform that function!'}), 401

    data = request.get_json()
    if not data:
        return jsonify({'message' : 'Link not found!Check your Inputs!'}), 400

    original_url = data['original_url']
    link = Link(original_url=original_url) 
    db.session.add(link)
    db.session.commit()

    return jsonify({'message' : "New link created successfully!"}), 201

@shortner.route('/delete_link/<short_url>', methods=['DELETE'])
@token_required
def delete_user(current_user, short_url):
    if not current_user:
        return jsonify({'message' : 'Authentication failed. Cannot perform that function!'}), 401

    link = Link.query.filter_by(short_url=short_url).first()
    if not link:
        return jsonify({'message' : 'Link not found!Check your Inputs!'}), 400

    db.session.delete(link)
    db.session.commit()

    return jsonify({'message' : 'The link has been deleted!'}), 200

@shortner.route('/<short_url>')
def redirect_to_original_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first_or_404()
    return redirect(link.original_url) 
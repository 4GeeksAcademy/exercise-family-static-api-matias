"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# John Jackson
# 33 Years old
# Lucky Numbers: 7, 13, 22

# Jane Jackson
# 35 Years old
# Lucky Numbers: 10, 14, 3

# Jimmy Jackson
# 5 Years old
# Lucky Numbers: 1
member_John = {"id":None,"first_name":"John", "age":33, "lucky_numbers":[7, 13, 22]}
member_Jane = {"id":None,"first_name":"Jane", "age":35, "lucky_numbers":[10, 14, 3]}
member_Jimmy = {"id":None,"first_name":"Jimmy", "age":5, "lucky_numbers":[1]}

jackson_family.add_member(member_John)
jackson_family.add_member(member_Jane)
jackson_family.add_member(member_Jimmy)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# GET /members
# status_code: 200 if success. 400 if bad request (wrong info) screw up, 500 if the server encounter an error
# RESPONSE BODY (content-type: application/json):
# [], // List of members.
@app.route('/members', methods=['GET'])
def get_members():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = members

    return jsonify(response_body), 200


# GET /member/<int:member_id>
# RESPONSE (content_type: application/json):
# status_code: 200 if success. 400 if bad request (wrong info) screw up, 500 if the server encounter an error
# body: //the member's json object
# {
#     "id": Int,
#     "first_name": String,
#     "age": Int,
#     "lucky_numbers": List
# }
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):

    member = jackson_family.get_member(member_id)
    response_body = member

    return jsonify(response_body), 200


# POST /member
# REQUEST BODY (content_type: application/json):
# {
#     first_name: String,
#     age: Int,
#     lucky_numbers: [],
#     id: Int *optional
# }
# RESPONSE (content_type: application/json):
# status_code: 200 if success. 400 if a bad request (wrong info) screw up, 500 if the server encounters an error
# body: empty
@app.route('/member', methods=['POST'])
def add_member():

    if not request.get_json()['id']:
        id = None
    else:
        id = request.get_json()['id']
    
    # first_name
    first_name =  request.get_json()['first_name']
    if not first_name:
        return jsonify({"error": "First name is required"}), 400
    
    # age
    age =  request.get_json()['age']
    if not age:
        return jsonify({"error": "Age is required"}), 400
    
    # lucky_numbers
    lucky_numbers= request.get_json()['lucky_numbers']
    if not lucky_numbers:
        return jsonify({"error": "Lucky_numbers are required"}), 400
    
    member = {"id":id,"first_name":first_name, "age":age, "lucky_numbers":lucky_numbers}
    jackson_family.add_member(member)

    response_body = {
        "member": member,
        "msg": f"New member added to {jackson_family.last_name}",
    }

    return jsonify(response_body), 200




@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):

    delete_member = jackson_family.delete_member(member_id)

    if not delete_member:
        return jsonify({"error": "Member not found"}), 400

    response_body = delete_member

    return jsonify(response_body), 200








# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

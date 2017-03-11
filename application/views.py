from flask import Flask, request, g
from flask_restful import Resource, marshal
from application.validate import Validation
from application.serializer import bucket_list_serializer
from flask_httpauth import HTTPTokenAuth

from .models import UserModel, BucketListModel, ItemsModel, db

valid = Validation() # valid is an instance of Validation class that validates json input for the API

auth = HTTPTokenAuth(scheme='Token') # creates an instance of HTTPTokenAuth

@auth.verify_token
def verify_token(token):
	"""Validates the token sent by the user """
	user = UserModel.verify_auth_token(token)
	if not user:
		return False
	g.user = user
	return True

class UserRegistration(Resource):
	""" This class handles new user registration"""
	def post(self):
		try:
			credentials = request.json
			if credentials:
				response = valid.validate_register_user(credentials)
				return response
		except Exception as e:
			return({'message': 'bad request'}, 400)

	def get(self):
		'''Ensures that get method is not allowed for registration'''
		return({'message': 'Method is not allowed'}, 405)

class CreateBucketList(Resource):
	""" This class handles the creation of a new create bucket list """
	@auth.login_required
	def post(self):
		try:
			bucket_list = request.json
			if bucket_list:
				response = valid.validate_create_bucket_list(bucket_list)
				return response
		except Exception as e:
			return({'message': 'bad request'}, 400)

class GetBucketLists(Resource):
	""" This class handles the retrieval of all created bucket list """
	@auth.login_required
	def get(self):
		q = request.args.get('q') # the search parameter
		page = request.args.get('page') # the current page for pagination
		limit = request.args.get('limit') # the limit numer of items for each page
		if q:
			bucket_lists = BucketListModel.query.filter(BucketListModel.name.ilike('%' + q + "%" )).filter_by(created_by=g.user.email).paginate(int(page), int(limit), False)
			buckets = bucket_lists.items
		else:
			bucket_lists = BucketListModel.query.filter_by(created_by = g.user.email).paginate(int(page), int(limit), False)
			buckets = bucket_lists.items

		if buckets:
			 if bucket_lists.has_next:
			 	next_page = str(request.url_root) + 'v1/bucketlists?q=' + q + '&page=' + str(int(page) + 1)
			 else:
				 next_page = 'None'

			 if bucket_lists.has_prev:
					prev = str(request.url_root) + 'v1/bucketlists?q=' + \
					q + '&page=' + str(int(page) - 1)
			 else:
					prev = 'None'
			 bkts = [bucket for bucket in buckets]
			 return({'bucketlists': marshal(bkts, bucket_list_serializer), 'next': next_page,
					'prev': prev},200)
		else:
			return([],404)
			

class GetBucketList(Resource):
	""" This class handles the retrival of a single bucket list"""
	@auth.login_required
	def get(self,id):
		try:
			bucket_list = BucketListModel.query.filter_by(created_by=g.user.email, id=id).first()
			if bucket_list:
				return({'bucketlist': marshal(bucket_list, bucket_list_serializer)},200)
			else:
				return({'message': 'not found'}, 404)
		except Exception as e:
			return({'message': 'bad request'}, 404)

class DeleteBucketList(Resource):
	""" This class handles the deletion of a single bucket list"""
	@auth.login_required
	def delete(self,id):
		try:
			bucket_list = BucketListModel.query.filter_by(created_by=g.user.email,id=id).first()
			if bucket_list:
				db.session.delete(bucket_list)
				db.session.commit()
				return({'message': 'ok'},200)
			else:
				return({'message': 'not found'}, 404)
		except Exception as e:
			return({'message': 'bad request'}, 400)

class UpdateBucketList(Resource):
	""" This class handles an update for a single bucket list"""
	@auth.login_required
	def put(self, id):
		try:
			bucket_list = BucketListModel.query.filter_by(created_by=g.user.email, id=id).first()
			if bucket_list:
				bucket_list_update = request.json
				if bucket_list_update:
					if bucket_list_update['name'] != "":
						if BucketListModel.query.filter_by(name = bucket_list_update['name']).first() is not None:
							return ({'message': 'the bucketlist item already exists'},409)
						else:
							bucket_list.name = bucket_list_update['name']
							db.session.commit()
						return({'message': 'ok'},200)
					else:
						return({'message': 'bad request'}, 400)
				else:
					return({'message': 'bad request'}, 400)
			else:
				return({'message': 'not found'}, 404)
		except Exception as e:
			print(str(e))
			return({'message': 'bad request'}, 400)

class CreateBucketListItems(Resource):
	""" This class creates items for a particular bucket list"""
	@auth.login_required
	def post(self, id):
		try:
			if BucketListModel.query.filter_by(id = id, created_by = g.user.email).first() is None:
				return ({'message': 'the bucketlist item does not exist'}, 404)
			else:
				bucket_list_items = request.json
				if bucket_list_items:
					response = valid.validate_create_bucket_list_items(bucket_list_items, id)
					return response
		except Exception as e:
			print(str(e))
			return({'message': 'bad request'}, 400)

class UpdateBucketListItem(Resource):
    """ This class updates items for a particular bucket list """
	@auth.login_required
	def put(self, id, item_id):
		try:
			if BucketListModel.query.filter_by(id = id, created_by = g.user.email).first() is None:
				return ({'message': 'the bucketlist item does not exist'}, 404)
			else:
				item = ItemsModel.query.filter_by(id = item_id ).first()
				if item:
					bucket_list_item = request.json
					if bucket_list_item["name"] == "" or bucket_list_item["done"] == "":
						return({'message': 'bad request'},400)
					else:
						item.name = bucket_list_item["name"]
						item.done = bucket_list_item["done"]
						db.session.commit()
						return({'message': 'ok'},200)
				else:
					return ({'message': 'the bucketlist item does not exist'}, 404)
		except Exception as e:
			print(str(e))
			return({'message': 'bad request'}, 400)

class DeleteBucketListItem(Resource):
	"""This class deletes an item for a particular bucket list"""
	@auth.login_required
	def delete(self, id, item_id):
		try:
			if BucketListModel.query.filter_by(id = id, created_by = g.user.email).first() is None:
				return ({'message': 'the bucketlist item does not exist'}, 404)
			else:
				item = ItemsModel.query.filter_by(id = item_id ).first()
				if item:
					db.session.delete(item)
					db.session.commit()
					return({'message': 'ok'},200)
				else:
					return ({'message': 'the bucketlist item does not exist'}, 404)
		except Exception as e:
			print(str(e))
			return({'message': 'bad request'}, 400)
			
class UserLogin(Resource):
	"""This class is authenticates the user and generates the token"""
	def post(self):
		try:
			credentials = request.json
			if credentials:
				response = valid.validate_login_credentials(credentials)
				return response
		except Exception as e:
			return({'message': 'bad request'}, 400)
	


	   
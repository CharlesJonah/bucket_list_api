'''
This module maps the data that will be used by the marshall when returning the
data to the user from the database
'''

from flask_restful import fields

bucket_list_item_serializer = {
    'item_id': fields.Integer,
    'name': fields.String,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'done': fields.Boolean
}

bucket_list_serializer = {
    'id': fields.Integer,
    'name': fields.String,
    'items':fields.Nested(bucket_list_item_serializer),
    'created_by': fields.String,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime
}
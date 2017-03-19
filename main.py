from flask_restful import Api
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from application.models import db
from application import models
from application.views import UserRegistration, GetBucketLists, DeleteBucketList,\
                              DeleteBucketListItem, CreateBucketListItems, GetBucketList,UpdateBucketList,\
                              UpdateBucketListItem, UserLogin, CreateBucketList
from application.config import Config


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
api = Api(app)
db.app = app
db.init_app(app)
db.create_all()


api.add_resource(UserRegistration, '/v1/auth/register', endpoint="user_registration")
api.add_resource(GetBucketLists, '/v1/bucketlists', endpoint="get_bucket_lists")
api.add_resource(CreateBucketListItems, '/v1/bucketlists/<int:id>/items', endpoint="create_bucket_list_items")
api.add_resource(UpdateBucketListItem, '/v1/bucketlists/<int:id>/items/<int:item_id>', endpoint="update_bucket_list_item")
api.add_resource(DeleteBucketListItem, '/v1/bucketlists/<int:id>/items/<int:item_id>', endpoint="delete_bucket_list_item")
api.add_resource(CreateBucketList, '/v1/bucketlists', endpoint="create_bucket_list")
api.add_resource(GetBucketList, '/v1/bucketlists/<int:id>', endpoint="get_bucket_list")
api.add_resource(UpdateBucketList, '/v1/bucketlists/<int:id>', endpoint="update_bucket_list")
api.add_resource(DeleteBucketList, '/v1/bucketlists/<int:id>', endpoint="delete_bucket_list")
api.add_resource(UserLogin, '/v1/auth/login', endpoint="login")

@app.route("/")
def main():
	return render_template('index.html')

if __name__ == '__main__':
   app.run(debug = True, host='127.0.0.1', port=5800)
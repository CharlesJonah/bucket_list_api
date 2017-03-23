from .models import ItemsModel, BucketListModel, UserModel, db
from flask import g

class Validation():
    """ This class validates iput given by the user as a json object"""
    
    def validate_register_user(self, credentials):
        """This method validates if the user has given all the registration details required 
           for registrationv in the correct format"""
        if credentials['email'] == '' or credentials['password'] == '':
            return({'message': 'Please provide email and the password.'}, 400)
        else:
            if len(credentials['password']) < 8:
                return({'message': 'password too short'}, 400)
            else:
                if UserModel.query.filter_by(email = credentials['email']).first() is not None:
                    return ({'message': 'user with that username already exists'},409)
                user = UserModel(email = credentials['email'], password = credentials['password'] )
                db.session.add(user)
                db.session.commit()
                return ({'message': 'user created'}, 201)
    
    def validate_create_bucket_list(self, bucket_list):
        """This method validates all details required for bucket list
            creation"""
        if bucket_list['name'] =='':
            return({'message': 'bucket list name is missing'}, 400) 
        else:
                if BucketListModel.query.filter_by(name = bucket_list['name']).first() is not None:
                    return ({'message': 'the bucketlist already exists'},409)
                bucket_list_data = BucketListModel(name = bucket_list['name'],created_by = g.user.email)
                db.session.add(bucket_list_data)
                db.session.commit()
                return ({'message': 'bucketlist created'}, 201)
        
    def validate_login_credentials(self, credentials):
        """ This method validates login details provided by the user"""
        if credentials['email'] == '' or credentials['password'] == '':
            return({'message': 'Please provide all credentials'}, 400)
        else:
            user = UserModel.query.filter_by(email = credentials['email']).first()
            if user and user.verify_password(credentials['password']):
                token = user.generate_auth_token()
                return ({'Authorization':'Token ' + token.decode('ascii')}, 200)

            else:
                return ({'message': 'invalid username or password'}, 401)
    
    def validate_create_bucket_list_items(self, bucket_list_items, id):
        """This method validates all details required for bucket list items
            creation"""

        if bucket_list_items['items'] == "":
            return({'message': 'bad request. no items to be added'}, 400)
        else:
            if type(bucket_list_items["items"] ) is not list:
                return({'message': 'bad request. items should be in a list format'}, 400)
            else:
                for item in bucket_list_items["items"]:
                    if item['name'] == '' or item['done'] == '':
                        return({'message': 'bad request.name is missing in your item'}, 400)
                    else:
                        item = ItemsModel(name = item["name"], done = item["done"], bucketlist_id = id)
                        db.session.add(item)
                        db.session.commit()           
                return ({'message': 'bucketlist items have added'}, 201)



import unittest
import json

from application import views
from application.config import Test
import main

class BaseTest(unittest.TestCase):
    """ This is the core class that holds all the basic setups required for the tests"""
    def setUp(self):
        """ This method creates all the initial setups required to run the tests """
        main.app.config['SQLALCHEMY_DATABASE_URI'] = Test.SQLALCHEMY_TEST_DATABASE_URI
        self.client = main.app.test_client()
        main.db.app = main.app
        main.db.init_app(main.app)
        main.db.create_all()
        registration_details = {"email":"mutua.charles48@gmail.com","password":"124245yytstts"}
        self.client.post("v1/auth/register",data = json.dumps(registration_details),
                                     content_type='application/json')  
        login_details = {"email":"mutua.charles48@gmail.com","password":"124245yytstts"}
        response =  self.client.post("v1/auth/login",data = json.dumps(login_details),
                                     content_type='application/json')  
        self.token = json.loads(response.get_data())['Authorization']
      
class TestUserRegistration(BaseTest):
    """ This class holds all the test cases for registration logic"""
    def test_user_registration_using_bad_request(self):
        registration_details = 0 
        
        response =  self.client.post("v1/auth/register",data = registration_details,
                                     content_type='application/json')                     
        self.assertEqual(response.status_code, 400)

    def test_user_can_register(self):
        registration_details = {"email":"mutua1.charles48@gmail.com","password":"124245yytstts"}
        
        response =  self.client.post("v1/auth/register",data = json.dumps(registration_details),
                                     content_type='application/json')                     
        self.assertEqual(response.status_code, 201)

    def test_user_can_regiter_with_missing_data(self):
        registration_details = {"email":"","password":"ssdffsfsfsffsfsffs"}
        response =  self.client.post("v1/auth/register",data = json.dumps(registration_details),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_user_can_register_with_weak_password(self):
        registration_details = {"email":"mutua2.charles48@gmail.com","password":"12"}
        response =  self.client.post("v1/auth/register",data = json.dumps(registration_details),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)

class TestCreateBucketList(BaseTest):
    """ This class holds all the test cases for creating a bucket list """
    def test_create_bucket_list_using_bad_request(self):
        bucket_list = 0 
        
        response =  self.client.post("v1/bucketlists",data = bucket_list,
                                     headers={'Content-Type':'application/json','Authorization': self.token})                     
        self.assertEqual(response.status_code, 400)
   
    def test_create_bucket_list(self):
        bucket_list = {"name": "BucketList1"}
        response =  self.client.post("v1/bucketlists",data = json.dumps(bucket_list),
                                     headers={'Content-Type':'application/json','Authorization': self.token})                     
        self.assertEqual(response.status_code, 201)

    def test_create_bucket_list_with_missing_data(self):
        bucket_list = {"name": ""}
        response =  self.client.post("v1/bucketlists",data = json.dumps(bucket_list),
                                     headers={'Content-Type':'application/json','Authorization': self.token})                     
        self.assertEqual(response.status_code, 400)

class TestUserLogin(BaseTest):
    """ This class holds all the test cases for login logic """
    def test_user_can_login(self):
        login_details = {"email":"mutua.charles48@gmail.com","password":"124245yytstts"}
        response =  self.client.post("v1/auth/login",data = json.dumps(login_details),
                                     content_type='application/json') 
        self.assertEqual(response.status_code, 200) 

    def test_user_cannot_login_with_wrong_credentials(self):
        login_details = {"email":"mutua.charles48@gmail.com","password":"125yytstts"}
        response =  self.client.post("v1/auth/login",data = json.dumps(login_details),
                                     content_type='application/json') 
        self.assertEqual(response.status_code, 401)
        
class TestGetBucketLists(BaseTest):
    """ This class holds the test cases for getting bucket lists"""
    def test_get_bucketlists(self):
        response =  self.client.get("v1/bucketlists?page=1&limit=1",
                                     headers={'Content-Type':'application/json','Authorization': self.token})                   
        self.assertEqual(response.status_code, 200)

class TestGetBucketList(BaseTest):
    """ This class holds the test cases for getting a single bucket list"""
    def test_get_bucketlist(self):
        response =  self.client.get("v1/bucketlists/1",
                                     headers={'Content-Type':'application/json','Authorization': self.token})                   
        self.assertEqual(response.status_code, 200)
    def test_get_non_existent_bucketlist(self):
        response =  self.client.get("v1/bucketlists/10",
                                     headers={'Content-Type':'application/json','Authorization': self.token})                   
        self.assertEqual(response.status_code, 404)

class TestUpdateBucketList(BaseTest):
    """ This class holds the test cases for updating a bucket list """
    def test_update_bucketlist(self):
        data = {"name":"Bucket"}
        response =  self.client.put("v1/bucketlists/1", data = json.dumps(data),
                                     headers={'Content-Type':'application/json','Authorization': self.token})                   
        self.assertEqual(response.status_code, 200)

    def test_update_bucketlist_without_update_data(self):
        data = {"name":""}
        response =  self.client.put("v1/bucketlists/1", data = json.dumps(data),
                                     headers={'Content-Type':'application/json','Authorization': self.token})                   
        self.assertEqual(response.status_code, 400)

    def test_update_non_existent_bucketlist(self):
        response =  self.client.put("v1/bucketlists/10",
                                     headers={'Content-Type':'application/json','Authorization': self.token})                   
        self.assertEqual(response.status_code, 404)

class TestCreateBucketListItems(BaseTest):
    """ This class holds the test cases for creating bucket list items """
    def test_create_bucket_list_items_without_a_bucket_list(self):
        items = {"items":[{"name":"item","done":"false"},{"name":"item1","done":"false"},{"name":"item2","done":"false"}]}
        response =  self.client.post("v1/bucketlists/10/items",data = json.dumps(items),
                                     headers={'Content-Type':'application/json','Authorization': self.token})                     
        self.assertEqual(response.status_code, 404)
   
    def test_create_bucket_list_items(self):
        items = {"items":[{"name":"item","done":"false"},{"name":"item1","done":"false"},{"name":"item2","done":"false"}]}
        response =  self.client.post("v1/bucketlists/1/items",data = json.dumps(items),
                                     headers={'Content-Type':'application/json','Authorization': self.token})                     
        self.assertEqual(response.status_code, 201)

    def test_create_bucket_list_items_with_missing_data(self):
        items = {"items": ""}
        response =  self.client.post("v1/bucketlists/1/items",data = json.dumps(items),
                                     headers={'Content-Type':'application/json','Authorization': self.token})                     
        self.assertEqual(response.status_code, 400)

class TestUpdateBucketListItems(BaseTest):
    """ This class holds the test cases for updating a bucket list item """
    def test_update_bucket_list_item_without_the_item(self):
        bucket_list_item_update = ""
        response =  self.client.put("v1/bucketlists/1/items/10",data = json.dumps(bucket_list_item_update),
                                     headers={'Content-Type':'application/json','Authorization': self.token})                     
        self.assertEqual(response.status_code, 404)
   
    def test_update_bucket_list_item(self):
        bucket_list_item_update = {"name":"Bucket","done":"True"}
        response =  self.client.put("v1/bucketlists/1/items/1",data = json.dumps(bucket_list_item_update),
                                     headers={'Content-Type':'application/json','Authorization': self.token})                     
        self.assertEqual(response.status_code, 200)

    def test_update_bucket_list_item_with_missing_data(self):
        bucket_list_item_update = {"name":"","done":""}
        response =  self.client.put("v1/bucketlists/1/items/1",data = json.dumps(bucket_list_item_update),
                                     headers={'Content-Type':'application/json','Authorization': self.token})                     
        self.assertEqual(response.status_code, 400)

class TestDeleteBucketList(BaseTest):
    """ This class holds the testcases for the logic behind the deletion of a bucket list """
    def test_delete_bucketlist(self):
        bucket_list = {"name": "BucketList2"}
        self.client.post("v1/bucketlists",data = json.dumps(bucket_list),
                                     headers={'Content-Type':'application/json','Authorization': self.token})   
        response =  self.client.delete("v1/bucketlists/2",
                                     headers={'Content-Type':'application/json','Authorization': self.token})                   
        self.assertEqual(response.status_code, 200)
    def test_delete_non_existent_bucketlist(self):
        response =  self.client.delete("v1/bucketlists/10",
                                     headers={'Content-Type':'application/json','Authorization': self.token})                   
        self.assertEqual(response.status_code, 404)


def tearDown(self):
    """ Thus function drops the tests databases after running all the tests """
    main.db.drop_all()
    

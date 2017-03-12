#BucketList API

## Introduction

> This application is a Flask API for a bucket list service that allows users to create, update and delete bucket lists and their items. It has been built with Flask Restful Framework. This API is a REST API and the return format for all endpoints is JSON.

## Endpoints

1. `POST /auth/login`
2. `POST /auth/register`
3. `GET /bucketlists/`: returns all bucket listing of all buckets list
4. `GET /bucketlists/<bucketlist_id>`: returns the bucket list with the specified ID
5. `PUT /bucketlist/<bucketlist_id>`: updates the bucket list with the specified with the provided data
6. `DELETE /bucketlist/<bucketlist_id>`: deletes the bucket list with the specified ID
7. `POST /bucketlists/<bucketlist_id>/items/`: adds a new item to the bucket list with the specified ID
8. `PUT /bucketlists/<bucketlist_id>/items/<item_id>`: updates the item with the given item ID from the bucket list with the provided ID
9. `DELETE /bucketlists/<bucketlist_id>/items/<item_id>`: deletes the item with the specified item ID from the bucket list with the provided ID

## Installation & Setup
1. Download & Install Python
 	* Head over to the [Python Downloads](https://www.python.org/downloads/) Site and download a version compatible with your operating system
 
2. Clone the repository to your personal computer to any folder
 	* Navigate to the directory of your choice
 	* On your right, click the green button 'Clone or download'
 	* Copy the URL
 	* Enter the terminal on Mac/Linux or Git Bash on Windows
 	* Type `git clone ` and paste the URL you copied from GitHub
 	* Press *Enter* to complete the cloning process
3. Virtual Environment Installation
 	* Install the virtual environment by typing: `pip install virtualenvwrapper` on your terminal
4. Create a virtual environment by running `mkvirtualenv bucket_list`. This will create the virtual environment in which you can run the project.
5. Activate the virtual environment by running `workon bucket_list`
6. Enter the project directory by running where you cloned the project
7. Once inside the directory install the required modules
 	* Run `pip install -r requirements.txt`
8. Inside the application folder run the main.py file:
 * On the terminal type `python main.py` to start the application

 ## Perform migrations
```
python server.py db init
python server.py db migrate
python server.py db upgrade

## Testing
To run the tests for the app, and see the coverage, run
```
nosetests --with-coverage
```

## Documentation & Usage
Click on [this link] (https://www.python.org/downloads/) to view see example on how to consume the API
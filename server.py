#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# You can start this by executing it in python:
# python server.py
#
# remember to:
#     pip install flask


import flask
from flask import Flask, request
import json
from flask import send_from_directory

app = Flask(__name__)
app.debug = True

# An example world
# {
#    'a':{'x':1, 'y':2},
#    'b':{'x':2, 'y':3}
# }

class World:
    def __init__(self):
        self.clear()
        
    def update(self, entity, key, value):
        entry = self.space.get(entity,dict())
        entry[key] = value
        self.space[entity] = entry

    def set(self, entity, data):
        self.space[entity] = data

    def clear(self):
        self.space = dict()

    def get(self, entity):
        return self.space.get(entity,dict())
    
    def world(self):
        return self.space

# you can test your webservice from the commandline
# curl -v   -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/entity/X -d '{"x":1,"y":1}' 

myWorld = World()          

# I give this to you, this is how you get the raw body/data portion of a post in flask
# this should come with flask but whatever, it's not my project.
def flask_post_json():
    '''Ah the joys of frameworks! They do so much work for you
       that they get in the way of sane operation!'''
    if (request.json != None):
        return request.json
    elif (request.data != None and request.data.decode("utf8") != u''):
        return json.loads(request.data.decode("utf8"))
    else:
        return json.loads(request.form.keys()[0])

@app.route("/")
@app.route("/static/index.html")
def hello():
    '''Return something coherent here.. perhaps redirect to /static/index.html '''
    return send_from_directory('', 'static/index.html')

@app.route("/json2.js")
def for_the_json():
    '''To get rid of the console erro'''
    return send_from_directory('', 'static/json2.js')

@app.route("/static/entity/<entity>", methods=['POST','PUT'])
@app.route("/entity/<entity>", methods=['POST','PUT'])
def update(entity):
    '''update the entities via this interface'''
    # I talked to Mashiad Hasan about this method
    if request.method == 'POST' or request.method == 'PUT':
        data = request.get_json()
        if entity:
            myWorld.set(entity, data)
            return data, 200
    else:
        return "This path is impossible", 404

@app.route("/world", methods=['POST','GET'])
def world():
    '''you should probably return the world here'''
    return myWorld.world(),200

@app.route("/entity/<entity>")
def get_entity(entity):
    '''This is the GET version of the entity interface, return a representation of the entity'''
    if not myWorld.get(entity):
        return {}, 200
    return myWorld.get(entity), 200

@app.route("/clear", methods=['POST','GET'])
def clear():
    '''Clear the world out!'''
    temp_world = myWorld.world()
    myWorld.clear()
    return temp_world

if __name__ == "__main__":
    app.run()

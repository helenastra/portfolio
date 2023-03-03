#!/bin/bash
curl --request GET http://127.0.0.1:5000/api/timeline_post
curl --request POST http://127.0.0.1:5000/api/timeline_post -d 'name=Helen&email=helen@gmail.com&content=just added db'
curl --request GET http://127.0.0.1:5000/api/timeline_post


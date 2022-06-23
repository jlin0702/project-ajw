#!/bin/bash
curl --request POST http://localhost:5000/api/timeline_post -d 'name=Jacky&email=lin.jacky@ku.edu&content=Just Added Database to my portfolio site!'
curl http://localhost:5000/api/timeline_post
curl --request DELETE http://localhost:5000/api/timeline_post -d 'id=1'

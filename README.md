neo4j-facebook-example
======================

Storing Facebook friends data into Neo4j with Python and visualizing them using a D3.js graph


### Description
This project is an example that shows how to connect to Neo4j from Python, fetch some data from Facebook (your friends) and display your friends' relationships in a graph.
This project uses the py2neo module to connect to the Neo4j RESTful interface, the facebook-sdk to fetch data from your Fracebook profile and D3.js (the 'chords' graph) to visualize the data.


### Requirements
- Python 2.7
- [Neo4j v2.0](http://www.neo4j.org)
- [pythonforfacebook/facebook-sdk](https://github.com/pythonforfacebook/facebook-sdk)
- Facebook Access Token (You will need to register as a Facebook Developer https://developers.facebook.com/apps)


### How To

```
git clone git@github.com:tiepologian/neo4j-facebook-example.git
cd neo4j-facebook-example

(edit neo4j-facebook.py and set YOUR_NAME and YOUR_FB_TOKEN to your full name on Facebook and your access token)
./neo4j-facebook.py

(If there are no errors, follows.json is created. Move it to the chords folder)
mv follows.json chords/

(Move the chords folder to your web server folder, I'm using Apache)
sudo mv chords/ /var/www/
```

You can view the chords graph from your browser:
http://YOUR_IP_ADDRESS/chords


This is what mine looks like:
![](http://i1033.photobucket.com/albums/a416/Gianluca_Tiepolo/1958464_10152361719482189_94706854_n_zps70f4422c.jpg)


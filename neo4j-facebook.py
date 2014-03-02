#!/usr/bin/python

from __future__ import division
from py2neo import neo4j, node, rel, cypher
from threading import Thread
from collections import OrderedDict
import facebook, sys, time, json

# Configuration
YOUR_NAME = "YOUR_NAME"
YOUR_FB_TOKEN = "YOUR_FACEBOOK_ACCESS_TOKEN"
# IMPORTANT: IF YOU'RE RUNNING ON AN EC2.MICRO, PLEASE SET LEVEL <= 20 AND MAX_FRIENDS <= 100
DEEP_LEVEL = 20
MAX_FRIENDS = 100

# a few global variables
graph_db = 0
me = 0
graph = 0
friends = 0
myfriends = {}
friendID = {}

def printHeader():
    print
    print "+-+-+-+-+-+-+-+-+ +-+-+-+-+-+\n|F|a|c|e|b|o|o|k| |G|r|a|p|h|\n+-+-+-+-+-+-+-+-+ +-+-+-+-+-+"
    print "Version: 3.0"
    print "Date: 01/03/2014"
    print "Author: Gianluca Tiepolo"
    print

def getFriends():
    print "Requesting friends from Facebook...",
    global graph
    graph = facebook.GraphAPI(YOUR_FB_TOKEN)
    global friends
    friends = graph.get_connections("me", "friends")
    print "Done"

def getGender(user):
    profile = graph.get_object(user)
    if 'gender' in profile:
        return profile['gender']
    else:
        return "no gender"

def createANode(nname, nid):
    # method executed by thread
    global myfriends
    global friendID
    mynode, rel = graph_db.create({"name": nname}, (me[0], "FRIEND", 0))
    if getGender(nid) == 'male':
        mynode.add_labels("male")
        mynode.update_properties({"gender":"male"})
    elif getGender(nid) == 'female':
        mynode.add_labels("female")
        mynode.update_properties({"gender":"female"})
    myfriends[nname] = mynode
    friendID[nname] = nid

def createFriendNodes():
    count = 0
    threadPool = []
    for val in friends['data']:
        nodeName = val['name']
        nodeID = val['id']
        t = Thread(target=createANode, args=(nodeName, nodeID))
        # add all threads to a list
        threadPool.append(t)
        t.start()
        count += 1
        if count >= MAX_FRIENDS:
            break;
    counter = 0
    for t in threadPool:
        # wait for all threads to finish
        t.join()
        counter += 1
        perc = (counter/len(threadPool))*100
        sys.stdout.write("\rCreating Friends nodes... %d%%" %perc)
        sys.stdout.flush()

def createRel(a, b):
    mutualRel = graph_db.create((a, "FRIEND", b))

def findMutualFriends(j, i, myfriends):
    # method executed by thread
    mutual = graph.get_connections(j, "mutualfriends")
    count3 = 0
    for k in mutual['data']:
        if k['name'] in myfriends:
	    createRel(myfriends[i], myfriends[k['name']])
            count3 += 1
            if count3 >= DEEP_LEVEL:
                break;

def createFriendRelations(myfriends, friendID):
    count2 = 0
    mythreads = []
    for i,j in friendID.iteritems():
        count2 += 1
        if count2 >= MAX_FRIENDS:
            break;
        t = Thread(target=findMutualFriends, args=(j, i, myfriends))
        mythreads.append(t)
        t.start()
    counter = 0
    for l in mythreads:
        # wait for all threads to finish
        l.join()
        counter += 1
        perc = (counter/len(mythreads))*100
        sys.stdout.write("\rCreating Relations... %d%%" %perc)
        sys.stdout.flush()

def saveJson():
    query = neo4j.CypherQuery(graph_db, "MATCH a-[:FRIEND]->b RETURN a.name, collect(b.name)")
    result = query.execute()
    data = []
    for i in result:
        dati = OrderedDict()
        dati["name"] = i[0]
        dati["follows"] = i[1]
        data.append(dati)
    with open('follows.json', 'w') as outfile:
        json.dump(data, outfile)
        
def main():
    printHeader()
    print "Connecting to Neo4j database...",
    global graph_db 
    graph_db= neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
    global me
    me = graph_db.create({"name": YOUR_NAME})
    me[0].add_labels("me")
    print "Done"
    getFriends()    
    print "Creating Friends nodes...",
    sys.stdout.flush()
    createFriendNodes()
    sys.stdout.write("\rCreating Friends nodes... Done\n")
    sys.stdout.flush()
    print "Creating Relations...",
    sys.stdout.flush()
    createFriendRelations(myfriends, friendID)
    sys.stdout.write("\rCreating Relations... Done\n")
    sys.stdout.flush()
    print "Saving file...",
    saveJson()
    print "Done"
    print
    print "Finished! - JSON saved as follows.json"


if __name__ == '__main__':
  main()


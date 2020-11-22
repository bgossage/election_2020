#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 18:17:26 2020

@author: bgossage
"""

import json
import numpy

with open( "../Downloads/pa_president.json" ) as votes_file:
    data = votes_file.read()
    
    db = json.loads( data )

    timeseries = db["data"]["races"][0]["timeseries"]
    
    prev_trump_count = 0
    prev_trump_share = 0.0
    item_count = 0

    for item in timeseries:
        votes = item["votes"]
        print( item["timestamp"], ": votes: " , votes )
        
        shares = item["vote_shares"]
        trump_share = shares["trumpd"]
        biden_share = shares["bidenj"]
        
        total_share = trump_share + biden_share
        
        print( "total share: ", total_share )

        
        print( "Trump share: ", trump_share)
        trump_count = int( trump_share * float(votes) )
        print( "Trump count: ", trump_count )
        
        print( "Biden share: ", biden_share )
        biden_count = int( biden_share * float(votes) )
        print( "Biden count: ",  biden_count )
        
        print( "Differential: ", trump_count - biden_count )
        print( "Missing votes: ", votes - int( total_share * float(votes) ) )
        
        if item_count > 10:
            if trump_count < prev_trump_count:
                print( "FRAUD WARNING!!!!" )
                input()
                #break
                
            if trump_share < prev_trump_share:
                print( "FRAUD ALERT!!!!" )
                input()
                #break
        
        prev_trump_count = trump_count
        prev_trump_share = trump_share
        item_count += 1
        
        print( "--------------------------------------\n" )
        
    #end for
    
#end while

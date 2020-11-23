#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 18:17:26 2020

@author: bgossage
"""

import json
import numpy
import matplotlib
import matplotlib.pyplot
from datetime import datetime

time_format = "%Y-%m-%dT%H:%M:%SZ"

with open( "mi_president.json" ) as votes_file:
    data = votes_file.read()
    
    db = json.loads( data )

    timeseries = db["data"]["races"][0]["timeseries"]
    
    prev_trump_count = 0
    prev_trump_share = 0.0
    prev_biden_count = 0
    prev_biden_share = 0.0
    prev_votes = 0
    
    item_count = 0        
    trump_debt = 0
    biden_debt = 0
    
    trump_shares = []
    trump_counts = []
    trump_deltas = []
    biden_shares = []
    biden_counts = []
    biden_deltas = []
    total_votes = []
    vote_deltas = []
    time_strings = []
    
    for item in timeseries:
        votes = item["votes"]
        total_votes.append( votes )
        vote_delta = votes - prev_votes
        vote_deltas.append( vote_delta )
        
        time_string = item["timestamp"];
        #time_string = time_string.replace('Z','+00:00')
        #time_string = time_string.replace('T',' ')
        print( time_string, ": votes: " , votes )
        

        time_strings.append( time_string )
        
        shares = item["vote_shares"]
        trump_share = shares["trumpd"]
        trump_shares.append( trump_share )
        
        biden_share = shares["bidenj"]
        biden_shares.append( biden_share )
        
        total_share = trump_share + biden_share
        
        print( "total share: ", total_share )

        
        print( "Trump share: ", trump_share)
        trump_count = int( trump_share * float(votes) )
        print( "Trump count: ", trump_count )
        trump_counts.append( trump_count )
        trump_deltas.append( trump_count - prev_trump_count )
        
        print( "Biden share: ", biden_share )
        biden_shares.append( biden_share )
        biden_count = int( biden_share * float(votes) )
        biden_counts.append( biden_count )
        print( "Biden count: ",  biden_count )
        biden_deltas.append( biden_count - prev_biden_count )
        
        print( "Differential: ", trump_count - biden_count )
        missing_votes = votes - int( total_share * float(votes) )
        print( "Missing votes: ", missing_votes )


        prev_trump_count = trump_count
        prev_trump_share = trump_share
        prev_biden_count = biden_count
        prev_trump_share = biden_share
        prev_votes = votes
        
        item_count += 1
        
        print( "--------------------------------------\n" )
        
    #end for
    
    print( "Total Trump debt: ", trump_debt )
    print( "Total Biden debt: ", biden_debt )
    
## Proportional control law?

#end with
    
    vote_stream = open( "pa_president.json" )
    
    stream_data = json.load( vote_stream )
    
    pp_stream = open( "pa_president_pp.json", "w" )
    
    pp_string = json.dumps( stream_data, indent = 3 )
    
    pp_stream.write( pp_string )
    pp_stream.close()

#############################################################3

    start_index = 0
    num_samples = 525
    end_index = start_index + num_samples
    
    start_time = time_strings[ 1 ]
    start_time_obj = datetime.strptime(start_time , time_format )
    
    print( "Start time: ", start_time )
    
    time_values = numpy.empty( num_samples )
    trump_values = numpy.empty( num_samples )
    biden_values = numpy.empty( num_samples )
    vote_values = numpy.empty( num_samples )
    
    i = 0
    
    for index in numpy.arange(start_index,end_index):

        sample_time = time_strings[index]
        #print( "Time: ", sample_time )
        date_time_obj = datetime.strptime(sample_time, time_format )
       # print( "Time obj: ", date_time_obj.strftime( time_format ) )
       
        delta_time = date_time_obj - start_time_obj
        
        elapsed_time = delta_time.total_seconds()
        #print( "delta: ", delta_time )
        time_values[i] = elapsed_time / (60.0 * 60)
        trump_values[i] = trump_deltas[index]
        biden_values[i] = biden_deltas[index]
        vote_values[i] = vote_deltas[index]
        
        print( i, ", ", time_values[i], "   ", trump_values[i] )

        i += 1

    
# Plot the solution...
    matplotlib.pyplot.title( "President 2020" )
    matplotlib.pyplot.figure( 0, figsize=(10,8) )
    matplotlib.pyplot.legend( loc='best' )
    matplotlib.pyplot.xlabel( "t (hours)" )
    matplotlib.pyplot.ylabel( "vote deltas" )
    matplotlib.pyplot.scatter( time_values, trump_values,
                            label="Trump", linestyle=':', color='r' 
                          )
    matplotlib.pyplot.scatter( time_values, biden_values,
                            label="Biden", linestyle='--', color='b' 
                          )
 #   matplotlib.pyplot.scatter( time_values, vote_values,
 #                           label="Votes", linestyle='-', color='g' 
 #                         )
    
    
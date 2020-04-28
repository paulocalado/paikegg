# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 17:01:23 2020

@author: paulo
"""

import pandas as pd
import streamlit as st
from riotwatcher import LolWatcher, ApiError
import plotly.express as px
import plotly.graph_objects as go

def getGame(summoner, api_key):
    watcher = LolWatcher(api_key)
    my_region = 'br1'
    
    me = watcher.summoner.by_name(my_region, summoner)
    #df = pd.DataFrame(me)
    my_matches = watcher.match.matchlist_by_account(my_region, me['accountId'])

# fetch last match detail
    last_match = my_matches['matches'][0]
    match_detail = watcher.match.by_id(my_region, last_match['gameId'])
    
    return match_detail
   
    

def getDamage(name,match_detail):
    participants = []
    participants_id = []
    for row in match_detail['participants']:
        participants_row = {}
        participants_row['champion'] = row['championId']
        participants_row['spell1'] = row['spell1Id']
        participants_row['spell2'] = row['spell2Id']
        participants_row['win'] = row['stats']['win']
        participants_row['kills'] = row['stats']['kills']
        participants_row['deaths'] = row['stats']['deaths']
        participants_row['assists'] = row['stats']['assists']
        participants_row['totalDamageDealt'] = row['stats']['totalDamageDealt']
        participants_row['goldEarned'] = row['stats']['goldEarned']
        participants_row['champLevel'] = row['stats']['champLevel']
        participants_row['totalMinionsKilled'] = row['stats']['totalMinionsKilled']
        participants_row['item0'] = row['stats']['item0']
        participants_row['item1'] = row['stats']['item1']
        participants_row['participant_id'] = row['stats']['participantId']
        participants.append(participants_row)
        
    for row in match_detail['participantIdentities']:
        participantsIdentities_row = {}
        participantsIdentities_row['id'] = row['participantId']
        participantsIdentities_row['name'] = row['player']['summonerName']
        participantsIdentities_row['profileIcon'] = row['player']['profileIcon']
        participants_id.append(participantsIdentities_row)
    
    playerInfo = pd.DataFrame(participants_id)
    matchInfo = pd.DataFrame(participants)    
    fullInfo = matchInfo.merge(playerInfo,left_on='participant_id',right_on='id')
    fullInfo['color'] = 'blue'
    fullInfo.loc[fullInfo['name']==name,'color'] = 'red'
    st.dataframe(fullInfo.drop(['participant_id','id'],axis=1))
    
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
            x=fullInfo['name'],
            y=fullInfo['totalDamageDealt'],
            text = fullInfo['totalDamageDealt'],
            textposition = 'auto',
            marker_color = fullInfo['color']
            ))
  
    fig.update_layout(xaxis = {'categoryorder': 'total descending'})
    st.write(fig)
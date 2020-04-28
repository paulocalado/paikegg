# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 19:33:53 2020

@author: paulo
"""

import requests as rt
import streamlit as st
import pandas as pd
import json
from riotwatcher import LolWatcher, ApiError
from api_methods import getGame, getDamage

def main():
    st.title("Hello League")
    summonerName = st.text_input("Summoner:")
    api_key = 'RGAPI-2a009ea4-a77e-4815-ae7c-ec5a110e1e8e'
    if(summonerName != ''):
         match_detail = getGame(summonerName, api_key)
         selectbox = st.selectbox('What do you want to know about your last game?',('Damage','Vision'))
         if selectbox == 'Damage':
             getDamage(summonerName, match_detail)
         elif selectbox == 'Vision':
             st.markdown('Vision')
        
    

if __name__ == '__main__':
    main()
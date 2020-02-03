# -*- coding: utf-8 -*-
import json
import pandas as pd
from pandas.io.json import json_normalize
import os.path 
import urllib
from flask import Flask

app = Flask(__name__)


leagueid='471237557296820224'
league_string2 = '[{"user_id":"436876366495870976","settings":null,"metadata":{"user_message_pn":"on","transaction_waiver":"on","transaction_trade":"on","transaction_free_agent":"on","transaction_commissioner":"on","team_name_update":"on","team_name":"Johnson and Johnson","player_nickname_update":"on","mention_pn":"on","mascot_message_leg_2":"","mascot_message_emotion_leg_2":"idle","mascot_message_emotion_leg_1":"idle_nervous","mascot_message":"on","mascot_item_type_id_leg_1":"","allow_pn":"on"},"league_id":"471237557296820224","is_owner":null,"is_bot":false,"display_name":"MarkyJ","avatar":"56954d15232c82270bc35562afa6db5f"},{"user_id":"465431267769315328","settings":null,"metadata":{"team_name":"Never Fournette","mention_pn":"on","mascot_message_leg_5":"Dude.  Do you even lift?","mascot_message_leg_4":"","mascot_message_leg_2":"","mascot_message_leg_14":"Smoked","mascot_message_leg_11":"","mascot_message_leg_1":"","mascot_message_emotion_leg_5":"idle","mascot_message_emotion_leg_4":"idle","mascot_message_emotion_leg_14":"idle","mascot_message_emotion_leg_13":"idle_happy","mascot_message_emotion_leg_11":"idle","mascot_message_emotion_leg_1":"","mascot_item_type_id_leg_17":"","mascot_item_type_id_leg_16":"","mascot_item_type_id_leg_15":"","mascot_item_type_id_leg_14":"","mascot_item_type_id_leg_13":"","allow_pn":"on"},"league_id":"471237557296820224","is_owner":null,"is_bot":false,"display_name":"MSorrenson","avatar":"9cf0ba07b858634478ff0edec78d0412"},{"user_id":"466181495111806976","settings":null,"metadata":{"mention_pn":"on","mascot_message_leg_5":"","mascot_message_leg_3":"","mascot_message_leg_2":"Smoked","mascot_message_leg_14":"","mascot_message_leg_11":"It’s been a long time between drinks - was just wondering if you still knew how to spell it","mascot_message_emotion_leg_3":"idle","mascot_message_emotion_leg_2":"idle","mascot_message_emotion_leg_11":"idle","mascot_item_type_id_leg_9":"","mascot_item_type_id_leg_8":"","mascot_item_type_id_leg_7":"","mascot_item_type_id_leg_6":"","mascot_item_type_id_leg_5":"","mascot_item_type_id_leg_4":"","mascot_item_type_id_leg_3":"","mascot_item_type_id_leg_17":"","mascot_item_type_id_leg_16":"","mascot_item_type_id_leg_15":"","mascot_item_type_id_leg_14":"","mascot_item_type_id_leg_13":"","mascot_item_type_id_leg_12":"","mascot_item_type_id_leg_11":"","mascot_item_type_id_leg_10":"","allow_pn":"on"},"league_id":"471237557296820224","is_owner":true,"is_bot":false,"display_name":"skzm","avatar":null},{"user_id":"466816403391901696","settings":null,"metadata":{"team_name":"Kamara shy","mention_pn":"on","mascot_message_leg_4":"SNAP!","mascot_message_leg_3":"If I cut a loud fart you will short circuit","mascot_message_leg_2":"All season mofo","mascot_message_leg_1":"I must break you","mascot_message_emotion_leg_7":"idle","mascot_message_emotion_leg_5":"idle","mascot_message_emotion_leg_4":"action_hurt01","mascot_message_emotion_leg_3":"idle","mascot_message_emotion_leg_2":"idle","mascot_message_emotion_leg_1":"idle","mascot_item_type_id_leg_9":"","mascot_item_type_id_leg_8":"","mascot_item_type_id_leg_7":"","mascot_item_type_id_leg_6":"","mascot_item_type_id_leg_5":"","mascot_item_type_id_leg_4":"","mascot_item_type_id_leg_3":"","mascot_item_type_id_leg_2":"","mascot_item_type_id_leg_17":"","mascot_item_type_id_leg_16":"","mascot_item_type_id_leg_15":"","mascot_item_type_id_leg_14":"","mascot_item_type_id_leg_13":"","mascot_item_type_id_leg_12":"","mascot_item_type_id_leg_11":"","mascot_item_type_id_leg_10":"","mascot_item_type_id_leg_1":"","allow_pn":"on"},"league_id":"471237557296820224","is_owner":null,"is_bot":false,"display_name":"AKamara41","avatar":"55d84a9842931cd39b70ed61cda09c06"}]'
	
league = json.loads(league_string2)
for i in range(1,16):
	print(i)
	if os.path.exists("mu" + str(i) + "-" + leagueid + ".txt"):	
		with open("mu" + str(i) + "-" + leagueid + ".txt", "r") as read_file:
			data = json.load(read_file)
	else:
		with urllib.request.urlopen("https://api.sleeper.app/v1/league/" + leagueid + "/matchups/" + str(i)) as url:
			data  = json.loads(url.read().decode())
		with open("mu" + str(i) + "-" + leagueid + ".txt", "w") as write_file:
			json.dump(data, write_file)
	

	if os.path.exists("s" + str(i) + ".txt"):	
		with open("s" + str(i) + ".txt", "r") as read_file:
			s1 = json.load(read_file)
	else:
		with urllib.request.urlopen("https://api.sleeper.app/v1/stats/nfl/regular/2019/" + str(i)) as url:
			s1  = json.loads(url.read().decode())
		with open("s" + str(i) + ".txt", "w") as write_file:
			json.dump(s1, write_file)

	stats_df = pd.DataFrame.from_dict(s1).transpose()
	
	for j in range(len(data)):
		bench2 = pd.DataFrame(set(data[j]['players'])- set(data[j]['starters']), columns=['player_id'])	
		bench2 = pd.merge(bench2, stats_df, how='left', left_on='player_id', right_index=True)[['player_id', 'pts_ppr']]		
		bench2['roster_id'] = j
		start2 = pd.DataFrame(data[j]['starters'], columns=['player_id'])
		start2 = pd.merge(start2, stats_df, how='left', left_on='player_id', right_index=True)[['player_id', 'pts_ppr']]		
		start2['roster_id'] = j

		if j == 0:
			bench1 = bench2
			start1 = start2
		else:
			bench1 = pd.concat([bench1, bench2])
			start1 = pd.concat([start1, start2])
	
	if i == 1:
		bench = bench1
		start = start1
	else:
		bench = pd.DataFrame.merge(bench, bench1, how='outer', on=['player_id', 'roster_id'])
		start = pd.DataFrame.merge(start, start1, how='outer', on=['player_id', 'roster_id'])
	
	bench = bench.rename(columns = {'pts_ppr':'week' + str(i)})
	start = start.rename(columns = {'pts_ppr':'week' + str(i)})

with open("players.txt", "r") as read_file:
	dfpl = json.load(read_file)
player_df = pd.DataFrame.from_dict(dfpl).transpose()
print(bench)
bench = pd.merge(bench, player_df, how='left', left_on='player_id', right_on='player_id')[['player_id','full_name','week1','week2','week3','week4','week5','week6','week7','week8','week9','week10','week11','week12','week13','week14','week15', 'roster_id']]
start = pd.merge(start, player_df, how='left', left_on='player_id', right_on='player_id')[['player_id','full_name','week1','week2','week3','week4','week5','week6','week7','week8','week9','week10','week11','week12','week13','week14','week15', 'roster_id']]
start['Total'] = start.sum(axis=1)
bench['Total'] = bench.sum(axis=1)
print(bench.sort_values('Total', ascending=False).head(10)[['player_id', 'full_name', 'Total', 'roster_id']])

#df2 = pd.DataFrame(data2[0]['starters'], columns=['player_id'])
#df2 = pd.merge(df2, stats_df, how='left', left_on='player_id', right_index=True)[['player_id', 'pts_ppr']]
#df2.columns.values[1] = 'week1'
#df3 = pd.DataFrame.merge(df, df2, how='outer', on='player_id')
#print(df3)




#df3 = pd.concat([df2,df[~df.player_id.isin(df2.player_id)]],axis=0)

#df3.loc[df[~df.player_id.isin(df2.player_id)],'pts_ppr'] = df.loc[df[~df.player_id.isin(df2.player_id)],'pts_ppr']

#
#print(stats_df)
#draft_summary = pd.merge(df, stats_df, how='left', left_on='player_id', right_index=True)[['player_id', 'pts_ppr']]
#print(draft_summary)
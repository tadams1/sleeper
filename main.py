
# -*- coding: utf-8 -*-
import json
import pandas as pd


from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
	json_string = '[{"type":"snake","status":"complete","start_time":1566726780000,"sport":"nfl","settings":{"teams":4,"slots_wr":3,"slots_te":2,"slots_super_flex":1,"slots_rb":3,"slots_qb":2,"slots_flex":2,"slots_def":1,"slots_bn":8,"rounds":24,"player_type":0,"pick_timer":60,"cpu_autopick":1,"alpha_sort":0},"season_type":"regular","season":"2019","metadata":{"scoring_type":"dynasty","name":"Dynasty","description":""},"league_id":"471237557296820224","last_picked":1566728606783,"last_message_time":1566728606859,"last_message_id":"471297572451905536","draft_order":{"466816403391901696":4,"466181495111806976":1,"465431267769315328":3,"436876366495870976":2},"draft_id":"471237560434159616","creators":["466181495111806976"],"created":1566714298871}]'
	league_string = '[{"user_id":"436876366495870976","settings":null,"metadata":{"user_message_pn":"on","transaction_waiver":"on","transaction_trade":"on","transaction_free_agent":"on","transaction_commissioner":"on","team_name_update":"on","team_name":"Johnson and Johnson","player_nickname_update":"on","mention_pn":"on","mascot_message_leg_2":"","mascot_message_emotion_leg_2":"idle","mascot_message_emotion_leg_1":"idle_nervous","mascot_message":"on","mascot_item_type_id_leg_1":"","allow_pn":"on"},"league_id":"471237557296820224","is_owner":null,"is_bot":false,"display_name":"MarkyJ","avatar":"56954d15232c82270bc35562afa6db5f"},{"user_id":"465431267769315328","settings":null,"metadata":{"team_name":"Never Fournette","mention_pn":"on","mascot_message_leg_5":"Dude.  Do you even lift?","mascot_message_leg_4":"","mascot_message_leg_2":"","mascot_message_leg_14":"Smoked","mascot_message_leg_11":"","mascot_message_leg_1":"","mascot_message_emotion_leg_5":"idle","mascot_message_emotion_leg_4":"idle","mascot_message_emotion_leg_14":"idle","mascot_message_emotion_leg_13":"idle_happy","mascot_message_emotion_leg_11":"idle","mascot_message_emotion_leg_1":"","mascot_item_type_id_leg_17":"","mascot_item_type_id_leg_16":"","mascot_item_type_id_leg_15":"","mascot_item_type_id_leg_14":"","mascot_item_type_id_leg_13":"","allow_pn":"on"},"league_id":"471237557296820224","is_owner":null,"is_bot":false,"display_name":"MSorrenson","avatar":"9cf0ba07b858634478ff0edec78d0412"},{"user_id":"466181495111806976","settings":null,"metadata":{"mention_pn":"on","mascot_message_leg_5":"","mascot_message_leg_3":"","mascot_message_leg_2":"Smoked","mascot_message_leg_14":"","mascot_message_leg_11":"It’s been a long time between drinks - was just wondering if you still knew how to spell it","mascot_message_emotion_leg_3":"idle","mascot_message_emotion_leg_2":"idle","mascot_message_emotion_leg_11":"idle","mascot_item_type_id_leg_9":"","mascot_item_type_id_leg_8":"","mascot_item_type_id_leg_7":"","mascot_item_type_id_leg_6":"","mascot_item_type_id_leg_5":"","mascot_item_type_id_leg_4":"","mascot_item_type_id_leg_3":"","mascot_item_type_id_leg_17":"","mascot_item_type_id_leg_16":"","mascot_item_type_id_leg_15":"","mascot_item_type_id_leg_14":"","mascot_item_type_id_leg_13":"","mascot_item_type_id_leg_12":"","mascot_item_type_id_leg_11":"","mascot_item_type_id_leg_10":"","allow_pn":"on"},"league_id":"471237557296820224","is_owner":true,"is_bot":false,"display_name":"skzm","avatar":null},{"user_id":"466816403391901696","settings":null,"metadata":{"team_name":"Kamara shy","mention_pn":"on","mascot_message_leg_4":"SNAP!","mascot_message_leg_3":"If I cut a loud fart you will short circuit","mascot_message_leg_2":"All season mofo","mascot_message_leg_1":"I must break you","mascot_message_emotion_leg_7":"idle","mascot_message_emotion_leg_5":"idle","mascot_message_emotion_leg_4":"action_hurt01","mascot_message_emotion_leg_3":"idle","mascot_message_emotion_leg_2":"idle","mascot_message_emotion_leg_1":"idle","mascot_item_type_id_leg_9":"","mascot_item_type_id_leg_8":"","mascot_item_type_id_leg_7":"","mascot_item_type_id_leg_6":"","mascot_item_type_id_leg_5":"","mascot_item_type_id_leg_4":"","mascot_item_type_id_leg_3":"","mascot_item_type_id_leg_2":"","mascot_item_type_id_leg_17":"","mascot_item_type_id_leg_16":"","mascot_item_type_id_leg_15":"","mascot_item_type_id_leg_14":"","mascot_item_type_id_leg_13":"","mascot_item_type_id_leg_12":"","mascot_item_type_id_leg_11":"","mascot_item_type_id_leg_10":"","mascot_item_type_id_leg_1":"","allow_pn":"on"},"league_id":"471237557296820224","is_owner":null,"is_bot":false,"display_name":"AKamara41","avatar":"55d84a9842931cd39b70ed61cda09c06"}]'

	with open("1.txt", "r") as read_file:
	    data = json.load(read_file)

	with open("2.txt", "r") as read_file:
	    player = json.load(read_file)

	with open("3.txt", "r") as read_file:
	    stats = json.load(read_file)

	df = pd.DataFrame.from_dict(stats).transpose() 
	league = json.loads(league_string)
	#df1 = df.sort_values('pts_ppr', ascending=False).head(1).join(player, on='player_id')

	draft_df = pd.DataFrame.from_dict(data)
	league_df = pd.DataFrame.from_dict(league)
	player_df = pd.DataFrame.from_dict(player).transpose()
	stats_df = pd.DataFrame.from_dict(stats).transpose()
	draft_summary = pd.merge(draft_df, league_df, how='left', left_on='picked_by', right_on='user_id')[['round', 'display_name', 'player_id']]
	draft_summary2 = pd.merge(draft_summary, player_df, how='left', left_on='player_id', right_on='player_id')[['round', 'display_name', 'player_id', 'full_name', 'position']]
	draft_summary3 = pd.merge(draft_summary2, stats_df, how='left', left_on='player_id', right_index=True)[['round', 'display_name', 'player_id', 'full_name', 'pts_ppr', 'position']]
	draft_summary3['position_rank'] = draft_summary3.groupby('position')['pts_ppr'].rank(ascending=False)
	draft_summary3['position_average'] = draft_summary3.groupby('position')['pts_ppr'].mean()
	draft_summary3['overall_rank'] = draft_summary3['pts_ppr'].rank(ascending=False)

	#for x in data:
	#	print x['metadata']['last_name']
	#	print stats['4881']

	league = json.loads(league_string)
	#for g in league:
	#	print(g['display_name'])

	draft = json.loads(json_string)
	return draft_summary3.to_html(header="true", table_id="table")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

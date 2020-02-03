# -*- coding: utf-8 -*-
import json
import pandas as pd
from pandas.io.json import json_normalize
from pandas_highcharts.core import serialize
import numpy as np
from flask import request
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/players')
def hello_world():
	position = request.args.get('position') if  request.args.get('position') != None else 'RB'
	try:
		playercount = int(request.args.get('playercount'))
	except (ValueError, TypeError):
		playercount = 20
#	for i in range(1,16):	
#		with open("mu" + str(i) + ".txt", "r") as read_file:
#			data = json.load(read_file)	
#		
#		with open("s" + str(i) + ".txt", "r") as read_file:
#			s1 = json.load(read_file)
#
#		stats_df = pd.DataFrame.from_dict(s1).transpose()
#		
#		dfa = pd.DataFrame(set(data[3]['players'])- set(data[3]['starters']), columns=['player_id'])	
#		dfa = pd.merge(dfa, stats_df, how='left', left_on='player_id', right_index=True)[['player_id', 'pts_ppr']]		
#		
#		if i == 1:
#			df = dfa
#		else:
#			df = pd.DataFrame.merge(df, dfa, how='outer', on='player_id')
#		
#		df.columns.values[i] = 'week' + str(i)	

	dfsingle= pd.DataFrame(data = {'player_id': ['6151', '2315']})	
	dfsingle.set_index('player_id', inplace=True)
	
	print(dfsingle)
	with open("players.txt", "r") as read_file:
		dfpl = json.load(read_file)
		
	with open("stats.txt", "r") as read_file:
		stats = json.load(read_file)
	stats_df = pd.DataFrame.from_dict(stats).transpose()
	player_df = pd.DataFrame.from_dict(dfpl).transpose()
	dfax = pd.merge(stats_df, player_df, how='left', right_on='player_id', left_index=True) #	
	
	dfx = dfax.loc[dfax['position'] == position].sort_values('pts_ppr', ascending= False).head(playercount)[['pts_ppr','position', 'full_name']]
	dfx.rename(columns={'pts_ppr': 'pts_ppr_full'}, inplace = True)	
	for i in range(1,16):	
		with open("s" + str(i) + ".txt", "r") as read_file:
			s1 = json.load(read_file)
		
		wstats_df = pd.DataFrame.from_dict(s1).transpose()[['pts_ppr']]
		dfsingle = pd.merge(dfsingle, wstats_df, how='left',  left_index=True , right_index=True)		
		dfsingle.rename(columns={'pts_ppr': 'week' + str(i)}, inplace = True)
		dfx = pd.merge(dfx, wstats_df, how='left', left_index=True, right_index=True)
		dfx.rename(columns={'pts_ppr': 'week' + str(i)}, inplace = True)
		
	
	print(dfsingle)
	#print(dfsingle.ix['167'].replace(np.nan, 'null').tolist())
	st = dfx.describe()
	print(st)
	del st['pts_ppr_full']
	dfx['graph'] =  ['No' for i in range(0, len(dfx.index))]
	print(dfx)
#		
#		if i == 1:
#			df = dfa
#		else:
#			df = pd.DataFrame.merge(df, dfa, how='outer', on='player_id')
#		
#		df.columns.values[i] = 'week' + str(i)	

	
	#player_df = pd.DataFrame.from_dict(dfpl).transpose()
	#df = pd.merge(df, player_df, how='left', left_on='player_id', right_on='player_id')[['player_id','full_name','week1','week2','week3','week4','week5','week6','week7','week8','week9','week10','week11','week12','week13','week14','week15']]
		
	#df2 = df[['player_id','full_name','week1']]
	chart = {"renderTo": 'chart_ID', "type": 'line', "height": 350,}
	#series = [{"name": 'Label1', "data": df['week1'].replace(np.nan, 'null').tolist()}, {"name": 'Label2', "data": df['week2'].replace(np.nan, 'null').tolist()}]
	
	series = [{"name": 'Top' + str(playercount) + ' Avg', "data": st.ix['mean'].replace(np.nan, 'null').tolist()}]
	title = {"text": 'Week by Week'}
	xAxis = {"categories": ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8', 'W9', 'W10', 'W11', 'W12', 'W13', 'W14', 'W15']}
	yAxis = {"title": {"text": 'yAxis PPR PTS'}}	
	return render_template('players.html',  data = json.dumps(dfx.replace(np.nan, 'null').values.tolist()), titles=dfx.columns.values.tolist(), chartID='chart_ID', chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis, position=position, playercount=playercount)

	
@app.route('/txns')
def txns():
	with open("tx6.txt", "r") as read_file:
		txl = json.load(read_file)
	
	with open("players.txt", "r") as read_file:
		dfpl = json.load(read_file)
		
	with open("stats.txt", "r") as read_file:
		stats = json.load(read_file)
		
	stats_df = pd.DataFrame.from_dict(stats).transpose()
	player_df = pd.DataFrame.from_dict(dfpl).transpose()
	dfx = pd.merge(stats_df, player_df, how='left', right_on='player_id', left_index=True) #	
	
	dfx = dfx[['pts_ppr','position', 'full_name']]
	dfx = dfx.dropna()
	dfx.rename(columns={'pts_ppr': 'pts_ppr_full'}, inplace = True)		
	
	dft = pd.DataFrame.from_dict(txl)[['type', 'status', 'adds', 'drops']]
	dft['added_player'] = dft['adds'].apply(lambda x : [*x][0] if x != None else None)
	dft['added_roster'] = dft['adds'].apply(lambda x : x[[*x][0]] if x != None else None)
	dft['dropped_player'] = dft['drops'].apply(lambda x : [*x][0] if x != None else None)
	dft['dropped_roster'] = dft['drops'].apply(lambda x : x[[*x][0]] if x != None else None)
	
	print(dft)
	dft = pd.merge(dft, dfx , how='left', left_on='added_player', right_index=True)
	dft.rename(columns={'pts_ppr_full': 'add_pts_ppr_full','position': 'add_position', 'full_name': 'add_full_name'}, inplace = True)		
	dft = pd.merge(dft, dfx , how='left', left_on='dropped_player', right_index=True)
	dft.rename(columns={'pts_ppr_full': 'drop_pts_ppr_full','position': 'drop_position', 'full_name': 'drop_full_name'}, inplace = True)		
	print(dft)
	return render_template('txns.html',  data = json.dumps(dft.replace(np.nan, 'null').values.tolist()))

@app.route('/txnstats')
def txnstats():
	with open("players.txt", "r") as read_file:
		dfpl = json.load(read_file)
		
	with open("stats.txt", "r") as read_file:
		stats = json.load(read_file)
		
	stats_df = pd.DataFrame.from_dict(stats).transpose()
	player_df = pd.DataFrame.from_dict(dfpl).transpose()
	dfx = pd.merge(stats_df, player_df, how='left', right_on='player_id', left_index=True) #	
	
	dfx = dfx[['pts_ppr','position', 'full_name']]
	dfx = dfx.dropna()
	dfx.rename(columns={'pts_ppr': 'pts_ppr_full'}, inplace = True)		
	
	for i in range(15,0,-1):	
		with open("s" + str(i) + ".txt", "r") as read_file:
			s1 = json.load(read_file)
			
		with open("tx" + str(i) + ".txt", "r") as read_file:
			txl = json.load(read_file)
			
		wstats_df = pd.DataFrame.from_dict(s1).transpose()[['pts_ppr']].fillna(0)
		dfx = pd.merge(dfx, wstats_df, how='left', left_index=True, right_index=True)
		dfx.rename(columns={'pts_ppr': 'week' + str(i)}, inplace = True)
		dfx['week' + str(i)]  = dfx['week' + str(i)].fillna(0)
		if i==15:
			dfx['ROS' + str(i)] = dfx['week' + str(i)]
		else:
			dfx['ROS' + str(i)] = dfx['week' + str(i)] + dfx['ROS' + str(i+1)]
		
		dft = pd.DataFrame.from_dict(txl)[['type', 'status', 'adds', 'drops']]
		dft['added_player'] = dft['adds'].apply(lambda x : [*x][0] if x != None else None)
		dft['added_roster'] = dft['adds'].apply(lambda x : x[[*x][0]] if x != None else None)
		dft['dropped_player'] = dft['drops'].apply(lambda x : [*x][0] if x != None else None)
		dft['dropped_roster'] = dft['drops'].apply(lambda x : x[[*x][0]] if x != None else None)
	
		dft = pd.merge(dft, dfx[['position', 'full_name','ROS' + str(i)]] , how='left', left_on='added_player', right_index=True)
		dft.rename(columns={'ROS' + str(i): 'add_pts_ppr_ros','position': 'add_position', 'full_name': 'add_full_name'}, inplace = True)			
		dft = pd.merge(dft, dfx[['position', 'full_name','ROS' + str(i)]] , how='left', left_on='dropped_player', right_index=True)
		dft.rename(columns={'ROS' + str(i): 'drop_pts_ppr_ros','position': 'drop_position', 'full_name': 'drop_full_name'}, inplace = True)		
		dft['week'] = i
		if i==15:
			dfn = dft
		else:
			dfn = pd.concat([dfn, dft])
	
	dfx = dfx.loc[dfx.index.isin(pd.concat([dfn['added_player'], dfn['dropped_player']]))]
	print(dfx)
	dfn = dfn.fillna(0)
	dfn['rosdiff'] = dfn['add_pts_ppr_ros'] - dfn['drop_pts_ppr_ros']	
	t1 = dfn[['add_full_name', 'added_player','added_roster', 'type']].groupby(['add_full_name', 'added_player','added_roster']).count().sort_values('type', ascending= False).head(20)
	t2 = dfn[['drop_full_name', 'dropped_player','dropped_roster', 'type']].groupby(['drop_full_name', 'dropped_player','dropped_roster']).count().sort_values('type', ascending= False).head(20)
	t3 = dfn[['add_full_name', 'added_player','type']].groupby(['add_full_name', 'added_player']).count().sort_values('type', ascending= False).head(20)
	t4 = dfn[['drop_full_name', 'dropped_player', 'type']].groupby(['drop_full_name', 'dropped_player']).count().sort_values('type', ascending= False).head(20)
	
	dfn.sort_values('rosdiff', ascending= False, inplace = True)
		
	return render_template('txns.html',  chart_data = dfx.to_json(orient='index'), data = json.dumps(dfn.replace(np.nan, 'null').values.tolist()),
	tables1=[t1.to_html(classes='data')], titles1=['name', 'id', 'roster','adds'],
	tables2=[t2.to_html(classes='data')], titles2=['name', 'id', 'roster','drops'],
	tables3=[t3.to_html(classes='data')], titles3=['name', 'id','adds'],
	tables4=[t4.to_html(classes='data')], titles4=['name', 'id', 'drops'])
	
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
	#hello_world()
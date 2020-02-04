# -*- coding: utf-8 -*-
import urllib, json
import pandas as pd
import numpy as np
from flask import request
from google.cloud import storage

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/<id>')
def hello_world(id):
	CLOUD_STORAGE_BUCKET = 'diesel-rhythm-93511.appspot.com'
	gcs = storage.Client()
	bucket = gcs.bucket(CLOUD_STORAGE_BUCKET)
	
	if not id:
		id='471237557296820224'
	
	with urllib.request.urlopen("https://api.sleeper.app/v1/league/" + id + "/users") as url:
		league = json.loads(url.read().decode())

	with urllib.request.urlopen("https://api.sleeper.app/v1/league/" + id + "/drafts") as url:
		drafts = json.loads(url.read().decode())

	with urllib.request.urlopen("https://api.sleeper.app/v1/draft/" + drafts[0]['draft_id'] + "/picks") as url:
		data  = json.loads(url.read().decode())

	player = json.loads(bucket.blob('players.txt').download_as_string())	
	stats = json.loads(bucket.blob('stats.txt').download_as_string())

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
	
	#return draft_summary3.to_html(header="true", table_id="table")
	return render_template('index.html',  tables=[draft_summary3.to_html(classes='data')], titles=draft_summary3.columns.values)
	
@app.route('/players')
def graph():
	position = request.args.get('position') if  request.args.get('position') != None else 'RB'
	stattype = request.args.get('stattype') if  request.args.get('stattype') != None else 'pts_ppr'
	try:
		playercount = int(request.args.get('playercount'))
	except (ValueError, TypeError):
		playercount = 20
		
	CLOUD_STORAGE_BUCKET = 'diesel-rhythm-93511.appspot.com'
	gcs = storage.Client()
	bucket = gcs.bucket(CLOUD_STORAGE_BUCKET)
	
	dfsingle= pd.DataFrame(data = {'player_id': ['6151', '2315']})	
	dfsingle.set_index('player_id', inplace=True)
	
	
	dfpl = player = json.loads(bucket.blob('players.txt').download_as_string())
	stats = json.loads(bucket.blob('stats.txt').download_as_string())
		
	stats_df = pd.DataFrame.from_dict(stats).transpose()
	player_df = pd.DataFrame.from_dict(dfpl).transpose()
	dfax = pd.merge(stats_df, player_df, how='left', right_on='player_id', left_index=True) #	
	
	dfx = dfax.loc[dfax['position'] == position].sort_values(stattype, ascending= False).head(playercount)[[stattype,'position', 'full_name']]
	dfx.rename(columns={stattype: stattype + '_full'}, inplace = True)	
	for i in range(1,16):	
		s1 = json.loads(bucket.blob('s'  + str(i) + '.txt').download_as_string())
		
		wstats_df = pd.DataFrame.from_dict(s1).transpose()[[stattype]]
		dfsingle = pd.merge(dfsingle, wstats_df, how='left',  left_index=True , right_index=True)		
		dfsingle.rename(columns={stattype: 'week' + str(i)}, inplace = True)
		dfx = pd.merge(dfx, wstats_df, how='left', left_index=True, right_index=True)
		dfx.rename(columns={stattype: 'week' + str(i)}, inplace = True)
		
	
	print(dfsingle)
	st = dfx.describe()
	del st[stattype + '_full']
	dfx['showvalues'] =  ['No' for i in range(0, len(dfx.index))]

	chart = {"renderTo": 'chart_ID', "type": 'line', "height": 350,}
	
	series = [{"name": 'Top' + str(playercount) + '  Avg', "data": st.ix['mean'].replace(np.nan, 'null').tolist()}]
	title = {"text": 'Week'}
	xAxis = {"categories": ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8', 'W9', 'W10', 'W11', 'W12', 'W13', 'W14', 'W15']}
	yAxis = {"title": {"text": 'yAxis ' + stattype}}
	return render_template('players.html',  data = json.dumps(dfx.replace(np.nan, 'null').values.tolist()), titles=json.dumps(dfx.columns.values.tolist()), chartID='chart_ID', chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis, position=position, playercount=playercount)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
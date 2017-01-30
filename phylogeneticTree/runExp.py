import json
from os import path
from scoreManip import dumpScore2Json
from drawTree import buildTree,drawTree
from distMatBuild import simiMat4Tree

#####################
# CHANGE THESE PATH #
#####################

# path where you store the scores
score_path = '/Users/gong/Documents/MTG document/Jingju arias/Scores'

# score info csv
score_info_filename = 'lyricsdata.csv'

# score json
score_json_filename = 'scores_withShengqiangBanshiSilence_noNormLengthPitch.json'

# similarity matrix json
namesSimiMat_filename = 'distMat_laosheng_eh_xp_noNormLengthPitch.json'

# index line csv
idx_line_filename = 'idx_line.csv'

# sorted similarity csv
sorted_simi_filename = 'sorted_dist_pairwise.csv'

##-- phrase subset for experiment, needs to be defined
phrase_subsets = [665, 666, 667, 668]


######################
# DON'T BOTHER THESE #
######################

score_info_filepath = path.join(score_path,score_info_filename)

##-- run this once, just dump all the score into a json file
# which stored in score_json_filename
dumpScore2Json(score_path,
               score_info_filepath,
               score_json_filename,
               onlyNotes=False,
               normalizeLength=False,
               normalizePitch=False)

##-- get the line identify and similarity matrix, store in namesSimiMat_filename
idx_keys = simiMat4Tree(score_json_filename,namesSimiMat_filename,idx_line_filename,sorted_simi_filename,phrase_subsets)

with open(namesSimiMat_filename,'r') as openfile:
    dict_distMat = json.load(openfile)

names = dict_distMat['names']
matrix = dict_distMat['matrix']

for ii in range(len(names)):
    data = names[ii]
    udata=data.decode("utf-8")
    names[ii]=udata.encode("ascii","ignore")

# print matrix[:6]

tree = buildTree(names,matrix)
drawTree(tree)

print idx_keys
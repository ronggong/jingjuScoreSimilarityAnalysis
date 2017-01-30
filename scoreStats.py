import json

filename_score = 'phylogeneticTree/scores_withShengqiangBanshiSilence_noNormLengthPitch.json'

score = json.load(open(filename_score,'rb'))

numLine_laosheng = 0
numLine_dan = 0
for key in score:
    if score[key]['roletype'] == 'laosheng':
        numLine_laosheng += 1
    elif score[key]['roletype'] == 'dan':
        numLine_dan += 1

print numLine_laosheng,numLine_dan
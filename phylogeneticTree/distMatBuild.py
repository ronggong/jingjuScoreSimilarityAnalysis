import json,sys
import unicodecsv as csv
from os import path
import numpy as np
from operator import itemgetter
from dtwSankalp import dtw1d_generic

dict_shengqiang = {u'xipi':u'xp', u'erhuang':u'eh'}
dict_banshi     = {u'manban':u'man', u'daoban':u'dao', u'sanyan':u'san', u'liushui':u'liu',
                   u'zhongsanyan':u'zhongsan', u'kuaiban':u'kuai',u'erliu':u'er', u'kuaisanyan':u'kuaisan',
                   u'sanban':u'san', u'yuanban':u'yuan', u'yaoban':u'yao'}
dict_roletype   = {u'dan':u'da', u'laosheng':u'ls', u'laodan':u'ld'}

def sortSimi(distMat,idx_keys):
    names = distMat['names']
    mat = distMat['matrix']

    indices = []
    for n in names:
        indices.append(n.split('_')[0])

    dist_pairwise = []
    for ii,idx_ii in enumerate(indices):
        for jj,mat_ii_jj in enumerate(mat[ii]):
            if mat_ii_jj:
                dist_pairwise.append([idx_keys[int(idx_ii)][0],idx_keys[int(idx_ii)][1],
                                      idx_keys[int(indices[jj])][0],idx_keys[int(indices[jj])][1],
                                      mat_ii_jj])
    dist_pairwise = sorted(dist_pairwise,key=itemgetter(4))

    return dist_pairwise

def simiMat4Tree(score_json_filename,namesSimiMat_filename,idx_line_filename,sort_simi_filename,phrase_subsets):
    with open(score_json_filename,'r') as openfile:
        dict_scores = json.load(openfile)

    names = []
    pitchtracks = []
    shengqiangs = []
    banshis     = []
    couplets     = []
    roletypes    = []
    idx_keys     = {}

    for ii,key in enumerate(dict_scores):
        # print key
        if key.split('_')[0] in phrase_subsets:

            idx_keys[ii] = [key.split('_')[0]+'_'+str(int(key.split('_')[1])+1),dict_scores[key]['lyrics']]

            shengqiang  = dict_scores[key]['shengqiang']
            banshi      = dict_scores[key]['banshi']
            couplet     = dict_scores[key]['couplet']
            roletype    = dict_scores[key]['roletype']

            shengqiangs.append(shengqiang)
            banshis.append(banshi)
            couplets.append(couplet)
            roletypes.append(roletype)

            identify_phrase = str(ii)+'_'+dict_roletype[roletype]+'_'+dict_shengqiang[shengqiang]\
                              +'_'+dict_banshi[banshi]+'_'+couplet

            pitchtrack  = dict_scores[key]['pitchtrack_cents']

            names.append(identify_phrase)
            pitchtracks.append(pitchtrack)

    # print set(shengqiangs)
    # print set(banshis)
    # print set(couplets)
    # print set(roletypes)

    ##-- random choose from the array 100 elements
    a = np.arange(len(names))
    np.random.shuffle(a)

    names = [names[ii] for ii in a[:100]]
    pitchtracks = [pitchtracks[ii] for ii in a[:100]]

    matrix = [[0.0]]
    for ii in range(1,len(pitchtracks)):
        list_dist = []
        for jj in range(ii):
            list_dist.append(dtw1d_generic(pitchtracks[ii],pitchtracks[jj]))
        list_dist.append(0.0)
        matrix.append(list_dist)

    distMat = {'names':names,'matrix':matrix}

    with open(namesSimiMat_filename,'wb') as openfile:
        json.dump(distMat,openfile)

    with open(path.join(idx_line_filename),'wb') as csvfile:
        w = csv.writer(csvfile)
        for key in idx_keys:
            w.writerow([key,idx_keys[key][0],idx_keys[key][1]])

    dist_pairwise_sorted = sortSimi(distMat,idx_keys)

    with open(path.join(sort_simi_filename),'wb') as csvfile:
        w = csv.writer(csvfile)
        for dps in dist_pairwise_sorted:
            w.writerow(dps)

    return idx_keys
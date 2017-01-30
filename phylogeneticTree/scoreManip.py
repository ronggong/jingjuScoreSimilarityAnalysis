# -*- coding: utf-8 -*-
from os import path
from jingjuScores import getMelodicLine
# from general.filePath import *
# from general.parameters import *
from utilsFunctions import hz2cents,pitchtrackInterp,SAMPLE_NUM_TOTAL,SAMPLE_NUM_QUARTER
import numpy as np
import csv,json

import matplotlib.pyplot as plt

# score information *.csv
# score_info_filepath = path.join(score_path,score_info_file_shenqiang_banshi)

def getDictScoreInfo(score_info_filepath):
    dict_score_info = {}
    with open(score_info_filepath, 'rb') as csvfile:
        score_info = csv.reader(csvfile)

        aria_name_old = ''
        line_number = 0
        for ii_row, row in enumerate(score_info):
            if row[0] != 'File name':
                aria_name = row[0]
                if len(aria_name):
                    # row[0] != empty
                    line_number = 0
                    aria_name_old = aria_name
                    part = 1
                else:
                    line_number += 1


                if row[5][:4] == 'Part':
                    # if lyric is 'Part', redefine roleType and part
                    # roleType = row[1].split()[2]
                    part = int(row[5].split()[1])

                if row[5][:4] != 'Part':
                    try:
                        dict_score_info[ii_row+1] = {'lyrics':row[5],
                                                   'startEndOffset':[float(row[6]),float(row[7])],
                                                   'part':part,
                                                   'roletype':row[1],
                                                   'shengqiang':row[2],
                                                   'banshi':row[3],
                                                   'couplet':row[4],
                                                   'linenumber':line_number,
                                                   'arianame':aria_name_old}
                    except ValueError:
                        print(aria_name_old+'_'+str(ii_row)+' '+'valueError: '+row[6]+' '+row[7])

        return dict_score_info

def getScores(score_path, dict_score_info, onlyNotes = True):
    score_filename = dict_score_info['arianame']
    start = dict_score_info['startEndOffset'][0]
    end = dict_score_info['startEndOffset'][1]
    part = dict_score_info['part']
    score_file_path = path.join(score_path,score_filename)
    line = getMelodicLine(score_file_path, start, end, partIndex=part, show=False)

    notes = []
    if onlyNotes:
        for note in line.flat.notes.stream():
            notes.append({'freq':note.pitch.freq440,'lyric':note.lyric,'quarterLength':float(note.quarterLength)})
    else:
        for note in line.flat.notesAndRests.stream():
            if note.isRest:
                notes.append({'freq':0.0,'lyric':None,'quarterLength':float(note.quarterLength)})
            else:
                notes.append({'freq':note.pitch.freq440,'lyric':note.lyric,'quarterLength':float(note.quarterLength)})

    dict_score_info['notes'] = notes
    return dict_score_info

def melodySynthesize(notes_pitch_hz,
                     notes_quarterlength,
                     onlyNotes,
                     normalizeLength,
                     normalizePitch):
    '''
    :param notes_quarterlength: a list of the note quarterLength
    :return: list, pitch track values
    '''
    # print notes_quarterlength

    notes_pitch_cents = hz2cents(np.array(notes_pitch_hz))
    # print notes_pitch_cents

    length_total = sum(notes_quarterlength)

    melody = []
    for ii in range(len(notes_quarterlength)):
        if normalizeLength:
            sample_note = int(round((notes_quarterlength[ii]/length_total)*SAMPLE_NUM_TOTAL))
        else:
            sample_note = int(round(notes_quarterlength[ii]*SAMPLE_NUM_QUARTER))
        melody += [notes_pitch_cents[ii]]*sample_note

    melody = np.array(melody)

    # mean normalization
    if onlyNotes:
        if normalizePitch:
            melody = melody - np.mean(melody)
    else:
        idx_nonzero = np.where(melody != -np.inf)
        idx_zero    = np.where(melody == -np.inf)

        # normalize melody by subtract the mean of the non zero part
        melody_nonzero = melody[idx_nonzero]
        mean_melody_nonzero = np.mean(melody_nonzero)
        if normalizePitch:
            melody = melody - mean_melody_nonzero

            # assign silence index to 0 value
            if len(idx_zero):
                melody[idx_zero] = 0
        else:
            if len(idx_zero):
                melody[idx_zero] = mean_melody_nonzero

    melody = melody.tolist()

    # interpolation
    if normalizeLength:
        if len(melody) != SAMPLE_NUM_TOTAL:
            melody = pitchtrackInterp(melody)

    # plt.figure()
    # plt.plot(melody)
    # plt.show()

    return melody

##-- dump json scores
def dumpScore2Json(score_path,
                   score_info_filepath,
                   score_json_filename,
                   onlyNotes=True,
                   normalizeLength=True,
                   normalizePitch=True):

    dict_score_infos = getDictScoreInfo(score_info_filepath)

    for key in dict_score_infos:
        dict_score_info = dict_score_infos[key]
        dict_score_info = getScores(score_path, dict_score_info, onlyNotes)

        # synthesize melody
        notes_quarterLength = []
        notes_pitch_hz = []
        for dict_note in dict_score_infos[key]['notes']:
            notes_pitch_hz.append(dict_note['freq'])
            notes_quarterLength.append(dict_note['quarterLength'])

        pitchtrack_cents = melodySynthesize(notes_pitch_hz,
                                            notes_quarterLength,
                                            onlyNotes,
                                            normalizeLength,
                                            normalizePitch)
        dict_score_info['pitchtrack_cents'] = pitchtrack_cents

        dict_score_infos[key] = dict_score_info

    # print dict_score_infos[key]
    with open(score_json_filename,'w') as outfile:
        json.dump(dict_score_infos,outfile)

    # with open('scores.json','r') as f:
    #     dict_score_infos = json.load(f)

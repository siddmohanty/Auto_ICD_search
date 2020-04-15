from flask import request
import pickle
import json


def get_data():
    data_to_send = []
    age = request.form["age"]
    sex = request.form["sex"].upper()
    doctor = request.form["doctor"].upper()
    string = request.form['input'].lower()

    key = tuple([age, sex, doctor])
    print(key)


    with open('counts.pickle', 'rb') as readFile:
        counts = pickle.load(readFile)

    # counts_codes = []
    # counts_count = []
    # for item in counts[key]:
    #     counts_codes.append(item[0])
    #     counts_count.append(item[1])

    with open('icd_list.json') as f:
        icd_list = json.load(f)

    if key in counts.keys():

        counts_codes = []
        counts_count = []
        for item in counts[key]:
            counts_codes.append(item[0])
            counts_count.append(item[1])


        print("key is present")
        print("mined codes : ", counts_codes)
        desc_list = []
        code_list = []
        for desc_code in icd_list:
            desc, code = desc_code.split(":")
            desc = desc.lower().strip()
            code = code.strip()

            if string in desc:
                desc_list.append(desc)
                code_list.append(code)

        intersection = set(code_list).intersection(set(counts_codes))
        if len(intersection) == 0:
            for desc, code in zip(desc_list, code_list):
                data_to_send.append({"desc" : desc, "code" : code})

        else:
            for intersecting_code in intersection:
                counts_code_idx = counts_codes.index(intersecting_code)
                code = counts_codes[counts_code_idx]
                desc_idx = code_list.index(intersecting_code)
                desc = desc_list[desc_idx]
                freq_score = counts_count[counts_code_idx]

                print("counts_code_idx  ", counts_code_idx)
                print("desc_idx  ", desc_idx)
                print("desc  ", desc)
                print("freq_score  ", freq_score)

                data_to_send.append({"desc" : desc, "code" : code, "score" : freq_score})

                # if code in counts_codes:
                #     idx = counts_codes.index(code)
                #     freq_score = counts_count[idx]
                #     data_to_send.append({"desc" : desc, "code" : code, "score" : freq_score})

        print("desc list : ", desc_list)
        print("icd codes for given desc (code_list) : ", code_list)
        print("intersection : ", set(code_list).intersection(set(counts_codes)))


    if key not in counts.keys():
        print("key is not present")
        for desc_code in icd_list:
            desc, code = desc_code.split(":")
            desc = desc.lower().strip()
            code = code.strip()

            if string in desc:
                data_to_send.append({"desc" : desc, "code" : code})


    if len(data_to_send) != 0:
        if "score" in data_to_send[0].keys():
            data_to_send = sorted(data_to_send, key=lambda x:x["score"])

    return data_to_send

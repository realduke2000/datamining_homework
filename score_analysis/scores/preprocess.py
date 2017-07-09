#!/usr/bin/python
import os
import os.path


def get_all_cols():
    all_cols = set()
    for root, dirs, filenames in os.walk("./csv/"):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            with open(filepath) as f:
                col_line = f.readline()
                cols = col_line.split(',')
                all_cols.update([col.strip() for col in cols])
    return all_cols


def assert_full_filled(csv):
    if len(csv) <= 1:
        return
    row_len = len(csv['name'])
    for i in range(0, len(csv)):
        if len(csv[csv.keys()[i]]) == 0:
            csv[csv.keys()[i]] = ["" for r in range(row_len)]
        assert row_len == len(csv.values()[i]), "%s,%s:%s" % (
            str(csv["date"][0]), str(len(csv.values()[0])), str(len(csv.values()[i])))


def get_all_csv():
    csv_list = []
    cols = get_all_cols()
    for root, dirs, files in os.walk('./csv/'):
        for filename in files:
            filepath = os.path.join(root, filename)
            score_type = filename.split('.')[2]
            score_date = "-".join(filename.split('.')[0:2]) + "-01"
            csv_data = read_csv_file(filepath, cols)
            row_len = len(csv_data['name'])
            csv_data['type'] = [score_type for k in range(row_len)]
            csv_data['date'] = [score_date for k in range(row_len)]
            assert_full_filled(csv_data)
            csv_list.append(csv_data)
    return merge_csv(csv_list)


def read_csv_file(filename, cols):
    dataframe = {}
    for col in cols:
        dataframe[col] = []

    with open(filename) as csv_file:
        headers = csv_file.readline().split(',')
        headers = [h.strip() for h in headers]
        for line in csv_file.readlines():
            fields = [s.strip() for s in line.split(',')]
            assert len(headers) == len(fields), "file(%s):header(%s),fields(%s)" % (filename, " ".join(headers), line)
            for i in range(len(fields)):
                assert headers[i] in dataframe, "col %s not initialized in file %s" % (headers[i], filename)
                dataframe[headers[i]].append(fields[i])
    return dataframe


def merge_csv(csv_list):
    merged_csv = {}
    for csv in csv_list:
        for k in csv:
            if k in merged_csv:
                merged_csv[k].extend(csv[k])
            else:
                merged_csv[k] = csv[k]
    return merged_csv


def convert_to_csv_str(csv):
    csv_str = ""
    for k in csv:
        csv_str += k + ","
    csv_str = csv_str.strip(",") + "\n"
    for irow in range(len(csv.values()[0])):
        for k in csv:
            csv_str += csv[k][irow] + ','
        csv_str = csv_str.rstrip(",") + "\n"

    return csv_str


def create_csv():
    all_csv = get_all_csv()
    csv_str = convert_to_csv_str(all_csv)
    filepath = '/Users/houhualong/Developer/src/github/datamining_homework/score_analysis/scores/scores.noid.csv'
    if os.path.exists(filepath):
        os.remove(filepath)
    f = open(filepath, 'w')
    f.write(csv_str)


def write_id():
    filepath = '/Users/houhualong/Developer/src/github/datamining_homework/score_analysis/scores/scores.noid.csv'
    newfilepath = '/Users/houhualong/Developer/src/github/datamining_homework/score_analysis/scores/scores.csv'
    with open(filepath) as f:
        f.readline()  # skip header
        nameid = {}
        for line in f.readlines():
            fields = line.split(',')
            if (fields[1] in nameid) and (nameid[fields[1]] is not None and nameid[fields[1]] != ""):
                continue
            nameid[fields[1]] = fields[8]  # name=id

        f.seek(0)
        if os.path.exists(newfilepath):
            os.remove(newfilepath)
        with open(newfilepath, 'w') as newfile:
            newfile.write(f.readline())  # write header line
            for line in f.readlines():
                orig_fields = [field.strip() for field in line.split(',')]
                orig_fields[8] = nameid[orig_fields[1]]
                newline = ",".join(orig_fields) + "\n"
                newfile.write(newline)


def testid():
    filepath = '/Users/houhualong/Developer/src/github/datamining_homework/score_analysis/scores/scores.csv'
    with open(filepath) as f:
        f.readline()
        idname = {}
        for line in f.readlines():
            fields = [field.strip() for field in line.split(',')]
            if fields[8] in idname:
                assert idname[fields[8]] == fields[1], "%s!=%s" % (idname[fields[8]], fields[1])


def main():
    create_csv()
    write_id()
    testid()


if __name__ == "__main__":
    main()

import json, os, csv, re
with open('./items.json', 'w') as json_data:
    with open('./final_df.csv', 'r') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        for row in csv_reader:
            """
            {
                "id": 39712, 
                "desc": "e need to confirm this bug with Microsoft.", 
                "blocked": [], 
                "dependson": [], 
                "assigned": "Wan-Teh Chang", 
                "reporter": "Wan-Teh Chang", 
                "duplicates": []
            }
            """
            _data = {
                "id": int(row[0]),
                "desc": row[1],
                "blocked": [int(i) for _id in row[9].split(',')
                            for i in re.findall(r"^\d+$", _id.strip().replace("\n", ""))],
                "dependson": [int(i) for _id in row[8].split(',')
                              for i in re.findall(r"^\d+$", _id.strip().replace("\n", ""))],
                "assigned": row[2].strip().replace("\n", ""),
                "reporter": row[3].strip().replace("\n", ""),
                "duplicates": [],
                "cc": row[4].strip().replace("\n", ""),
                "platform": row[6].strip().replace("\n", ""),
                "sys": row[7].strip().replace("\n", ""),
                "creation_ts": row[11].strip().replace("\n", ""),
                "modified": row[12].strip().replace("\n", ""),
                "commname": row[13].strip().replace("\n", "")
            }
            json_data.write(json.dumps(_data)+'\n')

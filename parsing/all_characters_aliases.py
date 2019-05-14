import json

import pandas as pd

from aliases_parser import parse_character

character_links_dataframe = pd.read_csv('characters_dataset.csv')


def create_big_dataset(df):
    dataset = []
    i = 1
    for row in df.itertuples():
        data = parse_character(getattr(row, '_2').strip(), getattr(row, 'name'))
        print(data)
        if data is not None:
            dataset.append(json.loads(data))
        print("Progress: {}%".format((i / 2055) * 100))
        i += 1
    return json.dumps(dataset, separators=(",\n", ": "))


with open("example_better.json", "w") as file:
    file.write(create_big_dataset(character_links_dataframe))

import pandas as pd

topic_info = pd.read_csv("../outputs/bertopic_topics.csv")

for topic_id in [76, 179, 277, 42, 63]:
    row = topic_info[topic_info["Topic"] == topic_id]
    if len(row) > 0:
        print(f"Topic {topic_id}:")
        print(f"  Name: {row['Name'].values[0]}")
        print(f"  Count: {row['Count'].values[0]}")
        print(f"  Representation: {row['Representation'].values[0]}")
        print()
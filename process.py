import pandas as pd
import sqlite3

# Read csv file.
df = pd.read_csv("recipe.csv")

# Connect to (create) database.
database = "db.sqlite3"
conn = sqlite3.connect(database)
dtype={
    "rc_num" : "IntegerField",
    "rc_name" : "CharField",
    "rc_view" : "CharField",
    "rc_rec" : "CharField",
    "rc_scrap" : "CharField",
    "rc_type" : "CharField",
    "rc_sit" : "CharField",
    "rc_sort" : "CharField",
    "rc_nick" : "CharField",
    "rc_info" : "CharField",
    "rc_ing" : "CharField",
    "rc_diff" : "CharField",
    "rc_time" : "CharField",
}
df.to_sql(name='ingredients_recipelist', con=conn, if_exists='replace', dtype=dtype, index=True, index_label="id")
conn.close()
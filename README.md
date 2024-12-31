# What is Not-Pandas?

Not-Pandas is a minimal pandas-style DataFrame to be used when disk space is limited,
and you don't need the full feature set of pandas (charts, statistical toolbox, database
connections etc.). Some functions, methods and logic has been mirrored with a subset of
parameters, two differences to pandas are that datatypes are not kept and NaN is not
supported, we use None.


# Quickstart

Loading data into a DataFrame is as simple as

```python
from not_pandas import DataFrame


df = DataFrame(
    [
        {"row": 1, "col_a": "abc", "col_b": 123},
        {"row": 2, "col_a": "def", "col_b": 456},
        {"row": 3, "col_a": "hij", "col_b": 789},
        {"row": 4, "col_a": "abc", "col_b": 999},
    ]
)
```

Just like pandas, you can perform various aggregations and filters

```python
df[df["col_a"]=="abc"].sum()
# ---
# 1122
# ---

df[df["col_b"].isin([123, 456])].len()
# ---
# 2
# ---
```

You can add and update columns

```python
df["col_c"] = 2
df["col_a"] = df["col_c"] * 5

print(df)

# ---
#   row    col_a    col_b    col_c
# -----  -------  -------  -------
#     1       10      123        2
#     2       10      456        2
#     3       10      789        2
#     4       10      999        2
# ---
```
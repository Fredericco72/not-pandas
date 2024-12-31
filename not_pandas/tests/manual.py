from not_pandas import DataFrame
from not_pandas.tests.datasets import dataset_1


def print_line(*, n=2, length=120):
    for _ in range(n):
        print("-" * length)


df = DataFrame(dataset_1)
print("Print DataFrame")
print(df)
print_line()


print("Select a Series")
print(df["col_a"])
print_line()


print("Compare a Series (Not Equal)")
print(df["col_a"] != 123)
print_line()


print("Compare a Series (Greater Than)")
print(df["col_a"] > 200)
print_line()


print("Select Rows using a Series Comparison (Less Than)")
print(df[df["col_a"] < 200])
print_line()


print("Sum a Series")
print(df["col_a"].sum())
print_line()


print("Print Columns")
print(df.columns())
print_line()


print("Add Series")
print(df["col_a"] + df["col_b"])
print_line()


print("Multiply Series")
print(df["col_a"] * 5)
print_line()


print("Group by")
print_line(n=1, length=80)
for group, data in df.groupby(["col_a", "col_b"]):
    print("Group:", group)
    print(f"DataFrame:\n{data}")
    print_line(n=1, length=80)
print_line()


print("Group by Aggregate")
print('| Equivalent to pandas: df.groupby("col_a")["col_b"].sum()')
print(df.groupby_agg(["col_a"], "col_b", sum))
print_line()


print("Rank")
print(df["col_b"].rank())
print_line()


print("Add a Column (static value)")
df["col_new_static"] = 1
print(df)
print_line()


print("Add a Column (from Series)")
df["col_new_series"] = df["col_b"].rank()
print(df)
print_line()


print("Rename Column (dict)")
print(df.rename(columns={"col_new_series": "col_rank"}))
print_line()


print("Rename Column (function)")
print(df.rename(columns=lambda x: x + "_suffix"))
print_line()


print("Head")
print(df.head(2))
print_line()


print("Sort Values")
print(df.sort_values("col_b"))
print_line(n=1, length=80)
print(df.sort_values("col_b", ascending=False))
print_line()

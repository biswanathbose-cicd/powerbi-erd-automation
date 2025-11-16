import os
from collections import defaultdict
import pandas as pd
from sanitize_utils import sanitize_attr, sanitize_type
from pk_fk_detection import is_primary_key, detect_relationship_sides

DATA_DIR = "data"
OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)

tables = pd.read_csv(os.path.join(DATA_DIR, "Tables.csv"))
columns = pd.read_csv(os.path.join(DATA_DIR, "Columns.csv"))
relationships = pd.read_csv(os.path.join(DATA_DIR, "Relationships.csv"))

t_id_key = "ID"
t_name_key = "Name"

c_id_key = "ID"
c_table_name_key = "Table" if "Table" in columns.columns else None
c_tableid_key = "TableID" if "TableID" in columns.columns else None
c_name_key = "Name"
c_dtype_key = "DataType" if "DataType" in columns.columns else None
is_key_key = "IsKey" if "IsKey" in columns.columns else None
is_unique_key = "IsUnique" if "IsUnique" in columns.columns else None
is_nullable_key = "IsNullable" if "IsNullable" in columns.columns else None

from_colid_key = "FromColumnID"
to_colid_key = "ToColumnID"
from_card_key = "FromCardinality" if "FromCardinality" in relationships.columns else None
to_card_key = "ToCardinality" if "ToCardinality" in relationships.columns else None

table_name_by_id = {row[t_id_key]: row[t_name_key] for _, row in tables.iterrows()}

cols_by_table = defaultdict(list)
col_by_id = {}

for _, col in columns.iterrows():
    tname = None
    if c_table_name_key and col.get(c_table_name_key):
        tname = col.get(c_table_name_key)
    elif c_tableid_key and col.get(c_tableid_key):
        tname = table_name_by_id.get(col.get(c_tableid_key))

    if not tname:
        continue

    clean_name = sanitize_attr(col.get(c_name_key))
    dtype_raw = col.get(c_dtype_key) if c_dtype_key else "string"
    dtype = sanitize_type(dtype_raw)

    pk = is_primary_key(col, is_key_key, is_unique_key, is_nullable_key)

    cols_by_table[tname].append({
        "name": clean_name,
        "dtype": dtype,
        "pk": pk,
        "fk": False
    })

    col_by_id[col.get(c_id_key)] = (tname, clean_name)

pk_candidates = defaultdict(set)
fk_candidates = defaultdict(set)
rels_out = []

for _, rel in relationships.iterrows():
    from_colid = rel.get(from_colid_key)
    to_colid = rel.get(to_colid_key)

    from_table, from_col = col_by_id.get(from_colid, (None, None))
    to_table, to_col = col_by_id.get(to_colid, (None, None))

    if not from_table or not to_table:
        continue

    left_card, right_card = detect_relationship_sides(rel, from_card_key, to_card_key)

    if right_card == "||":
        pk_candidates[to_table].add(to_col)
        fk_candidates[from_table].add(from_col)

    rels_out.append((from_table, left_card, right_card, to_table))

for tname, cols in cols_by_table.items():
    for c in cols:
        if c["name"] in pk_candidates.get(tname, set()):
            c["pk"] = True
        if c["name"] in fk_candidates.get(tname, set()):
            c["fk"] = True

lines = ["erDiagram", ""]

for ftable, lcard, rcard, ttable in rels_out:
    lines.append(f"    {sanitize_attr(ftable)} {lcard}--{rcard} {sanitize_attr(ttable)} : relates")

lines.append("")

for tname, cols in cols_by_table.items():
    safe_t = sanitize_attr(tname)
    lines.append(f"    {safe_t} {{")
    for c in cols:
        tags = []
        if c["pk"]: tags.append("PK")
        if c["fk"]: tags.append("FK")
        suffix = " " + " ".join(tags) if tags else ""
        lines.append(f"        {c['dtype']} {c['name']}{suffix}")
    lines.append("    }")
    lines.append("")

os.makedirs(OUT_DIR, exist_ok=True)
out_path = os.path.join(OUT_DIR, "model.mmd")
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Mermaid ER Diagram generated at: {out_path}")

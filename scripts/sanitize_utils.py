import re

def sanitize_attr(name: str, maxlen: int = 80) -> str:
    if name is None:
        return ""
    s = str(name).strip()
    s = re.sub(r"[^\w]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    if s and s[0].isdigit():
        s = "_" + s
    return s[:maxlen] or "col_"

def sanitize_type(dtype: str) -> str:
    if dtype is None:
        return "string"
    t = re.sub(r"\W+", "", str(dtype))
    return t or "string"

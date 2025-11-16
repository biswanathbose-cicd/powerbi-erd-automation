def is_primary_key(column_row, is_key_key, is_unique_key, is_nullable_key):
    val = lambda k: str(column_row.get(k)).strip().lower() if k in column_row else ""
    if is_key_key and val(is_key_key) == "true":
        return True
    if is_unique_key and is_nullable_key:
        return val(is_unique_key) == "true" and val(is_nullable_key) == "false"
    return False

def detect_relationship_sides(row, from_card_key, to_card_key):
    from_card = row.get(from_card_key) if from_card_key in row else None
    to_card = row.get(to_card_key) if to_card_key in row else None
    if not from_card and not to_card:
        return "o{", "||"
    return from_card or "o{", to_card or "||"

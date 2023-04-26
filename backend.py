from query_builder import build_query

def main(code, code_extension, fewShot="no"):
    if fewShot == "yes":
        message = build_query(code, 3, "fewShot")
    else:
        message = build_query(code)

    return message
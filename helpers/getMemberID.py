from helpers.extractstring import extract_string


def getMemberID(people: str):
    return int(extract_string(people, s="!", e=">")) \
        if (people[2] == "!" and people[-1:] == ">") else int(extract_string(people, s="@", e=">")) \
        if (extract_string(people, s="!", e=">") == "") else 0

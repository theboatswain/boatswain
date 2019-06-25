def getSimpleName(name: str):
    parts = name.split('-')
    max_characters = 3
    result = []
    for item in parts:
        result.append(item[0].upper())
        if len(result) >= max_characters:
            break
    return ''.join(result)

def capitalize_title(title):
    lowercase_words = {'and', 'in', 'the', 'of', 'a', 'an', 'to', 'with', 'for', 'on', 'at', 'by', 'from', 'via', 'as', 'into', 'onto', 'upon', 'but', 'nor', 'or', 'so'}
    words = title.split()
    capitalized_words = [word.capitalize() if word.lower() not in lowercase_words else word.lower() for word in words]
    capitalized_words[0] = capitalized_words[0].capitalize()  # Always capitalize the first word
    return ' '.join(capitalized_words)
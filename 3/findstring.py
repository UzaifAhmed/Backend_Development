def ispresent(person):
    names = ['Al', 'Bo', 'Chi', 'Go']
    return True if person in names else False

def nodigit(person):
    return True if person.isalpha() else False
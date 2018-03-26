letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
offset = 0

def get_letter_position(letter):
    position = 0
    try:
        position = (letters.index(letter))
    except:
        pass
    return position + offset
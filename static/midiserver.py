import mido

with mido.open_input('virtualport', virtual=True) as inport:
     for message in inport:
        print(message)
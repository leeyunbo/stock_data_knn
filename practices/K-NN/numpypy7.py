def debounce(last):
    current = last
    if last!=current:
        current = last
    return current

lastButton = False
currentButton = debounce(lastButton)


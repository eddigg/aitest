def turn_on_lights():
    print("Lights turned on")

def turn_off_lights():
    print("Lights turned off")

def play_music():
    print("Music playing")

def stop_music():
    print("Music stopped")

action_map = {
    "turn_on_lights": turn_on_lights,
    "turn_off_lights": turn_off_lights,
    "play_music": play_music,
    "stop_music": stop_music
}

def get_action(intent: str):
    return action_map.get(intent)
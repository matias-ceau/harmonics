from mido import MidiFile
import pygame
#from midiutil import MIDIFile as MidiWrite

def play_music(music_file):
    """
    https://gist.github.com/guitarmanvt/3b6a91cefb2f5c3098ed
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    """
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
        print("Music file %s loaded!" % music_file)
    except pygame.error:
        print("File %s not found! (%s)" % (music_file, pygame.get_error()))
        return
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(30)
from ..data.drums import quick_gm
import mido, rtmidi
import random, time

def read_file(path):
    with open(path) as f:
        lines = f.readlines()
        lines = [i[:-1] for i in lines]
        instruments = {}
        for li in lines:
            if li[0] in quick_gm.keys():
                line = li[2:].replace(' ','')
                spec = [i for i in set(line) if i != '-']
                print(spec)
                dic = quick_gm[li[0]]
                spec_midi = [dic.get(i) if i in dic.keys() else random.choice(list(dic.values())) for i in spec]
                for sp,spm in zip(spec, spec_midi):
                    instruments[spm] = []
                    for n in line:
                        if n == sp:
                            instruments[spm].append(1)
                        else:
                            instruments[spm].append(0)
        print(instruments)
        # to change
        midiout = rtmidi.MidiOut()
        midiout.open_port(0)
        # send midi
        counter = 0
        while True:
            counter += 1
            for k,v in instruments.items():
                index = counter%len(v)
                if v[index] == 1:
                    midiout.send_message(
                            mido.Message('note_on',
                                         channel=9,
                                         note=k,
                                         velocity=random.choice(range(70,90))).bin()
                            )

            time.sleep(0.125)



                


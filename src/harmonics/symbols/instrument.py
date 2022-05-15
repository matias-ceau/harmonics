class Instrument():
    """Mainly a property of a part."""

    def __init__(self,
                 name=None,
                 channel=None,
                 bank=None,
                 instrument_type=None):
        self.name = name
        self.channel = channel
        self.bank = bank
        self.instrument_type = instrument_type

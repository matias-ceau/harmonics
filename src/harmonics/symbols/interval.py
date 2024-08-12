from ..data.intervals import IDICT, INAMES, INTERVALS, EDICT


class Interval:
    """Encapsulates the concept of an interval."""

    def __init__(self, name):
        if isinstance(name, Interval):
            self.__dict__.update(vars(name))
            return
        else:
            if name in INAMES:
                self.name = name
                self.distance = IDICT[name]
                if int(self.name.split("b")[-1].split("#")[-1]) > 7:
                    self.distance += 12
            else:
                if type(name) in [tuple, list]:
                    if len(name) == 2 and type(name[0]) == Note:
                        self.distance = name[1].midi - name[0].midi
                else:
                    self.distance = name
                candidates = [a for a, b in IDICT.items() if b == self.distance % 12]
                if self.distance > 12:
                    candidates = [c for c in candidates if EDICT[c] in (1, 2)]
                elif self.distance < 12:
                    candidates = [c for c in candidates if EDICT[c] in (0, 2)]
                self.name = candidates[0]
            self.other_names = [a for a, b in IDICT.items() if b == self.distance % 12]
            for a in INTERVALS.keys():
                self._detect(a)
            self.octave = self.distance // 12

    def _detect(self, class_attribute):
        if type(INTERVALS[class_attribute][0]) == str:
            attribute = self.name
        else:
            attribute = self.distance
        if attribute in INTERVALS[class_attribute]:
            self.__dict__[class_attribute.lower()] = True
        else:
            self.__dict__[class_attribute.lower()] = False

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __eq__(self, interval):
        if isinstance(interval, Interval):
            return self.distance == interval.distance
        elif type(interval) == str:
            return self.distance == Interval(str)
        else:
            return self.distance == interval

    def __add__(self, interval):
        if type(interval) == Interval:
            return Interval(self.distance + interval.distance)
        elif type(interval) == int:
            return Interval(self.distance + interval)

    def __sub__(self, interval):
        if type(interval) == Interval:
            return Interval((self.distance - interval.distance) % 12)
        elif type(interval) == int:
            return Interval((self.distance - interval) % 12)

    def __invert__(self):
        if self.distance < 0:
            return Interval(abs(self.distance - 12) % 12)
        if self.distance > 0:
            return Interval(abs(self.distance + 12) % 12)
        if self.distance == 0:
            return Interval(0)

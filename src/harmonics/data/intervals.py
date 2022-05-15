INAMES = [
    "1",
    "b2",
    "b9",
    "9",
    "2",
    "#9",
    "b3",
    "3",
    "4",
    "11",
    "#4",
    "#11",
    "b5",
    "5",
    "b6",
    "b13",
    "6",
    "13",
    "b7",
    "7",
]
EXTENSION = [2, 0, 1, 1, 0, 1, 0, 2, 0, 1, 0, 1, 0, 2, 0, 1, 0, 1, 2, 2]
IDIST = [0, 1, 1, 2, 2, 3, 3, 4, 5, 5, 6, 6, 6, 7, 8, 8, 9, 9, 10, 11]

IDICT = {k: v for k, v in zip(INAMES, IDIST)}
EDICT = {k: v for k, v in zip(INAMES, EXTENSION)}

INTERVALS = {
    'APPROACH': ["b3", "3", "b7", "7"],
    'EXTENSION': ["b9", "#9", "11", "#11", "b13", "13"],
    'MINOR': ["b2", "b3", "b6", "b7"],
    'MAJOR': ["3", "6", "7"],
    'SUS': ["2", "4"],
    'TRITONE': ["6"],
    'ROOT': ["1"],
    'SECOND': ["b2", "2"],
    'THIRD': ["b3", "3"],
    'FOURTH': ["4", "#4"],
    'FIFTH': ["b5", "5"],
    'SIXTH': ["b6", "6"],
    'SEVENTH': ["b7", "7"],
}

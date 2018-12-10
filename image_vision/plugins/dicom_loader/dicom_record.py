from enum import Enum


class DicomRecordType(Enum):
    DIR = 1
    PATIENT = 2
    STUDY = 3
    SERIES = 4
    IMAGE = 5


class DicomRecord:
    def __init__(self, record_type, record_id, dataset=None):
        self.type = record_type
        self.id = record_id
        self.dataset = dataset
        self.children = {}  # { id: DicomRecord }

    def __str__(self, level=0):
        s = '\t' * level + repr(self.id) + '\n'
        for child_record in self.children.values():
            s += child_record.__str__(level + 1)
        return s


class DicomDir(DicomRecord):
    def __init__(self, path):
        super().__init__(DicomRecordType.DIR, path)

        self.path = path


class DicomPatient(DicomRecord):
    def __init__(self, record_id, dataset=None):
        super().__init__(DicomRecordType.PATIENT, record_id, dataset)


class DicomStudy(DicomRecord):
    def __init__(self, record_id, dataset=None):
        super().__init__(DicomRecordType.STUDY, record_id, dataset)


class DicomSeries(DicomRecord):
    def __init__(self, record_id, dataset=None):
        super().__init__(DicomRecordType.SERIES, record_id, dataset)


class DicomImage(DicomRecord):
    def __init__(self, record_id, dataset=None):
        super().__init__(DicomRecordType.IMAGE, record_id, dataset)

class DummyVisitSchedule:
    def __init__(self):
        self.schedules = {}
        self.visit_model = 'edc_reference.subjectvisit'


class Panel:
    def __init__(self, name):
        self.name = name


class Crf:
    def __init__(self):
        self.model = 'edc_reference.crfone'


class Requisition:
    def __init__(self):
        self.model = 'edc_reference.subjectrequisition'
        self.panel = Panel(name='cd4')


class DummyVisit:
    def __init__(self):
        self.crfs = [Crf()]
        self.requisitions = [Requisition()]


class DummySchedule:
    def __init__(self):
        self.enrollment_model = 'edc_reference.enrollment'
        self.disenrollment_model = 'edc_reference.disenrollment'
        self.visits = dict(visit=DummyVisit())


class DummySite:
    def __init__(self):
        self.registry = {}

    def autodiscover(self, *args, **kwargs):
        pass

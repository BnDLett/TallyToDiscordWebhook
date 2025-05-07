from Field import Field
from datetime import datetime


class ApplicationResponse:
    creation_time: datetime
    submission_id: str
    form_id: str
    form_name: str

    fields: list[Field]

    def __init__(self, creation_time: datetime, submission_id: str, form_id: str, form_name: str, fields: list[Field]):
        self.creation_time = creation_time
        self.submission_id = submission_id
        self.form_id = form_id
        self.form_name = form_name

        self.fields = fields

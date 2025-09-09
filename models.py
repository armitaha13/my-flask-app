# models.py

class Service:
    """
    Represents a dental service from the 'services' table.
    Each instance of this class corresponds to a row in the services table.
    """
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f"ID: {self.id}, Service: {self.name}"


class Appointment:
    """
    Represents a patient appointment from the 'appointments' table.
    Each instance of this class corresponds to a row in the appointments table.
    """
    def __init__(self, id, patient_name, patient_phone, patient_nationalCode,
                 appointment_date, appointment_time, service_id, descriptions=None, refrences=None):
        self.id = id
        self.patient_name = patient_name
        self.patient_phone = patient_phone
        self.patient_nationalCode = patient_nationalCode
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.service_id = service_id
        self.descriptions = descriptions
        self.refrences = refrences

    def __str__(self):
        return (f"Appointment ID: {self.id}\n"
                f"  Patient: {self.patient_name}\n"
                f"  Phone: {self.patient_phone}\n"
                f"  Date: {self.appointment_date}\n"
                f"  Time: {self.appointment_time}\n"
                f"  Service ID: {self.service_id}\n"
                f"--------------------")
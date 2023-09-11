from db import session, Appointments


"""

The appointments are always from 10:00 a.m. to 3:00 p.m. 
<<<<<<< HEAD
You can process 4 donors every quarter. -> 16 donors per hour -> 50 donors per appointment
=======
You can process 4 donors every quarter. -> 16 donaters per hour -> 50 donators per appointment
>>>>>>> 499fe1c (add appointments)

"""


class Appointment:
    def __init__(self, date, time):
        self.date = date
        self.time = time

    @staticmethod
    def get_all():
        appointment = session.query(Appointments).all()
        if not appointment:
            return None

        return appointment

    @staticmethod
<<<<<<< HEAD
    def get_one(date, time):
        appointment = session.query(Appointments).filter(Appointments.date == date, Appointments.time == time).first()
=======
    def get_one(time):
        appointment = session.query(Appointments).filter(Appointments.time == time).first()
>>>>>>> 499fe1c (add appointments)
        if not appointment:
            return None

        return appointment

    @staticmethod
<<<<<<< HEAD
    def get_appointment(date):
        dates = []
        appointments = session.query(Appointments).filter(Appointments.date == date).all()
=======
    def get_dates():
        dates = []
        appointments = session.query(Appointments).all()
>>>>>>> 499fe1c (add appointments)
        for appointment in appointments:
            if appointment.date not in dates:
                dates.append(appointment.date)

        return dates

    @staticmethod
    def add_appointment(date):
        if not session.query(Appointments).filter(Appointments.date == date).first():
            time = 945
            while time < 1500:
                if time % 100 == 45:  # get the last two digits of the current time to check if it is quater to
                    time += 55  # first subtract 45 then add 100 to get the next full hour
                else:
                    time += 15  # go to the next quarter
                termin = Termin(date=date, time=time)
                session.add(termin)
            session.commit()
<<<<<<< HEAD

    @staticmethod
    def delete_appointment(date):
        appointments = session.query(Appointments).filter(Appointments.date == date).all()
        if appointments:
            for appointment in appointments:
                session.delete(appointment)
            session.commit()

    @staticmethod
    def reset_time(date, time):
        appointment = session.query(Appointments).filter(Appointments.date == date, Appointments.time == time).first()
        if not appointment:
            return None

        return appointment


=======
>>>>>>> 499fe1c (add appointments)

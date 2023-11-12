from db import session, Appointments, Doners

"""

The appointments are always from 10:00 a.m. to 3:00 p.m. 
You can process 4 donors every quarter. -> 16 donors per hour -> 80 donors per appointment

The from for the dates is following: "DD-MM-YYYY"

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
    def get_one(date, time):
        appointment = (session.query(Appointments).filter(Appointments.date == date, Appointments.time == time)
                       .first())
        if not appointment:
            return None

        return appointment

    @staticmethod
    def get_appointment(date):
        appointments = session.query(Appointments).filter(Appointments.date == date).all()
        return appointments

    @staticmethod
    def get_dates(open_appointment=False):
        if not open_appointment:
            dates = []
            appointments = session.query(Appointments).all()

            for appointment in appointments:
                if appointment.date not in dates:
                    dates.append(appointment.date)

            return dates

        if open_appointment:
            pass

    @staticmethod
    def add_appointment(date):
        if not session.query(Appointments).filter(Appointments.date == date).first():
            time = 945
            while time < 1500:
                if time % 100 == 45:  # get the last two digits of the current time to check if it is quater to
                    time += 55  # first subtract 45 then add 100 to get the next full hour
                else:
                    time += 15  # go to the next quarter
                appointment = Appointments(date=date, time=str(time))
                session.add(appointment)
            session.commit()

    @staticmethod
    def delete_appointment(date):
        appointments = session.query(Appointments).filter(Appointments.date == date).all()
        if appointments:
            for appointment in appointments:
                session.delete(appointment)
            session.commit()

    @staticmethod
    def reset_time(date, time):
        appointment = (session.query(Appointments).filter(Appointments.date == date, Appointments.time == str(time))
                       .first())
        if not appointment:
            return None

        appointment.delete()
        new_appointment = Appointment(
            date == appointment.date,
            time == appointment.time,
        )
        session.add(new_appointment)
        session.commit()
        return appointment

    @staticmethod
    def free_slots(date, time):
        slot = session.query(Appointments).filter(Appointments.time == str(time),
                                                  Appointments.date == date).first()
        return slot.left_slots

    @staticmethod
    def add_doner(date, time, doner_id):
        slot = session.query(Appointments).filter(Appointments.time == time,
                                                  Appointments.date == date).first()

        doner = session.query(Doners).filter(Doners.user_id == doner_id).first()

        if doner.appointment:
            return

        if slot.left_slots == 0:
            return

        elif slot.left_slots == 4:
            slot.doner1 = doner_id

        elif slot.left_slots == 3:
            slot.doner2 = doner_id

        elif slot.left_slots == 2:
            slot.doner3 = doner_id

        elif slot.left_slots == 1:
            slot.doner4 = doner_id

        slot.left_slots -= 1

        doner.appointment = True
        session.commit()

from sqlalchemy import Engine, select , desc , func
from sqlalchemy.orm import Session

from .models import Service, Category, LastWork ,Appointment, create_tables
from .engine import ENGINE
from datetime import date , datetime

class DBManager:

    def __init__(self, engine: Engine):
        self.engine = engine
        create_tables(self.engine)

    def get_all_categories(self):
        with Session(self.engine) as session:
            categories = select(Category)
            categories = session.scalars(categories).all()
        
        return categories
    
    def get_services_by_category(self, category_id):
        with Session(self.engine) as session:
            services = select(Service).filter(Service.category_id==category_id)
            services = session.scalars(services).all()
        
        return services
    
    def get_service(self, service_id):
        with Session(self.engine) as session:
            service = select(Service).filter(Service.id==service_id)
            service = session.scalar(service)
        
        return service
    

    def get_last_works(self):
        with Session(self.engine) as session:
            works = select(LastWork).order_by(LastWork.date)
            works = session.scalars(works).all()

        return works
    

    def insert_work(self, path):
        with open(path, "rb") as file:
            data = file.read()
            with Session(self.engine) as session:
                session.add(
                    LastWork(
                        image = data
                    )
                )
                session.commit()
    def insert_work_bytes(self,byte_code):
         with Session(self.engine) as session:
                session.add(
                    LastWork(
                        image = byte_code
                    )
                )
                session.commit()


    def delete_work(self, work_id):
        with Session(self.engine) as session:
            work=select(LastWork).filter(LastWork.id==work_id)
            work=session.scalar(work)
            session.delete(work)
            session.comit()


    def insert_appointment(self,data):
        del data["state"]
        with Session(self.engine) as session:
            session.add(
                Appointment(**data)
            )
            session.commit()

    def get_all_services(self):
        with Session(self.engine) as session:
            services=select(Service)
            services=session.scalars(services).all()
        return services
    

    def delete_services(self,service_id):
        with Session(self.engine) as session:
            service=self.get_service(service_id=service_id)
            session.delete(service)
            session.commit()

    def insert_service(self, data):
        with Session(self.engine ) as session:
            session.add(
                Service(
                **data
                )
            )
    
        session.commit()


    def get_appointments(self):
        with Session(self.engine ) as session:
            appointments=select(Appointment).filter(func.date(Appointment.time)==date.today()).order_by(desc(Appointment.time))
            appointments=session.scalars(appointments).all()

        return appointments
    def get_apoointment(self, appointment_id):
        with Session(self.engine) as session:
            appointment=select(Appointment).filter(Appointment.id==appointment_id)
            appointment=session.scalar(appointment)

        return appointment
    
    def delete_appointment(self,appointment_id):
        with Session(self.engine ) as session:
            appointment=select(Appointment).filter(Appointment.id==appointment_id)
            appointment=session.scalar(appointment)
            session.delete(appointment)
            session.comit()
            
    
MANAGER=DBManager(engine=ENGINE)



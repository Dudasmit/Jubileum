import sys  
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float 
  
from sqlalchemy.orm import declarative_base  
  
from sqlalchemy.orm import relationship  
  
from sqlalchemy import create_engine  


Base = declarative_base()  

engine = create_engine('sqlite:///company_anniversary.db')


#Base.metadata.drop_all(engine)  
  



class Company_anniversary(Base):  
    __tablename__ = 'company_anniversary'  
    
    KvKNumber = Column('KvK Number', Integer, primary_key=True)  
    CompanyName = Column('Company Name',String(250), nullable=False)  
    Street = Column('Street',String(250), nullable=False)  
    HouseNumber = Column('House Number',String(15), nullable=False)  
    PostalCode = Column('Postal Code',String(250), nullable=False)  
    City = Column('City',String(250), nullable=False)  
    PhoneNumber = Column('Phone Number',String(250), nullable=False)  
    EmployeeCount = Column('Employee Count',String(250), nullable=False)  
    RegistrationDate = Column('Registration Date',Date, nullable=False)  
    BrancheType = Column('Branche Type',String(250), nullable=False)  
    BrancheCode = Column('Branche Code',String(250), nullable=False)  
    BrancheDescription = Column('Branche Description',String(250), nullable=False)  
    StatusCompany = Column('Status Company',String(250), nullable=False)  
    lat = Column(Float, nullable=False)  
    lon = Column(Float, nullable=False)  

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'KvKNumber': self.KvKNumber,
            'CompanyName': self.CompanyName,
            'Street': self.Street,
            'HouseNumber': self.HouseNumber,
            'PostalCode': self.PostalCode,
            'City': self.City,
            'PhoneNumber': self.PhoneNumber,
            'EmployeeCount': self.EmployeeCount,
            'RegistrationDate': self.RegistrationDate,
            'BrancheType': self.BrancheType,
            'BrancheCode': self.BrancheCode,
            'BrancheDescription': self.BrancheDescription,
            'StatusCompany': self.StatusCompany,
            'lat': self.lat,
            'lon': self.lon,
        }

class Anniversaries(Base):
    __tablename__ = 'Anniversaries'
    id = Column(Integer, primary_key=True)
    KvKNumber = Column('KvK Number', Integer, ForeignKey("company_anniversary.KvK Number"))  
    AnniversaryDay = Column('Anniversary Day',Date, nullable=False)  
    Anniversary    = Column('Anniversary',Integer, nullable=False)
    company_anniversary = relationship(Company_anniversary)
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'KvKNumber': self.KvKNumber,
            'AnniversaryDay': self.AnniversaryDay,
            'Anniversary': self.Anniversary,
        }
  




Base.metadata.create_all(engine)

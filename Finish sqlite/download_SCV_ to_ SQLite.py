from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from database_setup import Company_anniversary, Anniversaries, Base
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta

engine = create_engine('sqlite:///company_anniversary.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

List_of_columns = ['KvK Number', 'Company Name', 'Street',
       'House Number', 'Postal Code', 'City', 'Phone Number', 'Employee Count',
       'Registration Date', 'Branche Type', 'Branche Code',
       'Branche Description', 'Status Company', 'lat', 'lon']


df_Company = pd.read_csv('Companies Data_.csv')
df_Company['Registration Date'] = pd.to_datetime(df_Company['Registration Date'], format='%d/%m/%Y', errors='coerce').dt.date
df_Company.dropna(subset=['Registration Date'], inplace=True)
df_Company.fillna(0, inplace=True)


for i, row in df_Company[List_of_columns].iterrows():

    Company_anniversary_ = Company_anniversary(KvKNumber = row['KvK Number'], CompanyName = row['Company Name'], 
        Street = row['Street'], HouseNumber = row['House Number'], PostalCode = row['Postal Code'], City = row['City'],
        PhoneNumber = row['Phone Number'], EmployeeCount = row['Employee Count'],
        RegistrationDate = row['Registration Date'],
        BrancheType = row['Branche Type'],
        BrancheCode = row['Branche Code'], BrancheDescription = row['Branche Description'], StatusCompany = row['Status Company'],
        lat = row['lat'], lon = row['lon'])

    session.add(Company_anniversary_)
    
session.commit()



def days_until_anniversary(registration_date,value):
    #print(registration_date)
    today = pd.Timestamp('today')
    anniversary_date = pd.Timestamp(registration_date.year + value, registration_date.month, registration_date.day)
    '''
    if anniversary_date < today:
        return date(1, 1, 1)
        while anniversary_date < today:
            anniversary_date = pd.Timestamp(anniversary_date.year + value, anniversary_date.month, anniversary_date.day)
    delta = anniversary_date - today
    '''
    return datetime.date(anniversary_date)

list_years=[1,5,10,15,20,25]



for years in list_years:
    df_Company['Anniversary Day'] = df_Company['Registration Date'].apply(days_until_anniversary,args = ([years]))
    
    for i, row in df_Company.iterrows():
        Anniversaries_ = Anniversaries(KvKNumber = row['KvK Number'],
            AnniversaryDay = row['Anniversary Day'],
            Anniversary = years)

        session.add(Anniversaries_)

    session.commit()
    

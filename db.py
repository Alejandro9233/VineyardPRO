import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import datetime as dt
import pytz
import pandas as pd
import meteomatics.api as api


load_dotenv()

host=os.getenv("DATABASE_HOST")
user=os.getenv("DATABASE_USERNAME")
passwd=os.getenv("DATABASE_PASSWORD")
db=os.getenv("DATABASE")
db_key = f"mysql+pymysql://{user}:{passwd}@{host}/{db}?charset=utf8mb4"

engine = create_engine(
    db_key,
    connect_args={
        "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    }
)


def load_hectares_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from Hectare"))
        result_all = result.fetchall()
        projects = []
        for row in result_all:
            my_dict = {
                'id': row[0],
                'temperature': row[1],
                'sprinkler': row[2],
                'light': row[3],
                'ceiling': row[4],
                'timeStamp': row[5],
            }
            projects.append(my_dict)
        return projects

def load_users_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from Usuarios"))
        result_all = result.fetchall()
        projects = []
        for row in result_all:
            my_dict = {
                'id': row[0],
                'name': row[1].upper(),
                'vineyards': row[2],
            }
            projects.append(my_dict)
        return projects
    

def load_vineyards_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from vineyards"))
        result_all = result.fetchall()
        projects = []
        for row in result_all:
            my_dict = {
                'id': row[0],
                'name': row[1].upper(),
                'imgURL': row[2],
                'hectares': row[3],
                'location': row[4],
            }
            projects.append(my_dict)
        return projects
print(load_vineyards_from_db())

username = os.getenv("METEO_USER")
password = os.getenv("METEO_PASSWORD")

def load_weather():
    #Parameters
    coordinates = [(25.68, -100.31)]
    parameters = ['t_2m:C']
    model = 'mix'
    timezone = pytz.timezone('America/Monterrey')
    startdate = dt.datetime.now().astimezone(timezone)
    enddate = startdate + dt.timedelta(hours=1)
    interval = dt.timedelta(hours=1)
    #Request
    df = api.query_time_series(coordinates, startdate, enddate, interval, parameters, username, password, model=model)
    #Formating
    df.index = pd.DatetimeIndex(df.index.get_level_values('validdate'))
    df.index = df.index.tz_convert(timezone)
    data_array = df.to_numpy()
    return data_array[0][0]
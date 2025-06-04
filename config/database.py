from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote
from sqlalchemy.ext.declarative import declarative_base


password = quote("Y3f3r#@+")
mysql_file_name = f"mysql+mysqlconnector://root:{password}@localhost:3306/pos3d"


#password = quote("Y3f3rGuzm4n")
#mysql_file_name = f"mysql+mysqlconnector://admin:{password}@database-1.cdci468iy9mj.us-west-1.rds.amazonaws.com:3306/tienda"

engine = create_engine(mysql_file_name, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()
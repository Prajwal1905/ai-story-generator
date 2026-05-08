from sqlalchemy import create_engine
from urllib.parse import quote_plus

password = quote_plus("Prajwal@19")
url = f"mysql+pymysql://root:{password}@localhost:3306/story_generator"
print("URL:", url)

engine = create_engine(url)
conn = engine.connect()
print("Connected successfully!")
conn.close()
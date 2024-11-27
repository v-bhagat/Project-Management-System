from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///instance/site.db')

Session = sessionmaker(bind=engine)
session = Session()

metadata = MetaData()
metadata.reflect(bind=engine)

choice = int(input("\nPress 1 for delete task\nPress 2 for delete project\nPress 3 to EXIT\n\nEnter your choice::"))

if choice == 1:
    tablename = 'task'
elif choice == 2:
    tablename = 'project'
else:
    exit(0)
   

tabledata = metadata.tables.get(tablename)

if tabledata is not None:
    try:
        row = input("Enter id to delete: ")
        delete_query = tabledata.delete().where(tabledata.c.id == row)
        session.execute(delete_query)
        
        session.commit()
        print(f"Row with id = {row} deleted.")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()
else:
    print(f"Table {tablename} not found in the database.")
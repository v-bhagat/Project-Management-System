import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String

# Define the path to the SQLite database in the instance folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "instance", "site.db")}'

# Create a new SQLite database or connect to an existing one
engine = create_engine(DATABASE_URI)

# Create a base class for declarative models
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'  # Ensure this matches your actual table name
    
    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    role = Column(String(10), nullable=False, default='employee')

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

def update_user_role(email):
    user = session.query(User).filter_by(email=email).first()
    
    if user:
        if user.role == 'admin':
            print("User is already an admin.")
            print("Do you want to change role to employee")
            print("Enter 'yes' to change role to employee")
            print("Enter 'no' to keep role as admin")
            user_input = input("Enter your choice: ")
            if user_input.lower() == 'yes':
                user.role = 'employee'
                session.commit()
                print(f"User {email} has been updated to employee.")
            else:
                print(f"User {email} role remains as admin.")
        else:
            user.role = 'admin'
            session.commit()
            print(f"User {email} has been updated to admin.")
    else:
        print("User not found.")

if __name__ == "__main__":
    email_to_update = input("Enter the employee email to promote to admin: ")
    update_user_role(email_to_update)

    # Close the session
    session.close()

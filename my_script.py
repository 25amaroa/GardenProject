import mysql.connector
import datetime

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="luna2002",
    database="gardenDB"
    
)

mycursor = conn.cursor()

#The following code was how I created and initialized the database and tables.

# Create a database named "gardenDB"
# mycursor.execute("CREATE DATABASE gardenDB")

# Create a table named "USER" in the "gardenDB" database
# USER table will have the following columns:
# user_id (primary key, auto-incremented integer)
# fname (string)
# lname (string)
# email (string)
    #mycursor.execute("CREATE TABLE USER (user_id INT AUTO_INCREMENT PRIMARY KEY, fname VARCHAR(255), lname VARCHAR(255), email VARCHAR(255))")
user_data = [
    (1, 'John', 'Doe', 'john@example.com'),
    (2, 'Jane', 'Smith', 'jane@example.com')
]
#for user in user_data:
#    mycursor.execute("INSERT INTO USER (user_id, fname, lname, email) VALUES (%s, %s, %s, %s)", user)

#USE gardenDB;
#SELECT * FROM USER;



# Create a table named "GARDEN" in the "gardenDB" database
# GARDEN table will have the following columns:
# garden_id (primary key, auto-incremented integer)
# user_id (foreign key, integer)
# date_created (date)
# size_of_bed (integer)
    #mycursor.execute("""CREATE TABLE GARDEN (garden_id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, date_created DATE, size_of_bed INT, FOREIGN KEY (user_id) REFERENCES USER(user_id))""")
garden_data = [
    (1, 1, '2024-05-01', 10),
    (2, 2, '2024-05-02', 8)
]
#for garden in garden_data:
#    mycursor.execute("INSERT INTO GARDEN (garden_id, user_id, date_created, size_of_bed) VALUES (%s, %s, %s, %s)", garden)


# Create a table named "PLANT" in the "gardenDB" database
# PLANT table will have the following columns:
# plant_id (primary key, auto-incremented integer)
# garden_id (foreign key, integer)
# english_name (string) 
# latin_name (string)
# date_planted (date)
    #mycursor.execute("""CREATE TABLE PLANT (plant_id INT AUTO_INCREMENT PRIMARY KEY, garden_id INT, english_name VARCHAR(255), latin_name VARCHAR(255), date_planted DATE, FOREIGN KEY (garden_id) REFERENCES GARDEN(garden_id))""")
plant_data = [
    (1, 1, 'Rose', 'Rosa', '2024-05-05'),
    (2, 1, 'Lily', 'Lilium', '2024-05-10'),
    (3, 2, 'Sunflower', 'Helianthus', '2024-05-15')
]

#for plant in plant_data:
#    mycursor.execute("INSERT INTO PLANT (plant_id, garden_id, english_name, latin_name, date_planted) VALUES (%s, %s, %s, %s, %s)", plant)

# Create a table named CARE_GUIDE in the gardenDB database
# CARE_GUIDE table will have the following columns:
# plant_id (foreign key, integer)
# season (string)
# sunlight (string)
# water (string)
# soil (string)
# fertilization (string)
    #mycursor.execute("""CREATE TABLE CARE_GUIDE (plant_id INT, season VARCHAR(255), sunlight VARCHAR(255), water VARCHAR(255), soil VARCHAR(255), fertilization VARCHAR(255), PRIMARY KEY (plant_id, season), FOREIGN KEY (plant_id) REFERENCES PLANT(plant_id))""")
care_guide_data = [
    (1, 'Spring', 'Full sunlight', 'Regular watering', 'Well-drained soil', 'Monthly fertilization'),
    (1, 'Summer', 'Partial sunlight', 'Twice a week watering', 'Loamy soil', 'Bi-weekly fertilization'),
    (2, 'Spring', 'Partial sunlight', 'Regular watering', 'Well-drained soil', 'Monthly fertilization'),
    (3, 'Summer', 'Full sunlight', 'Regular watering', 'Loamy soil', 'Weekly fertilization')
]

#for care_guide in care_guide_data:
#    mycursor.execute("INSERT INTO CARE_GUIDE (plant_id, season, sunlight, water, soil, fertilization) VALUES (%s, %s, %s, %s, %s, %s)", care_guide)

# Create a table named IMAGE in the gardenDB database
# IMAGE table will have the following columns:
# image_id (primary key, auto-incremented integer)
# user_id (foreign key, integer)
# plant_id (foreign key, integer)
# image_url (string)
# upload_date (datetime)
#mycursor.execute("""CREATE TABLE IMAGE (image_id INT AUTO_INCREMENT PRIMARY KEY,user_id INT, plant_id INT,image_url VARCHAR(255), upload_date DATETIME, FOREIGN KEY (user_id) REFERENCES USER(user_id), FOREIGN KEY (plant_id) REFERENCES PLANT(plant_id))""")

image_data = [
    (1, 1, 'rose.jpg', '2024-05-05 10:00:00'),
    (1, 2, 'lily.jpg', '2024-05-10 11:00:00'),
    (2, 3, 'sunflower.jpg', '2024-05-15 12:00:00')
]
#for image in image_data:
#    mycursor.execute("INSERT INTO IMAGE (user_id, plant_id, image_url, upload_date) VALUES (%s, %s, %s, %s)", image)

# The folowing code it the 3 functions that I listed I would create in the README.md file.

# Function to view care information for a plant
def view_care_information():
    try:
        # Retrieving care information
        english_name = input("Enter the English name of the plant you would like to view care information for: ")
        mycursor.execute("SELECT season, sunlight, water, soil, fertilization FROM CARE_GUIDE cg INNER JOIN PLANT p ON cg.plant_id = p.plant_id WHERE english_name = %s",
                         (english_name,))
        care_info = mycursor.fetchall()
        
        if care_info:
            print("Care information for", english_name, ":")
            for info in care_info:
                print("Season:", info[0])
                print("Sunlight:", info[1])
                print("Water:", info[2])
                print("Soil:", info[3])
                print("Fertilization:", info[4])
        else:
            print("Care information not found for", english_name)
    except mysql.connector.Error as err:
        print("Error retrieving care information:", err)


#view_care_information()

#Function to add a new plant to the garden
def add_plant_to_garden(mycursor, conn, user_id, garden_id, english_name, latin_name, date_planted):
    # Get the current date
    current_date = datetime.date.today()

    # SQL query to insert a new plant into the PLANT table
    insert_query = """
    INSERT INTO PLANT (garden_id, english_name, latin_name, date_planted)
    VALUES (%s, %s, %s, %s)
    """
    
    # Data to insert into the PLANT table
    plant_data = (garden_id, english_name, latin_name, date_planted)

    try:
        # Execute the INSERT query
        mycursor.execute(insert_query, plant_data)

        # Commit t
        conn.commit()
        
        print("Plant added to garden successfully!")
    except Exception as e:
        # If an error occurs
        conn.rollback()
        print("Error:", e)

# Test function to add a new plant to the garden

#add_plant_to_garden(mycursor, conn, user_id=2, garden_id=2, english_name="Yarrow", latin_name="Achillea millefolium", date_planted="2024-05-15")
#SELECT p.* 
#FROM PLANT p 
#INNER JOIN GARDEN g ON p.garden_id = g.garden_id 
#WHERE g.user_id = 2 AND g.garden_id = 2;


# Function to create a new user
def create_new_user(mycursor, conn):
    # Prompt the user to enter user information
    print("Please enter the following user information:")
    fname = input("First name: ")
    lname = input("Last name: ")
    email = input("Email: ")
    
    # SQL query to insert a new user into the USER table
    insert_query = """
    INSERT INTO USER (fname, lname, email)
    VALUES (%s, %s, %s)
    """
    
    # Data to insert into the USER table
    user_data = (fname, lname, email)

    try:
        # Execute the INSERT query
        mycursor.execute(insert_query, user_data)

        # Commit the transaction
        conn.commit()
        
        print("User added successfully!")
    except Exception as e:
        # If an error occurs
        conn.rollback()
        print("Error:", e)

# Test function to create a new user
#create_new_user(mycursor, conn)
#SELECT *FROM USER




# Test: Establish a connection to the MySQL database
#try:
    # Attempt to establish a connection to the MySQL database
#    connection = mysql.connector.connect(user='root', host='localhost', password='luna2002')
    
    # If no exception is raised, the connection was successful
#    print("Connection to MySQL database successful.")
    
    # Optionally, you can perform additional operations here
    
    # Don't forget to close the connection when you're done
#    connection.close()
    
#except mysql.connector.Error as err:
    # If an exception occurs, print the error message
#    print("Error connecting to MySQL database:", err)



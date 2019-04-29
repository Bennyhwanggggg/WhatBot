# Database
This module contains the database class which is responsible for all operations related to the database. It uses AWS RDS with PostgreSQL as the database.

## Features
### SQL Query Execution
Execute SQL queries using multiple instance of cursors to avoid race conditions when running against multiple clients. 

### SQL injection sanitation
Sanitize user inputs to avoid SQL injection attacks or Cross Site Scripting for better security.

### Common SQL queries
Contains common SQL queries used often in the rest of the software.

### File storage
Uses AWS S3 for file storage to store our training data.

## Data Schema
```
Database 1: postgres
    -| table 1: courselist 
        --| Attributes: (
                course_code, 
                course_name, 
                timetable, 
                adk, 
                comment)
    -| table 2: info_handbook:
        --| Attributes: 
                (cid, 
                title, 
                credit, 
                prerequisite, 
                outline_url, 
                faculty_url, 
                school_url, 
                offer_term,           
                campus, 
                description, 
                pdf_url, 
                indicative_contact_hr, 
                commonwealth_std, 
                domestic_std,
                international_std)
    -| table 3: consultation:
        --| Attributes:
                (cid,
                 sid,
                 time,
                 date)
    -| table 4: users:
        --| Attributes:
                (username,
                 password,
                 type)
    -| table 5: announcement:
        --| Attributes:
                (cid,
                 c_name,
                 content,
                 date)
    -| table 6: classroom:
        --| Attributes:
                (cid,
                 location)
    -| table 7: coursetimetable:
        --| Attributes:
                (cid,
                 c_name,
                 time)
    -| table 8: intent_data:
        --| Attributes:
                (query_text,
                 intent,
                 confidence,
                 timestamp)
    -| table 9: wam:
        --| Attributes:
                (sid,
                 cid,
                 mark,
                 credit)
```
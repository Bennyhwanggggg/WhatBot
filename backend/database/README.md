Data scheme


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

Database 2: 

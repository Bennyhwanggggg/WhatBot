-- data analytic module hadnbook

create domain URLType as
varchar(100) check (value like 'http://%');

create domain Tuition_fee as
varchar(100) check (value like '$%');


create table Info_handbook(
    CID            varchar(10) primary key,
    title          varchar(50),
    credit         varchar(20),
    prerequisite   VARCHAR(30),
    outline_url    URLType,
    faculty_url    URLType,
    school_url     URLType,
    Offer_term     varchar(20),
    campus         varchar(15),
    description    varchar(300),
    pdf_url        URLType,
    indicative_contact_hr  INTEGER,
    commonwealth_std Tuition_fee,
    domestic_std    Tuition_fee,
    international_std  Tuition_fee
);


create table course_list(
    Course_code varchar(8) primary key,
    Course_name varchar(50),
    Timetable varchar(20),
    ADK boolean,
    Comment varchar(50)
);

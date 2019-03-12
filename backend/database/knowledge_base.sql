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
    indicative_contact_hr  INTEGER,
    commonwealth_std Tuition_fee,
    domestic_std    Tuition_fee,
    international_std  Tuition_fee
);
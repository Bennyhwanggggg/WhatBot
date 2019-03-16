-- 9900 database
create domain Std_ID as
varchar(100) check (value like 'z%');

-- create TABLE Student(
--     SID     Std_ID primary key,
--     firstname varchar(50) not null,
--     lastname  VARCHAR(50) not null
-- );

create TABLE Student(
    SID     varchar(10) primary key,
    firstname varchar(50) not null,
    lastname  VARCHAR(50) not null
);

create TABLE Lecturer(
    LID  serial primary key,
    firstname varchar(50) not null,
    lastname  VARCHAR(50) not null
);


create table Timeslot(
    tid int primary key,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    available boolean
);

-- create table Appointment(
--     sid Std_ID REFERENCES Student(SID),
--     tid int REFERENCES Timeslot(tid),
--     starttime TIMESTAMP,
--     endtime TIMESTAMP,
--     primary key(sid,tid)
-- );

create table Appointment(
    sid varchar(10) REFERENCES Student(SID),
    tid int REFERENCES Timeslot(tid),
    starttime TIMESTAMP,
    endtime TIMESTAMP,
    primary key(sid,tid)
);

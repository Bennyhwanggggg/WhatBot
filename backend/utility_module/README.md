# UtilityModule

Utility Module contains many of WhatBot's cool features such as course consultation booking, wam 
calculator, course announcement and many more... The main UtilityModule Class has a design pattern
that follows similar to factory method such that it act as the entry point to instantiate everything
in this module

## Features

### Course Consultation Booking

Users can book consultation for a course through this functionality. Also, user can see their current
bookings and also cancel bookings as well. To simulate real world booking systems, this features limit
user to only allow to book consultation up to next 7 days as it seems unreasonable if people book consultation
for a time that is very far away.

### Classroom Finder

This feature allow user to locate where their classroom are such that they won't have to go through
the trouble of looking up their timetable and try to remember where all their classes are.

### Wam Calculator

For students, this feature allow them to check how they are currently progressing in their course work as
it provides them a nice summary of their grades for each course and also overall grade. For admins, 
this feature allow them to track any student's current performance by providing the same information except
they have access to all student's information.

### Announcement Getter

This feature allow student to check what the lecturer's latest announcement are so they can always stay up to date
with what is going on in a course!

### Course Timetable Finder

It is currently inconvenient to navigate through UNSW's timetable website as you need to navigate in and out 
of pages to see all the courses' timetable that you are interested in. This can be quite annoying especially 
when you want to plan your schedule as you need to go through many tabs to collect all the information. With this 
feature in WhatBot, you can get access to all timetable information inside this app, which eases the process alot.  
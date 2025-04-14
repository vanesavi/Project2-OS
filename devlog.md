

**april 11 4:30 pm**  
just finished reading through the project description. need to simulate a bank with 3 tellers and 50 customers using threads.
also have to make sure the manager safe and door have the right access rules. trying to figure out the best way to structure this before diving in  

**april 11 4:45 pm**  
started coding after getting a better idea of how things should work. looked more into semaphores and how they work in python.
figured out how to use threading Semaphore. created one for the manager since only one teller can go at a time one for the safe which allows two and another for the door to control customer entry. 
also made a semaphore for each teller  

**april 11 5:00 pm**  
ran into a problem where two threads were trying to remove themselves from the queue at the same time. 
they were both hitting the list and it caused errors like index out of range or removing the wrong person. did some searching and figured out that using a lock would help  

**april 11 5:15 pm**  
added a lock and wrapped all the queue access with it using with lock. that fixed it. no more crashes or weird behavior when customers enter or leave the line  

**april 11 6:00 pm**  
added a randomSleep function to simulate delays. used time sleep with random uniform so that teller actions and customer waits feel more realistic.
cleaner than writing out separate sleep statements every time  

**april 12 11:30 am**  
worked on making sure customers wait their turn in the queue. they now only move when they are at the front.
wrapped that check in the lock too just to be safe  

**april 12 11:50 am**  
noticed that some of the print statements were showing up on the same line. it made the output super messy and hard to follow  

**april 12 12:00 pm**  
added a print lock and made a safePrint function to fix that. now every print statement is locked so each line comes out clean and readable  

**april 12 12:20 pm**  
had a small issue with customerCount. python kept saying it was a local variable even though i defined it at the top. 
figured out i needed to use global customerCount inside the function before modifying it. after that it worked fine  

**april 12 2:00 pm**  
wanted a way to check if a semaphore was available without blocking. found out you can just use acquire with blocking set to false. 
used that when customers look for a free teller  

**april 12 2:30 pm**  
watched the project video to double check the flow. updated the code so tellers ask for the transaction and customers respond after.
also added logs before and after sleeps and anytime someone uses the manager or safe  

**april 12 3:10 pm**  
set up the transaction logic. withdrawals go to the manager and deposits skip straight to the safe.
made sure the semaphores work so only one teller can go to the manager and two to the safe at a time. logs show every step clearly  

**april 12 5:25 pm**  
tested with five customers. everything worked fine. no crashes and the logs looked good. 
queue logic held up and tellers responded correctly  

**april 13 12:15 pm**  
ran with ten customers. customer threads are entering in pairs like they should and transactions are going through with the right timing. 
manager and safe are working with no overlap  

**april 13 1:00 pm**  
bumped it up to twenty customers. still going smooth. fixed a few of the log messages to match the format from the sample output in the assignment  

**april 13 2:00 pm**  
ran the full fifty customer simulation. output is long but looks good. 
the queue never breaks and the right number of threads are allowed through each step. really happy with how the semaphores are working  

**april 13 3:30 pm**  
scrolled through the full log. everything lines up. tellers go back to waiting after each customer and the customer threads leave through the door properly.
even the final teller exits are printing when they are supposed to  

**april 13 8:00 pm**  
final run done. the logs are clean all semaphores are behaving and no weird thread behavior. feels good to be finished with this one

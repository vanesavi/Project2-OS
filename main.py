#Importing libs
import threading
import time
import random

# Setting up global variable so all threads can access queue to see
#  which is first in line to see teller nex
global customerQueue
customerQueue = []

#To control amount of customers in simulation
global customerCount
customerCount = 50


#Ensure good consistent formatting in the terminal due to threads clashing
print_lock = threading.Lock()
def safe_print(textToPrint):
    with print_lock:
        print(textToPrint)

#Setting up Semaphore for required bottlenecks 
managerSem = threading.Semaphore(value=1)
safeSem = threading.Semaphore(value=2)
doorSem = threading.Semaphore(value=2)

# Setting up teller Semaphore as a requirement is to state when each is ready
tellerSem = []
for j in range (3):
    tellerSem.append(threading.Semaphore(1))
    safe_print(f"Teller {j}: ready to serve")
    safe_print(f"Teller {j}: waiting for customer")

#Setting up random sleep funct to make code more clean 
def randomSleep(startFloat, endFloat):
    time.sleep(random.uniform(startFloat, endFloat))
    
#Coordinates the whole process for the customer threads
def init_customer(customerID):
    #frontOfLine only False if thread is next to see teller
    #serviceRequest 1 - Deposit/ 0 - Withdrawal
    frontOfLine = True
    serviceRequest = random.randint(0,1)

    if serviceRequest == 0:
        safe_print(f"{customerID}: wants to perform a withdraw transaction")
    else:
        safe_print(f"{customerID}: wants to perform a deposit transaction")
    
    #Time to decide to go to bank then get to bank
    randomSleep(0.0,0.1)

    #Make sure only 2 people at a time through the door
    safe_print(f"{customerID}: going to bank")
    doorSem.acquire()
    safe_print(f"{customerID}: entering bank")
    doorSem.release()

    #With statements endure that no clashing when accessing line and editing
    with lock:
        safe_print(f"{customerID}: getting in line")
        customerQueue.append(customerID)

    #If front of line then time to move to next step to get teller
    while frontOfLine:
        with lock:
            if customerQueue[0] == customerID:
                frontOfLine = False
                customerQueue.remove(customerID)
    
    #While statement ensures teller that is free is picked. 
    #After picked then executes the relavant code as per request
    safe_print(f"{customerID}: selecting teller")
    while True:
        
        #Keeps cycling through teller till avalible one found
        for iTeller in range(0,len(tellerSem)):
            freeSem = tellerSem[iTeller].acquire(blocking=False)
            
            if freeSem:
                safe_print(f"{customerID} [Teller {iTeller}]: selects teller")
                customerTransaction(iTeller,customerID,serviceRequest)

                #Ensure door only has 2 people using at once
                safe_print(f"{customerID}: goes to door")
                doorSem.acquire()
                safe_print(f"{customerID}: leaves the bank")
                doorSem.release()

                #releases the teller to deal with next customer
                tellerSem[iTeller].release()
                safe_print(f"Teller {iTeller}: Ready to serve")
                safe_print(f"Teller {iTeller}: Waiting for customer")

                #If last customer served frees tellers to leave for day
                global customerCount
                customerCount -=1
                if customerCount == 0:
                    for x in range(0,len(tellerSem)):
                        safe_print(f"Teller {x}: leaves for the day")
                return

#Coordinates requests by funneling into either deposit or withdraw
def customerTransaction(iTeller,customerID, serviceRequest):
    safe_print(f"{customerID} [Teller {iTeller}]: introduces themselves") 
    safe_print(f"Teller {iTeller} [{customerID}] : serving a customer") 
    safe_print(f"Teller {iTeller} [{customerID}] : asking for transaction") 

    if serviceRequest == 0:
        safe_print(f"{customerID} [Teller {iTeller}]: asks for withdrawal transaction") 
        ifWidthdraw(iTeller,customerID)
        
    else:
        safe_print(f"{customerID} [Teller {iTeller}]: asks for deposit transaction") 
        ifDeposit(iTeller,customerID)

    safe_print(f"{customerID} [Teller {iTeller}]: leaves teller") 


#Withdrawal logic
def ifWidthdraw(iTeller, customerID):
    
    safe_print(f'Teller {iTeller} [{customerID}]: handling withdraw transaction')
    
    managerSem.acquire()
    safe_print(f'Teller {iTeller} [{customerID}]: going to manager')
    safe_print(f"Teller {iTeller} [{customerID}]: getting manager's permission ")
    randomSleep(0.005, 0.03) # 5 to 30ms delay
    safe_print(f"Teller {iTeller} [{customerID}]: got manager's permission")
    managerSem.release()


    safe_print(f'Teller {iTeller} [{customerID}]: going to safe')
    safeSem.acquire()
    safe_print(f'Teller {iTeller} [{customerID}]: enter safe')
    randomSleep(0.01, 0.05) # 10 to 50ms delay
    safe_print(f'Teller {iTeller} [{customerID}]: leaving safe')
    safeSem.release()

    safe_print(f'Teller {iTeller} [{customerID}]: finishes withdraw transaction.')
    safe_print(f'Teller {iTeller} [{customerID}]: wait for customer to leave. ')


#Deposit logic
def ifDeposit(iTeller, customerID):
    safe_print(f'Teller {iTeller} [{customerID}]: handling deposit transaction')

    safe_print(f'Teller {iTeller} [{customerID}]: going to safe')
    safeSem.acquire()
    safe_print(f'Teller {iTeller} [{customerID}]: enter safe')
    randomSleep(0.01, 0.05) # 10 to 50ms delay
    safe_print(f'Teller {iTeller} [{customerID}]: leaving safe')
    safeSem.release()


    safe_print(f'Teller {iTeller} [{customerID}]: finishes deposit transaction.')
    safe_print(f'Teller {iTeller} [{customerID}]: wait for customer to leave.')



#Create lock to prevent collisions for accessing array
lock = threading.Lock()
threads = []

# Create and start a thread for each customer
for k in range(1,customerCount+1):
    thread = threading.Thread(target=init_customer, args=("Customer "+str(k),))
    threads.append(thread)
    thread.start()

# Optionally, wait for all threads to finish
for t in threads:
    t.join()

#End of program
safe_print("The bank closes for the day.")

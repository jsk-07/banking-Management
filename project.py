import csv

def transactions(ANo, type, amnt):
    a = [ANo, type, amnt]
    
    with open('y.csv', 'a', newline='') as f:
        b = csv.writer(f)
        b.writerow(a)

def load1():
    a = []
    try:
        with open('a.csv','r', newline='') as f:
            x = csv.reader(f)
            for i in x:
                try:
                    b = [i[0], i[1], i[2]]
                    a.append(b)
                except ValueError:
                    print(f"Skipping invalid row: {i}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return a

def load2():
    a = []
    try:
        with open('b.csv','r', newline='') as f:
            x = csv.reader(f)
            for i in x:
                try:
                    b = [i[0], i[1], i[2], i[3], i[4]]
                    a.append(b)
                except ValueError:
                    print(f"Skipping invalid row: {i}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return a

def load3():
    a = []
    try:
        with open('x.csv','r', newline='') as f:
            x = csv.reader(f)
            for i in x:
                try:
                    b = [str(i[0]), float(i[1])]
                    a.append(b)
                except ValueError:
                    print(f"Skipping invalid row: {i}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return a

def load4():
    a = []
    try:
        with open('z.csv','r', newline='') as f:
            x = csv.reader(f)
            for i in x:
                try:
                    b = [str(i[0]), float(i[1]), float(i[2]), str(i[3])]
                    a.append(b)
                except ValueError:
                    print(f"Skipping invalid row: {i}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return a

def save(Filename,a):
    try:
        with open(Filename,'w', newline='') as f:
            x = csv.writer(f)
            for i in a:
                x.writerow(i)
    except Exception as e:
        print(f"Error saving file: {e}")

def dep(ANo,a,d):
    for i in a:
        if i[0] == ANo:
            i[1] += d
            print(f"Deposited {d} to account {ANo}. New balance: {i[1]}")
            transactions(ANo, "Deposit", d)
            return True
    return False

def deposit(ANo):
    a = load3()
    while True:
        try:
            d = float(input("Enter the amount to deposit: "))
            if d < 0:
                print("Deposit amount must be positive. Please try again.")
                continue
        except ValueError:
            print("Invalid amount entered. Please enter a valid number.")
            continue

        if dep(ANo,a,d):
            save('x.csv',a)
            break 
        else:
            print(f"Account number {ANo} not found. Please check and try again.")

def withd(ANo,a,w):
    for i in a:
        if i[0] == ANo:
            i[1] -= w
            print(f"Withdrawn {w} to account {ANo}. New balance: {i[1]}")
            transactions(ANo, "Withdrawal", w)
            return True
    return False

def withdraw(ANo):
    a = load3()
    while True:
        try:
            w = float(input("Enter the amount to withdrawn: "))
            if w < 0:
                print("Deposit amount must be positive. Please try again.")
                continue
        except ValueError:
            print("Invalid amount entered. Please enter a valid number.")
            continue

        if withd(ANo,a,w):
            save('x.csv',a)
            break 
        else:
            print(f"Account number {ANo} not found. Please check and try again.")

def bal(ANo,a):
    for i in a:
        if i[0] == ANo:
            print(f" Account Number {ANo}. Newbalance: {i[1]}")
            return True
    return False

def balance(ANo):
    a = load3()
    while True:
        if bal(ANo,a):
            break 
        else:
            print(f"Account number {ANo} not found. Please check and try again.")

def transfer(ANo1):
    a = load3()
    
    while True:
        ANo2 = input("Enter the destination account number: ")
        ANo2_found = False
        for i in a:
            if i[0] == ANo2:
                ANo2_found = True
                break
        
        if not ANo2_found:
            print(f"Destination account {ANo2} not found. Please check and try again.")
            continue
        
        try:
            amount = float(input("Enter the amount to transfer: "))
            if amount <= 0:
                print("Transfer amount must be positive. Please try again.")
                continue
        except ValueError:
            print("Invalid amount entered. Please enter a valid number.")
            continue

        ANo1_found = False
        for i in a:
            if i[0] == ANo1:
                if i[1] >= amount:
                    i[1] -= amount
                    print(f"Transferred {amount} from account {ANo1}. New balance: {i[1]}")
                    transactions(ANo1, "Transfer", amount)
                    
                    for j in a:
                        if j[0] == ANo2:
                            j[1] += amount
                            print(f"Deposited {amount} to account {ANo2}. New balance: {j[1]}")
                            transactions(ANo2, "Transfer", amount)
                            save('x.csv', a) 
                            return True
                else:
                    print("Insufficient funds in the source account.")
                    ANo1_found = True
                    break
        
        if not ANo1_found:
            print(f"Source account {ANo1} not found. Please check and try again.")

def borrow_loan(ANo):
    a = load3()
    b = load4() 

    loan_found = False
    for loan in b:
        if loan[0] == ANo and loan[3] == "Pending": 
            loan_found = True
            break
    
    if loan_found:
        print(f"Loan application rejected. You have an unpaid loan. Please repay your existing loan before applying for a new one.")
        return 
    
    while True:
        try:
            loan_amount = float(input("Enter the loan amount you wish to borrow: "))
            if loan_amount <= 0:
                print("Loan amount must be positive. Please try again.")
                continue
        except ValueError:
            print("Invalid loan amount entered. Please enter a valid number.")
            continue
        
        interest_rate = 0.05
        total_due = loan_amount + (loan_amount * interest_rate)

        for i in a:
            if i[0] == ANo:
                i[1] += loan_amount
                print(f"Loan of {loan_amount} granted to account {ANo}. New balance: {i[1]}")
                transactions(ANo, "Loan Borrowed", loan_amount) 

                loan_data = [ANo, loan_amount, total_due, "Pending"]  # Mark loan status as "Pending"
                with open('z.csv', 'a', newline='') as f:
                    y = csv.writer(f)
                    y.writerow(loan_data)

                save('x.csv', a)
                print(f"Total loan to be repaid (including interest): {total_due}")
                return True

def repay_loan(ANo):
    a = load3()
    b= load4()
    
    loan_found = False
    loan_total_due = 0  
    loan_balance = 0  
    for loan in b:
        if loan[0] == ANo and loan[3] == "Pending":  
            loan_found = True
            loan_balance = float(loan[2])
            loan_total_due = loan_balance
            break

    if not loan_found:
        print(f"No pending loan found for account number {ANo}, Please check your loan status.")
        return

    while True:
        try:
            repay_amount = float(input(f"Enter the amount you want to repay (Remaining loan balance: {loan_balance}): "))
            if repay_amount <= 0:
                print("Repayment amount must be positive. Please try again.")
                continue
            if repay_amount > loan_balance:
                print("Repayment amount cannot exceed the remaining loan balance. Please enter a valid amount.")
                continue
        except ValueError:
            print("Invalid repayment amount entered. Please enter a valid number.")
            continue

        for i in a:
            if i[0] == ANo:
                if i[1] >= repay_amount:
                    i[1] -= repay_amount 
                    print(f"Repayment of {repay_amount} made from account {ANo}. New balance: {i[1]}")
                    transactions(ANo, "Loan Repayment", -repay_amount) 

                    loan_balance -= repay_amount
                    print(f"Remaining loan balance: {loan_balance}")

                    for loan in b:
                        if loan[0] == ANo and loan[3] == "Pending":
                            if loan_balance == 0:
                                loan[3] = "Paid" 
                                print(f"Loan for account {ANo} is now fully paid off.")
                            loan[2] = str(loan_balance) 
                            break

                    save('x.csv', a)
                    save('z.csv',b) 
                    return True
                else:
                    print(f"Insufficient funds to make a repayment of {repay_amount}. Please deposit more funds first.")
                    return False

def view_loan_status(ANo):
    a = load4()

    loan_found = False
    for i in a:
        if i[0] == ANo and i[3] == "Pending":
            loan_found = True
            x = float(i[1])
            y= float(i[1]+0.05*float(i[1]))
            z = float(i[2])
            print(f"Loan Details for Account {ANo}:")
            print(f"Loan Amount: {x}")
            print(f"Total Due (Including Interest): {y}")
            print(f"Amount Payed : {(y-z)}")
            print(f"Remaining Loan Balance: {z}")
            break

    if not loan_found:
        print(f"No pending loan found for account number {ANo}.")

def read(Filename):
    a=open(Filename,"r",newline="")
    b=csv.reader(a)
    for line in b:
        print(line)
    a.close()
    
def update_name1(EId, password):
    a = load2()
    found = False
    for i in a:
        if EId == i[0] and password == i[2]:
            new_name = input("Enter your new name: ")
            i[1] = new_name  # Update name
            print("Name updated successfully!")
            found = True
            break
    
    if not found:
        print("Employee ID or password incorrect.")
    save('b.csv',a)

def update_name2():
    a = load2()
    EId = input('Enter the Employee ID: ')
    found = False
    for i in a:
        if EId == i[0]:
            new_name = input("Enter your new name: ")
            i[1] = new_name  # Update name
            print("Name updated successfully!")
            found = True
            break
    
    if not found:
        print("Employee ID or password incorrect.")
    save('b.csv',a)

def update_name3(ANo, password):
    a = load1()
    found = False
    for i in a:
        if ANo == i[0] and password == i[2]:
            new_name = input("Enter your new name: ")
            i[1] = new_name  # Update name
            print("Name updated successfully!")
            found = True
            break
    
    if not found:
        print("Employee ID or password incorrect.")
    save('a.csv',a)

def update_name4():
    a = load1()
    ANo = input('Enter the Employee ID: ')
    found = False
    for i in a:
        if ANo == i[0] :
            new_name = input("Enter your new name: ")
            i[1] = new_name  # Update name
            print("Name updated successfully!")
            found = True
            break
    
    if not found:
        print("Employee ID or password incorrect.")
    save('a.csv',a)

def update_password(EId,password):
    a = load2()
    found = False
    for i in a:
        if EId == i[0] and password == i[2]:
            new_password = input("Enter your new password: ")
            i[2] = new_password  # Update password
            print("Password updated successfully!")
            found = True
            break
    if not found:
        print("Incorrect employee ID or password.")
    save('b.csv',a)

def update_password2(ANo, password):
    a = load1()
    found = False
    for i in a:
        if ANo == i[0] and password == i[2]:
            new_password = input("Enter your new password: ")
            i[2] = new_password  # Update password
            print("Password updated successfully!")
            found = True
            break
    if not found:
        print("Incorrect employee ID or password.")
    save('a.csv',a)

def update_salary():
    a = load2()
    EId = input('Enter the Employee ID: ')
    found = False
    for i in a:
        if EId == i[0] :
            new_salary = input("Enter new salary: ")
            i[4] = new_salary  # Update salary
            print("Salary updated successfully!")
            found = True
            break
    if not found:
        print("Incorrect employee ID.")
    save('b.csv',a)

def update_designation():
    a = load2()
    EId = input('Enter the Employee ID: ')
    found = False
    for i in a:
        if EId == i[0] :
            new_designation = input("Enter new designation: ")
            i[3] = new_designation  # Update Designation
            print("Designation updated successfully!")
            found = True
            break
    if not found:
        print("Incorrect employee ID.")
    save('b.csv',a)

def custsignup():
    a = input('Enter the account number: ')

    with open('a.csv', 'r') as f:
        x = csv.reader(f)
        for i in x:
            if a == i[0]:
                print(f"Account number {a} already exists. Please log in or choose a different account number.")
                return  

    b = input('Please enter your name: ') 
    c = input('Create password: ')
    d = float(input('Input Initial Deposit: '))
    e = [a, b, c]  
    g = [a, d]     

    with open('a.csv', 'a', newline='') as f:
        x = csv.writer(f)
        x.writerow(e)

    with open('x.csv', 'a', newline='') as f1:
        y = csv.writer(f1)
        y.writerow(g)

    transactions(a, 'Deposit', d)

    print('Sign-up successful!')

    while True:
        print('1. Make deposit\n''2. Make withdrawal\n''3. Transfer money\n''4. Check Balance\n''5. Apply for loan\n''6. Repay loan\n''7. Check Loan Status\n''8. Update Your Name\n''9. Update Your Password\n''10. Back to Main Menu\n''11. Exit')
        q = int(input('Enter choice: '))
        if q == 1:
            deposit(a)
        elif q == 2:
            withdraw(a)
        elif q == 3:
            transfer(a)
        elif q == 4:
            balance(a)
        elif q == 5:
            borrow_loan(a)
        elif q == 6:
            repay_loan(a)
        elif q == 7:
            view_loan_status(a)
        elif q == 8:
            update_name3(a, c)
        elif q == 9:
            update_password2(a, c)
        elif q == 10:
            continue
        elif q==11:
            break

def empsignup():
    a = input('Enter employee ID: ')

    with open('b.csv', 'r') as f:
        x = csv.reader(f)
        for i in x:
            if a == i[0]:
                print(f"Account number {a} already exists. Please log in or choose a different account number.")
                return  

    b = input('Please enter your name: ')
    c = input('Create password: ')
    d = input('Please enter your designation: ')
    e = input('Enter assigned salary: ')
    g = [a, b, c, d, e]
    
    with open('b.csv', 'a', newline='') as f:
        x = csv.writer(f)
        x.writerow(g)
    
    print('Sign-up successful!')

    while True:
        print('1. View Customer Records\n''2. View Employee Records\n''3. View Balance Records \n''4. View Loan Records\n''5. Update Employee Details\n''6. Update Customer Details\n''7. Back to Main Menu\n''8. Exit\n')
        q=int(input('enter choice'))
        if q==1:
            read('a.csv')
        elif q==2:
            read('b.csv')
        elif q==3:
            read('x.csv')
        elif q==4:
            read('z.csv')
        elif q==5:
            print('1. Change Your Name\n''2. Change Your Password\n')
            m=int(input('Enter Choice'))
            if m==1:
                update_name1(a,c)
            elif m==2:
                update_password(a,c)
        elif q==6:
            print('Change Customer Name\n')
            n=int(input('enter choice'))
            if n==1:
                update_name4()
        elif q==7:
            continue
        elif q==8:
            break

def custsignin():
    a = input('Enter the account number: ')
    with open('a.csv', 'r') as f:
        x = csv.reader(f)
        found = False  
        for i in x:
            if a == i[0]:
                c = input('Enter password: ')
                if c == i[2]:
                    print('Login successful!')
                    found = True

                    while True:
                        print('1. Make deposit\n''2. Make withdrawl\n''3. Transfer money\n''4. Check Balance\n''5. Apply for loan\n''6. Repay loan\n''7. Check Loan Status\n''8. Update Your Name\n''9. Update Your Password\n''10. Back to Main Menu\n''11. Exit\n')
                        q = int(input('Enter choice: '))
                        if q == 1:
                            deposit(a)
                        elif q == 2:
                            withdraw(a)
                        elif q == 3:
                            transfer(a)
                        elif q == 4:
                            balance(a)
                        elif q == 5:
                            borrow_loan(a)
                        elif q == 6:
                            repay_loan(a)
                        elif q == 7:
                            view_loan_status(a)
                        elif q == 8:
                            update_name3(a,c)
                        elif q == 9:
                            update_password2(a,c)
                        elif q == 10:
                            continue
                        elif q == 11:
                            break

                else:
                    print('Incorrect password.')
                    found = True
        
        if not found:
            print('Account number not found, try signing up.')

def empsignin():
    a = input('Enter the employee ID: ')
    with open('b.csv', 'r') as f:
        x = csv.reader(f)
        found = False  # Flag to track if employee ID is found
        for i in x:
            if a == i[0]:
                c = input('Enter password: ')
                if c == i[2]:
                    print('Login successful!')
                    found = True

                    while True:
                        print('1. View Customer Records\n''2. View Employee Records\n''3. View Balance Records \n''4. View Loan Records\n''5. Update Employee Details\n''6. Update Customer Details\n''7. Back to Main Menu\n''8. Exit')
                        q = int(input('Enter choice: '))
                        if q == 1:
                            read('a.csv')
                        elif q == 2:
                            read('b.csv')
                        elif q == 3:
                            read('x.csv')
                        elif q==4:
                            read('z.csv')
                        elif q==5:
                            print('1. Change Your Name\n''2. Change Your Password\n')
                            m=int(input('Enter Choice'))
                            if m==1:
                                update_name1(a,c)
                            elif m==2:
                                update_password(a,c)
                        elif q==6:
                            print('Change Customer Name\n')
                            n=int(input('enter choice'))
                            if n==1:
                                update_name4()
                        elif q==7:
                            continue
                        elif q==8:
                            break
                else:
                    print('Incorrect password.')
                    found = True
                    break

        if not found:
            print('Employee ID not found, try signing up.')

def adminlogin():
    a=input('Password')
    if a=='jsk':
        print('access granted')
        
        while True:
            print('1. View Customer Records\n''2. View Employee Records\n''3. View Balance Records \n''4. View Transactions\n''5. View Loan Status\n''6. Change Employee Details\n''7. Change Customer Detsils\n''8. Back to Main Menu\n''9. Exit\n')
            q=int(input('enter choice'))
            if q==1:
                read('a.csv')
            elif q==2:
                read('b.csv')
            elif q==3:
                read('x.csv')
            elif q==4:
                read('y.csv')
            elif q==5:
                read('z.csv')
            elif q==6:
                print('1. Change Employee Name\n''2. Change Employee Designation\n''3. Change Employee Salary\n''4. Back to Main Menu\n''5. Exit\n')
                m=int(input('Enter Choice'))
                if m==1:
                    update_name2()
                elif m==2:
                    update_designation()
                elif m==3:
                  update_salary()
                elif m==4:
                    continue
                elif m==5:
                    break
            elif q==7:
                print('1. Change Customer Name\n''2. Exit')
                n=int(input('Enter Choice'))
                if n==1:
                    update_name4()
                elif n==2:
                    break
            elif q==8:
                continue
            elif q==9:
                break

    else:
        print('wrong password')


while True:
    print('1. Customer\n''2. Employee\n''3. Admin\n''4. Exit\n')
    ch=int(input('Enter choice'))
    if ch==1:
        print('1. Sign Up\n''2. Sign In\n''3. Back to Main Menu\n''4. Exit\n')
        x=int(input('enter choice'))
        if x==1:
            custsignup()
        elif x==2:
            custsignin()
        elif x==3:
            continue
        elif x==4:
            break
    elif ch==2:
        print('1. Sign Up\n''2. Sign In\n''3. Back to Main Menu\n''4. Exit\n')
        x=int(input('enter choice'))
        if x==1:
            empsignup()
        elif x==2:
            empsignin()
        elif x==3:
            continue
        elif x==4:
            break
    elif ch==3:
        print('1. Admin Login\n''2. Back to Main Menu\n''3. Exit\n')
        x=int(input('enter choice'))
        if x==1:
            adminlogin()
        elif x==2:
            continue
        elif x==3:
            break
    elif ch==4:
        break

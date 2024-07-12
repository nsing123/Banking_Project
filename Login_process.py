# Login MOdule


import mysql.connector
from mysql.connector import Error
import pandas as pd
import random
import random
import getpass
from decimal import Decimal
import pymysql
import re


# In[106]:


import Validations_module as vd
import Database_connection as db_con
import Card_generate_module as cg
import Registration_process as reg_p


# In[107]:

# retrieving balance and account number
def chcek_balance(user_id):
        connection = db_con.database_connection()
        try:
            with connection.cursor() as cursor:

                sql_balance="select * from banking.account_details where user_id=%s"  # check for the specific userid if balance is there
                
                cursor.execute(sql_balance, (user_id,))
                result_balance=cursor.fetchall()
                if not result_balance:        # print no account found 
                    print("Account not present")
                return result_balance[0]
        except Exception as e:
            print("Error occured",e,"Try again")
                

        finally:
            connection.close()  # Close the connection


        


# In[108]:

#beneficiary details 

def get_beneficiary(user_id):
        connection = db_con.database_connection()
        try:
            with connection.cursor() as cursor:
                select_query="""
                select user_id,username,beneficiary_name,account_number,bank_name
                 from banking.Users_reg_data u join banking.Beneficiaries b on u.UserID=b.user_id
                where UserID=%s
                """
                cursor.execute(select_query, (user_id,))
                result = cursor.fetchall()
                if not result:  # no beneficiary then print below
                        print("No records found.")
                else:
                    print("Beneficiary details")
                    for i in result:
                        print("Beneficiary_name: ",i['beneficiary_name'],"account_number: ",i['account_number'],"bank_name: ",i['bank_name'])
                
            
            
        except Exception as e:
                print("error occured ", e)
        finally:
                connection.close()
        return True
    


# In[109]:

# get all the added cards for the user
def get_cards(user_id):
        connection =db_con.database_connection()
        try:
            with connection.cursor() as cursor:
                select_query="""
select user_id,username,b.card_type,card_number
 from banking.Users_reg_data u join banking.user_Cards b on u.UserID=b.user_id
where UserID=%s
                """
                cursor.execute(select_query, (user_id,))
                result = cursor.fetchall()
                if not result:  # no result in db show below message
                        print("No records found.")
                else:
                    
                    for i in result:
                        print("User ID: " ,i['user_id'],"username: ", i['username'],"card type : ",i['card_type'],'XXXX XXXX '+str(i['card_number'])[-4:])
                
            
            
        except Exception as e:
                print("error occured ", e)
        finally:
                connection.close()
        return True
    


# In[110]:

#add beneficiary for users
def add_beneficiary(user_id, beneficiary_name, account_number, bank_name):
    connection = db_con.create_db_connection()
    
    try:
        with connection.cursor() as cursor:
          
            
            # Check if beneficiary account already exists for the user
            check_ben = "SELECT * FROM Beneficiaries WHERE user_id = %s AND account_number = %s"
            cursor.execute(check_ben, (user_id, account_number))
            existing_beneficiary = cursor.fetchone() 
        
            #account=existing_beneficiary['account_number']
            
            if existing_beneficiary:
                print(f"Beneficiary account '{account_number}' already exists for user '{user_id}'.")
            else:
                # Insert beneficiary into Beneficiaries table
                insert_ben = "INSERT INTO Beneficiaries (user_id, beneficiary_name, account_number, bank_name) VALUES (%s, %s, %s, %s)"
                data = (user_id, beneficiary_name, account_number, bank_name)
                cursor.execute(insert_ben, data)
                connection.commit()  # Commit the transaction
                print(f"Beneficiary '{beneficiary_name}' added successfully for user '{user_id}'.")
    
    except pymysql.Error as e:
        print(f"Error: {e}")
    
    finally:
        connection.close()  # Close the database connection
    return True


# In[111]:


def update_account_info(user_id):
        connection = db_con.database_connection()
        
        print("Please enter your option to proceed ")
        print(" 1 for address ")
        print(" 2 for mobilenumber")
        
        response=input("Enter your option 1, 2")
        if response=='1':
            new_address=input("enter new address to update")
            while True:
                if not vd.validate_address(new_address):
                    new_address=input("Please enter a valid address")
                else:
                    break
            try:
                with connection.cursor() as cursor:

                    
                    update_address="update banking.Users_reg_data set Address=%s where UserID=%s"
                    cursor.execute(update_address, (new_address,user_id))
                    connection.commit()
                    
                    select_update="select * from banking.Users_reg_data where UserID=%s "
                    cursor.execute(select_update, (user_id))
                    result_updated = cursor.fetchall()
                    
                    adhar_number=result_updated[0]['AadharNumber']
                    #print(result_updated[0]['AadharNumber'],"XXXX XXXX " + adhar_number[-4:])
                    
                    print("Name: ",result_updated[0]['UserName'])
                    print("Address: ",result_updated[0]['Address'])
                    print("MobileNumber: ",result_updated[0]['MobileNumber'])
                    print("AadharNumber: ","XXXX XXXX " + adhar_number[-4:])
                    
                    return True
                    
            except Exception as e:
                print("error occured ", e)

        # same Process for mobile update

        if response=='2':
            new_mobile_no=input("enter new mobile number to update")
            while True:
                if not vd.validate_phone(new_mobile_no):
                    new_mobile_no=input("Please enter a valid mobile number")
                else:
                    break
            try:
                with connection.cursor() as cursor:

                    
                    update_mobile="update banking.Users_reg_data set MobileNumber=%s where UserID=%s"
                    cursor.execute(update_mobile, (new_mobile_no,user_id,))
                    connection.commit()
                    
                    select_update="select * from banking.Users_reg_data where UserID=%s "
                    cursor.execute(select_update, (user_id))
                    result_updated = cursor.fetchall()
                    
                    adhar_number=result_updated[0]['AadharNumber']
                    #print(result_updated[0]['AadharNumber'],"XXXX XXXX " + adhar_number[-4:])
                    
                    print("Name: ",result_updated[0]['UserName'])
                    print("Address: ",result_updated[0]['Address'])
                    print("MobileNumber: ",result_updated[0]['MobileNumber'])
                    print("AadharNumber: ","XXXX XXXX " + adhar_number[-4:])
                    
                    return True
                    
            except Exception as e:
                print("error occured ", e)
            finally:
                connection.close()
            return True
                  


# In[112]:


from decimal import Decimal, InvalidOperation


def fund_transfer(user_id):
    connection = db_con.database_connection()
    try:
        with connection.cursor() as cursor:
            sender_account = input("Enter sender's account number: ")
            while True:
                if not vd.validate_account(sender_account):
                    sender_account = input("Enter valid sender's account number: ")
                else:
                    break

            # Fetch sender's account details
            select_sender_query = """
            SELECT username, account_number, amount
            FROM Users_reg_data u
            JOIN account_details a ON u.userid = a.user_id
            WHERE u.userid = %s AND a.account_number = %s
            """
            cursor.execute(select_sender_query, (user_id, sender_account))
            sender_result = cursor.fetchone()

            if sender_result:
                print("Enter the beneficiary details")
                
                beneficiary_account = input("Enter the beneficiary's account number: ")
                while True:
                    if not vd.validate_account(beneficiary_account):
                        beneficiary_account = input("Enter valid beneficiary's account number: ")
                    else:
                        break

                # Validate beneficiary account existence
                    
                select_beneficiary_query = """
                SELECT id, account_number
                FROM Beneficiaries
                WHERE account_number = %s and user_id = %s
                """
                cursor.execute(select_beneficiary_query, (beneficiary_account, user_id))
                beneficiary_result = cursor.fetchone()

                if not beneficiary_result:
                    print("Beneficiary account not found.")
                else:
                    while True:
                        try:
                            amount = Decimal(input("Enter the amount to transfer: "))
                            if amount <= 0:
                                print("Amount must be greater than zero.")
                            elif amount > sender_result['amount']:
                                print("Insufficient balance.")
                                break
                            else:
                                break
                        except InvalidOperation:
                            print("Invalid amount. Please enter a valid number.")

                    # Update sender's balance
                    if amount <= sender_result['amount']:
                        new_sender_balance = sender_result['amount'] - amount
                        update_sender_query = """
                        UPDATE account_details
                        SET amount = %s
                        WHERE user_id = %s AND account_number = %s
                        """
                        cursor.execute(update_sender_query, (new_sender_balance, user_id, sender_account))
                        connection.commit()

                        # Record transaction
                        insert_transaction_query = """
                        INSERT INTO Transactions (sender_id, beneficiary_id, amount)
                        VALUES (%s, %s, %s)
                        """
                        cursor.execute(insert_transaction_query, (user_id, beneficiary_result['id'], amount))
                        connection.commit()

                        # Update beneficiary's balance if exists with current bank
                        update_beneficiary_query = """
                        UPDATE account_details
                        SET amount = amount + %s
                        WHERE account_number = %s
                        """
                        cursor.execute(update_beneficiary_query, (amount, beneficiary_account))
                        connection.commit()

                        print(f"Transfer of {amount} successful.")
                    
            else:
                print(f"Sender account {sender_account} not found for user.")

    except Exception as e:
        print("Error occurred:", e)
    finally:
        connection.close()


# In[114]:







def change_pin(user_id, cardtype, old_pin, new_pin):
    connection = db_con.database_connection()  # Assuming database_connection returns a valid connection object
    
    try:
        with connection.cursor() as cursor:
            while True:
                res = input("Enter 'exit' to quit registration process else 1 to proceed: ")
                if res.lower() == 'exit':
                    break
                
                # Fetch card details for the user
                fetch_card_details = """
                SELECT * FROM banking.user_Cards 
                WHERE user_id = %s AND card_type = %s AND pin = %s
                """
                cursor.execute(fetch_card_details, (user_id, cardtype, old_pin))
                result = cursor.fetchone()
                
                if not result:
                    print(f"No '{cardtype}' card found for user with provided PIN.")
                    continue
                
                card_num = result['card_number']
                
                # Verify old PIN and update new PIN if conditions are met
                if result['pin'] == str(old_pin):
                    update_query = """
                    UPDATE banking.user_Cards 
                    SET pin = %s 
                    WHERE user_id = %s AND card_type = %s AND card_number = %s
                    """
                    cursor.execute(update_query, (new_pin, user_id, cardtype, card_num))
                    connection.commit()  # Commit the transaction
                    print(f"PIN updated successfully for '{user_id}' with '{cardtype}' card.")
                else:
                    print("Old PIN does not match. PIN update failed.")
    
    except pymysql.Error as e:
        print(f"Error: {e}")
    
    finally:
        connection.close()  # Close the database connection

    return True


# In[116]:

# this function is to enter thr masked pin
def enter_new_pin():
    while True:
        new_pin = getpass.getpass("Enter 4-digit PIN: ")

        if not vd.validate_pin(new_pin):
            print("Invalid PIN. Please enter a 4-digit numeric PIN.")
        else:
            break
    return new_pin


# In[117]:


def reg_new_card(user_id):
        connection = db_con.database_connection()
        try:
            with connection.cursor() as cursor:
        
                card_num=input("enter the card number to register")
                while True:
                    if  ( len(card_num) == 16) and ( card_num.isdigit() and card_num[0]!='0'):
                        break
                    else:
                        card_num=input("enter the card number to register")
                cvv=getpass.getpass("enter the cvv ")
                #print(len(cvv))
                while True:
                    if  ( len(cvv) == 3) and ( cvv.isdigit()):
                        break
                    else:
                        cvv=getpass.getpass("enter the cvv to register")
                        
                pin=getpass.getpass("enter the pin ")
                while True:
                    if (len(pin)==4) and (pin.isdigit()):
                        break
                    else:
                        pin=getpass.getpass("enter the 4 digit pin again")
                response=input("enter the card_type 1 debit 2 credit")
                card_type='credit' if response=='2' else 'debit'
                sql_card="select * from banking.user_Cards where card_number=%s and user_id=%s"
                cursor.execute(sql_card, (card_num,user_id))
                card_res=cursor.fetchone()
                #print(card_res,card_res['card_number'])
                if card_res!=None and str(card_num)==str(card_res['card_number']):
                    print("card already exits")
                else:
        
                    sql_insert="Insert into banking.user_Cards(user_id,card_type,card_number,pin,cvv) values(%s,%s,%s,%s,%s)"
        
                    cursor.execute(sql_insert, (user_id, card_type, card_num,pin,cvv))
                    connection.commit()
        
        except Exception as e:
            print("Error Occured",e)
        finally:
            connection.close()
        return True
        
        
          


# In[118]:


def add_fund(user_id):
    connection = db_con.database_connection()
    try:
        with connection.cursor() as cursor:
            sender_account = input("Enter sender's account number: ")
            while True:
                if not vd.validate_account(sender_account):
                    sender_account = input("Enter valid account number: ")
                else:
                    break

            # Fetch user's account details
            select_query = """
            SELECT username, account_number, amount
            FROM Users_reg_data u
            JOIN account_details a ON u.userid = a.user_id
            WHERE u.userid = %s AND a.account_number = %s
            """
            cursor.execute(select_query, (user_id, sender_account))
            result = cursor.fetchone()  # Assuming there's only one result for the user

            if result:
                while True:
                    try:
                        amount = Decimal(input("Enter the amount to add: "))
                        if amount < 0:
                            print("Amount must be positive.")
                        else:
                            break
                    except ValueError:
                        print("Invalid amount. Please enter a valid number.")

                new_balance = amount + result['amount']

                # Update user's balance
                update_query = """
                UPDATE account_details
                SET amount = %s
                WHERE user_id = %s AND account_number = %s
                """
                cursor.execute(update_query, (new_balance, user_id, sender_account))
                connection.commit()

                # Fetch updated details
                cursor.execute(select_query, (user_id, sender_account))
                updated_result = cursor.fetchone()
                #print("Updated account details:")
                #print(updated_result)

            else:
                print(f"Account number {sender_account} not found for user.")

    except Exception as e:
        print("Error occurred:", e)
    finally:
        connection.close()
    return True


# In[119]:


def view_transactions(user_id):
        connection = db_con.database_connection()
        try:
            with connection.cursor() as cursor:
                sql_query="""
                select t.sender_id,t.beneficiary_id,t.amount,t.transaction_date,u.username,b.beneficiary_name
                from transactions t join Users_reg_data u on t.sender_id=u.userid and t.sender_id=%s
                join Beneficiaries b on t.beneficiary_id=b.id """
                    
                cursor.execute(sql_query, (user_id,))
                result = cursor.fetchall()
                if not result:
                    print("No result for user_id",user_id)
                for i in result:
                    #print(i)
                    for key, v in i.items():
                        print(key,v , end=" ")
                    print()

                    
        except Exception as e:
            print(e)
        finally:
            connection.close()
        return True
                
        
    
    


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





import crypt
import datetime
import pymongo
from pymongo.errors import DuplicateKeyError
import os

url = os.getenv("mongodb")

client = pymongo.MongoClient(url)
db = client["auth"]
auth_db = db["users"]
db.users.create_index([('email', pymongo.ASCENDING)], unique=True)


def login(email, password):
  try:
    result = auth_db.find_one({"email": email}, {"_id": 0})
    #print("Result from mongo DB", result)
    if result != None:
      key = result['key']
      got_password = result["password"]
      data_pass = (got_password, key)
      decrypted = crypt.decrypt(data_pass)

      flag = False
      if decrypted == password:
        print("Password matched!!")
        flag = True
        flag = str(flag)
        account_id = result["account_id"]
        user_db = db[str(account_id)]
        secret_list = []
        record_list = []

        #print("User DB:", user_db)
        for record in user_db.find():
          #print("Record after first for loop", record)
          record_list.append(record)
        count = 0
        for items in record_list:
          #print("items:", items)
          if "app" in items:
            count += 1
            #print("appname from the item:", items["app"])
            app = items["app"]
            user = items["user"]
            enc_pass = items["password"]
            enc_key = items["key"]
            is_admin = items["is_admin"]
            data = (enc_pass, enc_key)
            dec_pass = crypt.decrypt(data)
            #print("dec_pass_key:", dec_pass)
            secret_dict = {}
            secret_dict["app"] = app
            secret_dict["user"] = user
            secret_dict["password"] = dec_pass
            secret_dict["count"] = count
            secret_dict["is_admin"] = is_admin
            print("dictionary:", secret_dict)
            secret_list.append(secret_dict)
        #print("Secret List from mongo db:", secret_list)
        return secret_list, account_id
        #print("Total Record:", record_list)
      else:
        return "invalid_password"
    else:
      return "invalid_email"
  except Exception as e:
    print(e)
    return e


def create_account(email, user, mobile, password, adminemail):
  print("Entering into create account function")
  print("ADMIN EMAIL:", adminemail)
  try:
    import random
    result = auth_db.find_one({"admin": adminemail}, {"_id": 0})
    if result != None:
      print("Result from create_account function:", result)
      got_admin_email = result["admin"]
      account_id = result["account_id"]
      print("Admin email:", adminemail)
      print("Account ID:", account_id)
      if adminemail == got_admin_email:
        r = account_id
        user_db = db[str(r)]
      else:
        r = random.randint(1111, 9999)
        user_db = db[str(r)]
    else:
      r = random.randint(1111, 9999)
      user_db = db[str(r)]
    print("USER DB:", user_db)
    created_time = datetime.datetime.now()
    encrypt_data = crypt.encryptor(password)
    encrypte_pass = encrypt_data[0]
    key = encrypt_data[1]
    query = {
        "email": email,
        "user": user,
        "mobile": mobile,
        "admin": adminemail,
        "password": encrypte_pass,
        "key": key,
        "account_id": r,
        "created_time": created_time
    }
    print("Query to add into user DB:", query)
    auth_db.insert_one(query)
    query2 = {"created time": created_time}
    user_db.insert_one(query2)
    return True
  except DuplicateKeyError:
    print("Duplicate ID not allowed")
    return "duplicate"


def remove_entry(remove_app, remove_user, account_id):
  try:
    user_db = db[str(account_id)]
    query = {"app": remove_app, "user": remove_user}
    user_db.delete_one(query)
    return "removed"
  except Exception as e:
    print(e)
    return False


def add_entry(add_app, add_user, add_pword, account_id, email):
  print("kicked off add_entry function:")
  try:
    user_db = db[str(account_id)]
    print(user_db)
    result = auth_db.find_one({"email": email}, {"_id": 0})
    print("result from add_entry:", result)
    got_email = result["admin"]
    print("Email from user:", email)
    print("Got email from auth DB:", got_email)
    user = "USER"
    if got_email == email:
      user = "ADMIN"
    data = crypt.encryptor(add_pword)
    print("data from add entry:", data)
    encrypte_pass = data[0]
    key = data[1]
    query = {
        "app": add_app,
        "user": add_user,
        "is_admin": user,
        "password": encrypte_pass,
        "key": key
    }
    user_db.insert_one(query)
    return "added"
  except Exception as e:
    print(e)
    return e


def reset_password(user, email, admin, password):
  try:
    print("Password before encryption:", password)
    encrypt_data = crypt.encryptor(password)
    encrypte_pass = encrypt_data[0]
    key = encrypt_data[1]
    filter = {"email": email, "user": user, "admin": admin}
    new_values = { "$set":  {'password': encrypte_pass, 'key': key } }
    print("new_values:", new_values)
    print(auth_db)
    result = auth_db.find_one(filter)
    print(result.json())
    response = auth_db.update_one(filter, new_values)
    print(response)
    return "Updated"
  except:
    return "Failed"

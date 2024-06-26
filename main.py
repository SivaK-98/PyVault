# This is Working code
import logging
import datetime
from flask import Flask, flash, redirect, render_template, request, url_for

import mongodb

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['MESSAGE_FLASHING_OPTIONS'] = {'duration': 5}

logging.basicConfig(filename='logs/pyvault.txt',
                    filemode='a',
                    format='%(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@app.route('/')
@app.route('/home', methods=['POST', 'GET'])
def home():
  return render_template("home.html")


@app.route("/content", methods=['POST', 'GET'])
def content():
  if request.method == "POST":

    button = request.form.get("content_button")
    if button == "login":
      print("Executing login command")
      global email
      global password
      global data
      global account_id
      email = request.form.get("email")
      #print("email:", email)
      password = request.form.get("password")
      #print("password:", password)
      logger.info(f"Executing login command for the email: {email}")
      result = mongodb.login(email, password)
      if result == "invalid_email":
        flash("Invalid email ID!!", "error")
        logger.error(f"Invalid email given: {email}")
        return redirect(url_for('home'))
      elif result == "invalid_password":
        flash("Invalid Password !!", "error")
        logger.error(f"Invalid password given for the email: {email}")
        return redirect(url_for('home'))
      else:
        logger.info(
            f"Logged in successfully for the email: {email} at {datetime.datetime.now()} "
        )
        #print("result got from mongo db:", result)
        data = result[0]
        account_id = result[1]
        #print("Local account_id:", account_id)
        #print("data", data)
        #print("account_id: ", account_id)
        return render_template("content.html", item_name=data)
    elif button == "remove":
      logger.info("remove operation selected by user")
      remove_app = request.form.get("removeapp")
      remove_user = request.form.get("removeuser")
      logger.info(
          f"User chose to remove: {remove_app}:{remove_user} from the account {account_id}"
      )
      response = mongodb.remove_entry(remove_app, remove_user, account_id)
      print(response)
      result = mongodb.login(email, password)
      data = result[0]
      print(data)
      return render_template("content.html", item_name=data)
    else:
      print("you used add me")
      print("account id from add", account_id)
      add_app = request.form.get("add_app")
      add_user = request.form.get("add_user")
      add_pword = request.form.get("add_pass")

      print(add_app)
      print("Global account_id:", account_id)
      logger.info(
          f"User chose to add: {add_app}:{add_user} for the account {account_id}"
      )
      response = mongodb.add_entry(add_app, add_user, add_pword, account_id,
                                   email)
      result = mongodb.login(email, password)
      data = result[0]
      print("DATA:", data)

      return render_template("content.html", item_name=data)


@app.route("/signup", methods=['POST', 'GET'])
def signup():
  return render_template("signup.html")


@app.route("/create_account", methods=['POST', 'GET'])
def create_account():
  email = request.form.get("email")
  user = request.form.get("user")
  admin_email = request.form.get("adminemail")
  password = request.form.get("password")
  mobile = request.form.get("mobile")
  print("admin email:", admin_email)
  result = mongodb.create_account(email, user, mobile, password, admin_email)
  result = str(result)

  if result == "True":
    logger.info(f"Creating account: {email}:{user}:{admin_email}")
    return render_template("home.html")
  elif result == "duplicate":
    logger.error(f"Email exists: {email}")
    print("signup result:", result)
    flash("ID Already Used!!", "error")
    return redirect(url_for('signup'))


@app.route("/forgot_password", methods=["POST", "GET"])
def forgot_password():
  logger.info("Forgot password is used by someone")
  return render_template("forgot_password.html")


current_session = {}


@app.route("/verify_otp", methods=["POST", "GET"])
def verify_otp():

  if request.method == "POST":
    request.form.get("send_otp")
    global otp
    global result
    global data
    data = {}
    global current_session
    email = request.form.get("email")
    print("Email to send OTP:", email)
    logger.info(f"OTP sent to: {email}")
    admin = request.form.get("adminemail")
    user = request.form.get("user")
    data["email"] = email
    data["admin"] = admin
    data["user"] = user
    import generate_otp
    result = generate_otp.generate_opt(email)
    #current_session["OTP"] = result
    print("OTP Result:", result)
    return render_template("forgot_password.html", otp=result, data=data)


@app.route("/validate_otp", methods=["POST", "GET"])
def validate_otp():
  if request.method == "POST":
    user = data["user"]
    email = data["email"]
    admin = data["admin"]
    data2 = {"user": user, "eamil": email, "admin": admin}
    print("From Validate OTP: ")
    print(user)
    print(email)
    print(admin)
    OTP = request.form.get("OTP")
    print("OTP from previous result:", result)
    if result == OTP:
      logger.info(f"OTP verified and directed to password reset: {email}")
      print("OTP Matched")
      return render_template("reset_password.html", data=data2)
    else:
      logger.info(f"OTP not valid for: {email}")
      print("OTP Does not match")
      flash("OTP Does not match!!", "error")
      return render_template("forgot_password.html")


@app.route("/reset_password", methods=["POST", "GET"])
def reset_password():
  if request.method == "POST":
    print("From Reset Password:")
    print(data)
    email = data["email"]
    admin = data["admin"]
    password = request.form.get("password")
    response = mongodb.reset_password(email, admin, password)
    if response == "Updated":
      logger.info(f"Password updated for email: {email}")
      flash("Password updated successfully!!")
      return render_template("home.html")
    else:
      logger.info(f"Unable to update password: {email}")
      flash("Unable to reset password, check the email ID!!")
      return render_template("forgot_password.html")


@app.route("/about")
def about():
  return render_template("about.html")


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080, debug=True)

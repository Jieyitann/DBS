from flask import Flask, request, session, Response
import pymysql 
from flask_login import login_user, login_required, logout_user
 
connection = pymysql.connect(host='localhost', user='root', password='password', database='insurancedata', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor) 
 
app = Flask(__name__) 
app.config['SECRET_KEY'] = '123456'

cursor = connection.cursor() 

@app.route('/login', methods=['POST'])
def login():
  data = request.json
  id = data.get('id')
  pw = data.get('password')
  cursor.execute(f'SELECT * FROM User WHERE EmployeeID = "{id}"')
  user = cursor.fetchone()
  if user: 
    if pw == user['Password']:
      login_user(user, remember=True)
      session['user'] = user
      return Response("User is logged in", status=200, mimetype='text/xml')
    else:
        return Response("Password is wrong", status=401, mimetype='text/xml')
  else:
      return Response("User does not exist", status=401, mimetype='text/xml')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    if 'user' in session:  
      session.pop('user',None) 
    return Response("Logout", status=200, mimetype='text/xml')

@app.route('/delete/<int:claim_id>', methods = ['POST'])
def delete(claim_id):
  cursor.execute(f'SELECT * FROM InsuranceClaims WHERE ClaimID = "{claim_id}"')
  claim = cursor.fetchone()
  if claim:
    cursor.execute(f'DELETE FROM InsuranceClaims WHERE ClaimID = {claim_id}')
    connection.commit()
    return Response("Claim has been successfully deleted", status=200, mimetype='text/xml')
  else:
    return Response("Record cannot be deleted", status=200, mimetype='text/xml')

if __name__ == '__main__':
    app.run(debug = True)

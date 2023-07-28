from flask import Flask,render_template,redirect,request,session
import urllib3
import json

backendserver='http://127.0.0.1:2000'

frontend=Flask(__name__)
frontend.secret_key='litam'

@frontend.route('/')
def homePage():
    return render_template('home.html')

@frontend.route('/signup')
def signupPage():
    return render_template('signup.html')

@frontend.route('/signupform',methods=['post'])
def signupform():
    name=request.form['name']
    email=request.form['email']
    phone=request.form['phone']
    gender=request.form['gender']
    password=request.form['password']
    print(name,email,phone,gender,password)
    apirequest=backendserver+'/register?Name='+name+'&Email='+email+'&Phone='+phone+'&Gender='+gender+'&Password='+password
    http=urllib3.PoolManager()
    response=http.request('get',apirequest)
    response=response.data.decode('utf-8')
    print(response)
    if response=='account exist':
        return render_template('signup.html',err='account already exist')
    return render_template('signup.html',res='Registered')

@frontend.route('/login')
def loginPage():
    return render_template('login.html')

@frontend.route('/loginform',methods=['post'])
def loginform():
    userid=request.form['userid']
    password=request.form['password']
    print(userid,password)
    apirequest=backendserver+'/login?UserID='+userid+'&Password='+password
    http=urllib3.PoolManager()
    response=http.request('get',apirequest)
    response=response.data.decode('utf-8')
    print(response)
    if(response=='True'):
        session['username']=userid
        return redirect('/enquiry')
        # return render_template('login.html',res='Login Valid')
    else:
        return render_template('login.html',err='Login Invalid')

@frontend.route('/enquiry',methods=['post'])
def enquiry():
    To=request.form['To']
    From=request.form['From']
    print(To,From)
    apirequest=backendserver+'/enquiry?To='+To+'&From='+From
    http=urllib3.PoolManager()
    response=http.request('get',apirequest)
    response=response.data.decode('utf-8')
    print(response)
    return render_template('available.html')


@frontend.route('/trainbtw',methods=['get'])
def trainbtw():
    To=request.form['To']
    From=request.form['From']
    print(To,From)
    apirequest=backendserver+'/login?To='+To+'&From='+From
    http=urllib3.PoolManager()
    response=http.request('get',apirequest)
    response=response.data.decode('utf-8')
    print(response)
    return redirect ('/available')


@frontend.route('/available')
def available():
    apirequest=backendserver+'/availablet'
    http=urllib3.PoolManager()
    response=http.request('post',apirequest)
    response=response.data.decode('utf-8')
    print(response)
    return render_template('available.html',dashboard_data=response,l=len(response))

@frontend.route('/enquiry')
def enquirypage():
    return render_template('enquiry.html')

@frontend.route('/logout')
def logoutpage():
    session['username']=None
    return redirect('/')

@frontend.route('/about')
def about():
    return render_template('about.html')

@frontend.route('/about')
def about():
    return render_template('about.html')


if __name__=="__main__":
    frontend.run(host='0.0.0.0',port=5001,debug=True)
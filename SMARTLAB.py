import random

from flask import Flask, render_template, request, session, redirect

from DBConnection import Db
import datetime
import os
import subprocess

from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2

app = Flask(__name__)
path1=r"C:\Users\user\PycharmProjects\untitled\static\photo\\"
app.secret_key="key"
@app.route('/')
def hello_world():
    return render_template("student/LOGIN.html")
@app.route('/logout')
def logout():
    session['lin']=""
    return render_template("student/LOGIN.html")
@app.route('/login', methods=(['post']))
def login():
    db=Db()
    username=request.form['name']
    password=request.form['password']
    qry="select * from login where username='"+username+"' and password='"+password+"'"
    result=db.selectOne(qry)
    if result==None:
        return ("invalid user")
    elif result['usertype']=="admin":
        session['lin']="lin"
        return redirect('/admin_home')
    elif result['usertype'] == "staff":
        session['lin'] = "lin"
        session['login_id']=result['login_id']
        session['username']=result['username']
        return redirect('/staff_home')
    elif result['usertype'] == "student":
        session['lin'] = "lin"
        session['login_id'] = result['login_id']
        return redirect('/student_home')


    else:
        return ("invalid user")


@app.route('/admin_home')
def admin_home():
    if session['lin']=="lin":
        return render_template('admin/admin_home.html')
    else:
        return render_template("student/LOGIN.html")
@app.route('/staff_home')
def staff_home():
    if session['lin'] == "lin":
        return render_template('staff/index1.html',d=session['username'])
    else:
        return render_template("student/LOGIN.html")
@app.route('/student_home')
def student_home():
    if session['lin'] == "lin":
         return render_template('student/student_home.html')
    else:
        return render_template("student/LOGIN.html")

@app.route('/add_dept')
def add_dept():
    if session['lin'] == "lin":
        return render_template("admin/Add_dept.html")
    else:
        return render_template("student/LOGIN.html")
@app.route('/add_dept1',methods=['POST'])
def add_dept1():
    if session['lin']=='lin':
        db=Db()
        department=request.form['dept_name']
        qry1=db.selectOne("select * from dept where dept_name='"+department+"'")
        if qry1 is None:
            qry="insert into dept values(NULL,'"+department+"')"
            db.insert(qry)
            return'''<script>alert("successfully added");window.location="/add_dept"</script>'''
        else:
            return '''<script>alert("Already added");window.location="/add_dept"</script>'''
    else:
        return render_template("student/LOGIN.html")

@app.route('/view_dept')
def view_dept():
    if session['lin'] == 'lin':
        db=Db()
        qry="select * from dept"
        result=db.select(qry)
        return render_template("admin/viewdept.html",value=result)
    else:
        return render_template("student/LOGIN.html")
@app.route('/delete_dept/<a>')
def delete_dept(a):
    if session['lin'] == 'lin':
       db=Db()
       db.delete("delete from dept where dept_id='"+a+"'" )
       return view_dept()
    else:
        return render_template("student/LOGIN.html")
@app.route('/add_course')
def add_course():
    if session['lin'] == 'lin':
        db=Db()
        qry="select * from dept"
        result=db.select(qry)
        return render_template("admin/ADDCOURSE.html",value=result)
    else:
        return render_template("student/LOGIN.html")
@app.route('/add_coursepost',methods=['post'])
def add_coursepost():
    if session['lin'] == 'lin':
        db=Db()
        did=request.form['course_name']
        c_name=request.form['course']
        qry1 = db.selectOne("select * from course where c_name='" + c_name + "'")
        if qry1 is None:
          qry = "insert into course values(NULL,'"+did+"', '" + c_name+ "')"
          db.insert(qry)
          return '''<script>alert("successfully added");window.location="/add_course"</script>'''
        else:
          return '''<script>alert("Already added");window.location="/add_course"</script>'''
    else:
        return render_template("student/LOGIN.html")


@app.route('/view_course')
def view_course():
    if session['lin'] == 'lin':
        db=Db()
    # qry="select * from course"
        result=db.select("select * from course,dept where dept.dept_id=course.did")
        return render_template("admin/viewcourse.html",value=result)
    else:
        return render_template("student/LOGIN.html")
@app.route('/delete_course/<a>')
def delete_course(a):
    if session['lin'] == 'lin':
        db=Db()
        db.delete("delete from course where cid='"+a+"'")
        return '''<script>alert('deleted');window.location="/view_course"</script>'''
    else:
        return render_template("student/LOGIN.html")
@app.route('/edit_course/<cid>')
def edit_course(cid):
    if session['lin'] == 'lin':
        db=Db()
        qry=("select * from course where cid='"+cid+"'")
        result=db.selectOne(qry)
        qry1=db.select("select * from dept ")
       # print(result,qry1)
    # did=result['did']
    # session['did']=did
        return render_template("admin/editcourse.html",data=result,data1=qry1)
    else:
        return render_template("student/LOGIN.html")
@app.route('/edit_course1/<a>',methods=['post'])
def edit_course1(a):
    if session['lin'] == 'lin':
        db=Db()
        c_name = request.form['course']
        dept_name=request.form['course_name']
        qry="update course set c_name='"+c_name+"',did='"+dept_name+"' where cid='"+a+"'"
        db.update(qry)
        return '''<script>alert('updated');window.location="/view_course"</script>'''
    else:
        return render_template("student/LOGIN.html")

@app.route('/add_lab1')
def add_lab1():
    if session['lin'] == 'lin':
      return render_template("admin/Addlab.html")
    else:
        return render_template("student/LOGIN.html")
@app.route('/add_lab', methods=['post'])
def add_lab():
    if session['lin'] == 'lin':
        db=Db()
        lab_name=request.form['labname']
        qry1=db.selectOne("select * from lab where lab_name='"+lab_name+"' ")
        if qry1 is None:
         qry="insert into lab values('','"+lab_name+"')"
         db.insert(qry)
         return '''<script>alert("successfully added");window.location="/admin_home"</script>'''
        else:
         return '''<script>alert("Already added");window.location="/add_lab1"</script>'''
    else:
     return render_template("student/LOGIN.html")

@app.route('/view_lab')
def view_lab():
    if session['lin'] == 'lin':
        db=Db()
        qry="select * from lab"
        result=db.select(qry)
        return render_template("admin/viewlab.html",value=result)
    else:
        return render_template("student/LOGIN.html")
@app.route('/delete/<a>')
def delete(a):
    if session['lin'] == 'lin':
        db=Db()
        db.delete("delete from lab where lab_id='"+a+"'")
        return view_lab()
    else:
        return render_template("student/LOGIN.html")
@app.route('/add_staff')
def add_staff():
    if session['lin'] == 'lin':
      db=Db()
      qry=db.select("select * from dept")
      return render_template("admin/Addstaff.html",qry1=qry)
    else:
        return render_template("student/LOGIN.html")
@app.route('/add_staff1',methods=['post'])
def add_staff1():
    if session['lin'] == 'lin':
     db=Db()
     staff_name=request.form['staff_name']
     staff_dept_name=request.form['select']
     staff_email=request.form['staff_email']
     staff_photo=request.files['fileField']
     date=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
     staff_photo.save(path1+date+".jpg")
     path="/static/photo/"+date+".jpg"
     staff_phone=request.form['staff_phone']
     password=random.randint(0000,9999)
     qr="insert into login VALUES ('','"+staff_email+"','"+str(password)+"','staff')"
     db.insert(qr)
     qry="insert into staff values('','"+staff_name+"','"+staff_dept_name+"','"+staff_email+"','"+str(path)+"','"+staff_phone+"')"
     db.insert(qry)
     return '''<script>alert("successfully added");window.location="/admin_home"</script>'''
    else:
     return render_template("student/LOGIN.html")


@app.route('/view_staff')
def view_staff():
    if session['lin'] == 'lin':
        db=Db()
        qry="SELECT staff.*,dept.dept_name FROM dept,staff where staff.staff_dept_id=dept.dept_id"
        result = db.select(qry)
        return render_template("admin/viewstaff.html", value=result)
    else:
        return render_template("student/LOGIN.html")
@app.route('/delete_staff/<a>')
def delete_staff(a):
    if session['lin'] == 'lin':
        db=Db()
        db.delete("delete from staff where staff_id='"+a+"'")
        return view_staff()
    else:
        return render_template("student/LOGIN.html")
@app.route('/edit_staff/<a>')
def edit_staff(a):
    if session['lin'] == 'lin':
        db=Db()
        qry=db.selectOne("SELECT staff.*,dept.dept_name FROM dept,staff where staff.staff_dept_id=dept.dept_id and staff.staff_id='"+a+"'")
        return render_template("admin/Editstaff.html",data=qry)
    else:
        return render_template("student/LOGIN.html")
@app.route('/edit_staff1/<a>',methods=['post'])
def edit_staff1(a):
    if session['lin'] == 'lin':
        db=Db()
        staff_name=request.form['staff_name']
    #staff_dept_name=request.form['select']
        staff_email=request.form['staff_email']
        staff_photo=request.files['fileField']
        date=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        staff_photo.save(path1+date+".jpg")
        path="/static/photo/"+date+".jpg"
        staff_phone=request.form['staff_phone']
        qry="update staff set staff_name='"+staff_name+"',staff_email='"+staff_email+"',staff_photo='"+path+"',staff_phone='"+staff_phone+"'where staff_id='"+a+"' "
        db.update(qry)
        return view_staff()
    else:
        return render_template("student/LOGIN.html")
@app.route('/view_staff_sreach',methods=['post'])
def view_staff_sreach():
    if session['lin'] == 'lin':
        db=Db()
        n=request.form['n1']
        qry="SELECT staff.*,dept.dept_name FROM dept,staff where staff.staff_dept_id=dept.dept_id and dept.dept_name like '%"+n+"%'  "
        result = db.select(qry)
        return render_template("admin/viewstaff.html", value=result)
    else:
        return   render_template("student/LOGIN.html")
@app.route('/add_student')
def add_student():
    if session['lin'] == 'lin':
        db=Db()
        qry="select * from course"
        res=db.select(qry)
        return render_template("admin/Addstudent.html",qry1=res)
    else:
       return render_template("student/LOGIN.html")
@app.route('/add_student1',methods=['post'])
def add_student1():
    if session['lin'] == 'lin':
        db=Db()
        student_name=request.form['student_name']
        course_name=request.form['select']
        student_sem=request.form['student_sem']
        student_email=request.form['student_email']
        student_photo=request.files['fileField']
        date=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        student_photo.save(path1+date+".jpg")
        path="/static/photo/"+date+".jpg"
        student_phone=request.form['student_number']
        student_year=request.form['student_year']
        qry = "insert into student values('','" + student_name + "','" + course_name + "','" + student_sem+ "','"+student_email+"','"+ str(path) + "','" + student_phone+ "','"+student_year+"')"
        db.insert(qry)
        return '''<script>alert("successfully added");window.location="/admin_home"</script>'''
    else:
       return render_template("student/LOGIN.html")

@app.route('/view_student')
def view_student():
    if session['lin'] == 'lin':
        db=Db()
        qry="SELECT student.*,course.c_name from course,student where student.student_course_id=course.cid"
        result=db.select(qry)
        return render_template("admin/viewstudent.html",value1=result)
    else:
       return render_template("student/LOGIN.html")
@app.route('/delete_student/<a>')
def delete_student(a):
    if session['lin'] == 'lin':
        db=Db()
        db.delete("delete from student where student_id='"+a+"'")
        return '''<script>alert('deleted');window.location="/view_student"</script>'''
    else:
       return render_template("student/LOGIN.html")
@app.route('/edit_student/<a>')
def edit_student(a):
    if session['lin'] == 'lin':
      db=Db()
      qry = db.selectOne("SELECT student.*,course.c_name FROM course,student where student.student_course_id=course.cid and student.student_id='" + a + "'")
      return render_template("admin/edit_student.html", data=qry)
    else:
     return render_template("student/LOGIN.html")
@app.route('/edit_student1/<a>',methods=['post'])
def edit_student1(a):
    if session['lin'] == 'lin':
      db=Db()
      student_name = request.form['student_name']
    # c_name = request.form['select']
      student_sem = request.form['student_sem']
      student_email = request.form['student_email']
      student_photo = request.files['fileField']
      student_number = request.form['student_number']
      student_year = request.form['student_year']
      if request.files is not None:
         if student_photo.filename != "":
            date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            student_photo.save(path1+ date + ".jpg")
            path = "/static/photo/" + date + ".jpg"

            qry="update student set student_name='"+student_name+"',student_sem='"+student_sem+"',student_email='"+student_email+"',student_photo='"+str(path)+"',student_number='"+student_number+"',student_year='"+student_year+"' where student_id='"+a+"'"
            db.update(qry)
            return view_student()
         else:
            qry = "update student set student_name='" + student_name + "',student_sem='" + student_sem + "',student_email='" + student_email + "',student_number='" + student_number + "',student_year='" + student_year + "' where student_id='" + a + "'"
            db.update(qry)
            return  view_student()
      else:
            qry = "update student set student_name='" + student_name + "',student_sem='" + student_sem + "',student_email='" + student_email + "',student_number='" + student_number + "',student_year='" + student_year + "' where student_id='" + a + "'"
            db.update(qry)
            return view_student()
    else:
      return render_template("student/LOGIN.html")
@app.route('/add_subject')
def add_subject():
    if session['lin'] == 'lin':
        db = Db()
        qry = db.select("select * from course")
        qry1 = db.select("select * from lab")
        qry2= db.select("select student_sem from student")
        return render_template("admin/Addsubject.html", val=qry, value=qry1,data=qry2)
    else:
     return render_template("student/LOGIN.html")
@app.route('/add_subject1',methods=['post'])
def add_subject1():
    if session['lin'] == 'lin':
        db=Db()
        sub_name=request.form['sub_id']
        s_course_name=request.form['select']
        s_lab_name=request.form['select2']
        sem=request.form['select3']
        qry="insert into subject values('','"+sub_name+"','"+s_course_name+"','"+s_lab_name+"','"+sem+"')"
        db.insert(qry)
        return '''<script>alert("successfully added");window.location="/admin_home"</script>'''
    else:
        return render_template("student/LOGIN.html")

@app.route('/view_subject')
def view_subject():
    if session['lin'] == 'lin':
        db=Db()
        qry = "SELECT * from course, lab,subject where subject.s_course_id=course.cid and subject.s_course_id=lab.lab_id "
        result = db.select(qry)
        return render_template("admin/viewsubject.html",value=result)
    else:
        return render_template("student/LOGIN.html")
@app.route('/delete_subject/<a>')
def delete_subject(a):
    if session['lin'] == 'lin':
        db=Db()
        db.delete("delete from subject where sub_id='"+a+"'")
        return '''<script>alert('deleted');window.location="/view_subject"</script>'''
    else:
        return render_template("student/LOGIN.html")
@app.route('/edit_subject/<a>',methods=["get"])
def edit_subject(a):
    if session['lin'] == 'lin':
     db=Db()
     qry = db.selectOne("SELECT subject.*,course.c_name,lab.lab_name from course, lab,subject where subject.s_course_id=course.cid and subject.s_course_id=lab.lab_id and subject.sub_id='"+a+"'")
     return render_template("admin/edit_subject.html", data=qry)
    else:
        return render_template("student/LOGIN.html")
@app.route('/edit_subject1/<a>',methods=['post'])
def edit_subject1(a):
    if session['lin'] == 'lin':
      db=Db()
      sub_name=request.form['sub_name']
   #s_course_name = request.form['select']
   #s_lab_name = request.form['select2']
      qry="update subject set sub_name='"+sub_name+"' where sub_id='"+a+"'"
      db.update(qry)
      return '''<script>alert("edited");window.location="/"</script>'''
    else:
        return render_template("student/LOGIN.html")
@app.route('/add_labcharge')
def add_labcharge():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from lab")
        qry1=db.select("select * from staff")
        return render_template("admin/Addlabcharge.html", data=qry, data1=qry1)
    else:
        return render_template("student/LOGIN.html")
@app.route('/add_labcharge1', methods=['post'])
def add_labcharge1():
    if session['lin'] == 'lin':
        db=Db()
        lab_name=request.form['select']
        staff_name=request.form['select2']
        qry1=db.selectOne("select * from lab_in_charge where l_lab_id='"+lab_name+"' and l_staff_id='"+staff_name+"' ")
        if qry1 is None:
            qry="insert into lab_in_charge(l_lab_id,l_staff_id) values('"+lab_name+"','"+staff_name+"')"
            db.insert(qry)
            return '''<script>alert("successfully added");window.location="/admin_home"</script>'''
        else:
            return "already"
    else:
        return render_template("student/LOGIN.html")
@app.route('/view_labcharge')
def view_labcharge():
    if session['lin'] == 'lin':
        db=Db()
        qry=" select lab_in_charge.*,lab.lab_name,staff.staff_name from lab,staff,lab_in_charge where lab_in_charge.l_lab_id=lab.lab_id and lab_in_charge.l_staff_id=staff.staff_id"
        result = db.select(qry)
        return render_template("admin/Viewlabcharge.html",value=result)
    else:
        return render_template("student/LOGIN.html")
@app.route('/delete_lab_charge/<a>')
def delete_lab_charge(a):
    if session['lin'] == 'lin':
        db = Db()
        db.delete("delete from lab_in_charge where l_in_c_id='" + a + "'")
        return '''<script>alert('deleted');window.location="/view_labcharge"</script>'''
    else:
        return render_template("student/LOGIN.html")
@app.route('/add_labexam')
def add_labexam():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select *from lab")
        return render_template("admin/Addlabexam.html", data=qry)
    else:
        return render_template("student/LOGIN.html")
@app.route('/add_labexam11/<eid>')
def add_labexam11(eid):
    if session['lin'] == 'lin':
        db=Db()
        session['labids']=eid
        qry=db.select("select *from course")
        return render_template("admin/ajaxcourse.html", data1=qry)
    else:
        return render_template("student/LOGIN.html")
@app.route('/ajaxsem/<eid>')
def ajaxsem(eid):
    if session['lin'] == 'lin':
        db=Db()
        session['courseid']=eid
        return render_template("admin/ajaxsem.html")
    else:
        return render_template("student/LOGIN.html")
@app.route('/ajaxsub/<eid>')
def ajaxsub(eid):
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from subject where s_course_id='"+str(session['courseid'])+"' and s_lab_id='"+str(session['labids'])+"' and semester='"+eid+"'")
        return render_template("admin/ajaxsub.html",data1=qry)
    else:
        return render_template("student/LOGIN.html")

@app.route('/add_labexam1',methods=['post'])
def add_labexam1():
    if session['lin'] == 'lin':
      db=Db()
      lab_name=request.form['select']
      lab_date=request.form['lab_date']
      lab_time=request.form['lab_time']
      subject_name=request.form['select2']
      qry2=db.selectOne("select * from labexam where l_date='"+lab_date+"' and l_time='"+lab_time+"' and l_subject_id='"+subject_name+"' and l_status='pending'")
      if qry2 is None:
         qry="insert into labexam VALUES ('','"+lab_date+"','"+lab_time+"','"+subject_name+"','pending')"
         db.insert(qry)
         return '''<script>alert("successfully added");window.location="/add_labexam"</script>'''
      else:
         return '''<script>alert("successfully added");window.location="/add_labexam"</script>'''
    else:
         return render_template("student/LOGIN.html")

@app.route('/view_labexam')
def view_labexam():
    if session['lin'] == 'lin':
     db=Db()
     qry2=db.select("select * from lab")
     return render_template("admin/viewlabexam.html",data=qry2)
    else:
        return render_template("student/LOGIN.html")
@app.route('/view_labexam1',methods=['post','get'])
def view_labexam1():
    if session['lin'] == 'lin':
     db=Db()
     lab_name=request.form['select']
     course_name=request.form['sub']
     sem=request.form['select3']
     sub_name=request.form['select2']
     qry2=db.select("select *  from subject,course,lab,labexam where labexam.l_subject_id=subject.sub_id and subject.s_lab_id=lab.lab_id and subject.s_course_id=course.cid and subject.s_lab_id='"+lab_name+"' and course.cid='"+course_name+"' and subject.sub_id='"+sub_name+"' and subject.semester='"+sem+"'")
     #print(qry2)
     return render_template("admin/viewlabexam.html",value=qry2)
    else:
        return render_template("student/LOGIN.html")
@app.route('/delete_labexam/<a>')
def delete_labexam(a):
    if session['lin'] == 'lin':
     db = Db()
     db.delete("delete from labexam where leid='" + a + "'")
     return view_labexam()
    else:
     return render_template("student/LOGIN.html")
@app.route('/edit_labexam/<a>',methods=["get"])
def edit_labexam(a):
    if session['lin'] == 'lin':
     db=Db()
     qry = db.selectOne("select labexam.*,lab.lab_name,subject.sub_name from subject,lab,labexam where subject.s_lab_id=lab.lab_id and  labexam.l_subject_id=subject.sub_id and labexam.leid='"+a+"'")
     return render_template("admin/edit_labexam.html", data=qry)
    else:
     return render_template("student/LOGIN.html")
@app.route('/edit_labexam1/<a>',methods=['post'])
def edit_labexam1(a):
    if session['lin'] == 'lin':
      db=Db()
     #lab_name=request.form['select']
      lab_date=request.form['lab_date']
      lab_time=request.form['lab_time']
      subject_name=request.form['lab_status']
      qry = "update labexam set l_date='" + lab_date + "',l_time='"+lab_time+"',l_status='"+subject_name+"' where leid='" + a + "'"
      db.update(qry)
      return '''<script>alert("edited");window.location="/view_labexam"</script>'''
    else:
        return render_template("student/LOGIN.html")
@app.route('/view_system/<i>')
def view_system(i):
    if session['lin'] == 'lin':
     db=Db()
     qry="select system.*,lab.lab_id from system,lab where system.lab_id=lab.lab_id and lab.lab_id ='"+i+"' "
     result = db.select(qry)
     return render_template("admin/viewsystem1.html", value=result)
    else:
     return render_template("student/LOGIN.html")
@app.route('/view_allocatedstaff')
def view_allocatedstaff():
    if session['lin'] == 'lin':
        db=Db()
        qry="SELECT * FROM lab left join subject on lab.lab_id=subject.s_lab_id Left join course on course.cid=subject.s_course_id left join lab_schedule on lab_schedule.lab_subject_id=subject.sub_id left join staff on staff.staff_id=lab_schedule.staff_id"
        result = db.select(qry)
        # print(result)
        return render_template("Admin/allocate_staff.html", value=result)
    else:
        return render_template("student/LOGIN.html")

@app.route('/addstaff/<i>/<j>')
def addstaff(i,j):
    if session['lin'] == 'lin':
     db=Db()
     qry=db.select("select * from course,staff where course.did=staff.staff_dept_id and course.cid='"+i+"'")
     return render_template("Admin/addlabschedule.html", value=qry,s=j)
    else:
        return render_template("student/LOGIN.html")

@app.route('/addstaff1/<s>', methods=['post'])
def addstaff1(s):
    if session['lin'] == 'lin':
     db=Db()
     staff=request.form['s']
     times=request.form['t']
     qry=db.insert("insert into lab_schedule(lab_subject_id,staff_id,times) values('"+s+"','"+staff+"','"+times+"')  ")
     return view_allocatedstaff()
    else:
        return render_template("student/LOGIN.html")
@app.route('/delete_staff1/<a>')
def delete_staff1(a):
    if session['lin'] == 'lin':
     db=Db()
     db.delete("delete from lab_schedule where lab_subject_id='" + a + "'")
     return view_allocatedstaff()
    else:
        return render_template("student/LOGIN.html")






# ===================================================================================================================================================staff

@app.route('/viewallocated_lab')
def view_allocatedlab():
    if session['lin'] == 'lin':
        db=Db()
        qry="select * from lab join lab_in_charge on lab.lab_id=lab_in_charge.l_lab_id where lab_in_charge.l_staff_id='"+str(session['login_id'])+"'  "
        result=db.select(qry)
        #print(result)
        return render_template("staff/viewallocatedlab.html",value=result)
    else:
        return render_template("student/LOGIN.html")
@app.route('/addsystem_mgt')
def addsystem_mgt():
    if session['lin'] == 'lin':
        db = Db()
        qry= db.select("select * from  lab join lab_in_charge on lab.lab_id=lab_in_charge.l_lab_id where lab_in_charge.l_staff_id='"+str(session['login_id'])+"'")
        return render_template("staff/ADDsystemmgt.html", val=qry)
    else:
        return render_template("student/LOGIN.html")
@app.route('/addsystem_mgt1',methods=['post'])
def add_systemmgt1():
    if session['lin'] == 'lin':
        db=Db()
        system_mac = request.form['textfield']
        lab_name=request.form['select']
        details=request.files['textfield2']
        status=request.form['textfield3']
        date = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        details.save(path1 + date + ".jpg")
        path = "/static/photo/" + date + ".jpg"
        qry="insert into system values('','"+system_mac+"','"+lab_name+"','"+str(path)+"','"+status+"')"
        db.insert(qry)
        return '''<script>alert("successfully added");window.location="/staff_home"</script>'''

    else:
        return render_template("student/LOGIN.html")


@app.route('/viewsystem_mgt')
def viewsystem_mgt():
    if session['lin'] == 'lin':
        db=Db()
        qry="SELECT system.*,lab.lab_name from lab,system where system.lab_id=lab.lab_id"
        result=db.select(qry)
        return render_template("staff/viewsystemmgt.html",value=result)
    else:
        return render_template("student/LOGIN.html")
@app.route('/delete_viewsystemmgt/<a>')
def delete_viewsystemmgt(a):
    if session['lin'] == 'lin':
        db = Db()
        db.delete("delete from system where s_id='" + a + "'")
        return '''<script>alert("successfully deleted");window.location="/staff_home"</script>'''
    else:
        return render_template("student/LOGIN.html")
@app.route('/viewlab_schedule')
def viewlab_schedule():
    if session['lin'] == 'lin':
        db=Db()
        qry="select * from lab_schedule join subject on lab_schedule.lab_subject_id=subject.sub_id join lab on lab.lab_id=subject.s_lab_id join lab_in_charge on lab_in_charge.l_lab_id=lab.lab_id join staff on staff.staff_id=lab_in_charge.l_staff_id join course on course.cid=subject.s_course_id where lab_schedule.staff_id='"+str(session['login_id'])+"'"
        result=db.select(qry)
        #print(result)
        return render_template("staff/viewlabschedule.html", value=result)
    else:
        return render_template("student/LOGIN.html")
@app.route('/viewrunning_app')
def viewrunning_app():
    if session['lin'] == 'lin':
        db=Db()
        qry="select * from applog"
        result=db.select(qry)
        return render_template("staff/viewrunningapp.html",value=result)
    else:
        return render_template("student/LOGIN.html")
@app.route('/ppost',methods=['post'])
def ppost():
    if session['lin'] == 'lin':

        db=Db()
        s=request.form['s']
        if s=='Internet Explorer':
            db.insert("insert into applog values ( '','"+str(session['login_id'])+"','1','"+s+"',now());")
            subprocess.Popen("C:\Program Files (x86)\Internet Explorer\iexplore.exe")
        qry="select * from applog"
        result=db.select(qry)
        return render_template("staff/viewrunningapp.html",value=result)
    else:
        return render_template("student/LOGIN.html")
@app.route('/viewscreen_capture')
def viewscreen_capture():
    if session['lin'] == 'lin':
        db=Db()
        qry="select * from screencapture, system,lab_in_charge where screencapture.sys_id=system.s_id and lab_in_charge.l_lab_id=system.lab_id and lab_in_charge.l_staff_id='"+str(session['login_id'])+"'"
        result=db.select(qry)
        return render_template('staff/viewscreencapture.html',value=result)
    else:
        return render_template("student/LOGIN.html")

@app.route('/capreq',methods=['post'])
def capreq():
    if session['lin'] == 'lin':
        db=Db()
        db.insert("insert into screencaptrequest values('','6',curdate())")
        return viewscreen_capture()
    else:
        return render_template("student/LOGIN.html")

@app.route('/view_keyboardlog')
def view_keyboardlog():
    if session['lin'] == 'lin':
        db=Db()
        qry="select * from system,keylogs,lab_in_charge where system.s_id=keylogs.sys_id and system.lab_id=lab_in_charge.l_lab_id and lab_in_charge.l_staff_id='"+str(session['login_id'])+"'"
        result=db.select(qry)
        return render_template('staff/viewkeyboard.html', value=result)
    else:
        return render_template("student/LOGIN.html")
@app.route('/invoke_cmd')
def invoke_cmd():
    if session['lin'] == 'lin':
        db=Db()
        qry="select * from command "
        result=db.select(qry)
        return render_template('staff/invokingcommand.html', value=result)
    else:
        return render_template("student/LOGIN.html")

@app.route('/add_cmd')
def add_cmd():
        if session['lin'] == 'lin':
            db=Db()
            qry = "select * from command "
            qry1 = "select * from staff"
            result = db.select(qry)
            return render_template('staff/addinvoke.html', value=result)
        else:
            return render_template("student/LOGIN.html")
@app.route('/invoke/<a>')
def invoke(a):
    if session['lin'] == 'lin':
        db=Db()
        qry = "insert into invokecommand values('','" + a + "','" +str(session['login_id'])+"','1')"
        db.insert(qry)
        return '''<script>alert("successfully added");window.location="/invoke_cmd"</script>'''
    else:
        return render_template("student/LOGIN.html")

@app.route('/capture_img')
def capture_img():
    if session['lin'] == 'lin':
        db=Db()
        qry="select * from image_capture,system where image_capture.sys_id=system.s_id "
        result = db.select(qry)
        return render_template('staff/captureimage.html', value=result)
    else:
        return render_template("student/LOGIN.html")

@app.route('/cap_img',methods=['post'])
def cap_img():
    if session['lin'] == 'lin':
        db=Db()
        url=""
        import datetime
        d = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        #print("[INFO] starting video stream...")
        vs = VideoStream(src=0).start()
        time.sleep(2.0)
        img_counter = 0
        # loop over the frames from the video stream
        while True:
            # grab the frame from the threaded video stream and resize it
            # to have a maximum width of 400 pixels
            frame = vs.read()
            frame = imutils.resize(frame, width=400)
            imgname = path1+d+".jpg".format(img_counter)
            cv2.imwrite(imgname, frame)
            url="/static/photo/"+d+".jpg"

            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
            # db=Db()

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break

        cv2.destroyAllWindows()
        vs.stop()
        db.insert("insert into image_capture values('','6','" + url + "',now())")

        return capture_img()
    else:
        return render_template("student/LOGIN.html")
@app.route('/add_apppermission')
def add_apppermission():
    if session['lin'] == 'lin':
        db=Db()
        qry = db.select("select *from staff")
        import psutil
        k=[]
        for proc in psutil.process_iter():
            #print(proc.name())
            try:
                processName = proc.name()
                processID = proc.pid
                k.append(processName)
            except Exception as e:
                print(e)

        return render_template("staff/Addapplicationpermission.html", val=qry,k1=k)
    else:
        return render_template("student/LOGIN.html")
@app.route('/add_apppermission1',methods=['post'])
def add_apppermission1():
    if session['lin'] == 'lin':
        db=Db()
        appname=request.form['textfield2']
        qry="insert into app_permission values('','"+appname+"','"+str(session['login_id'])+"',now())"
        db.insert(qry)
        return '''<script>alert("successfully added");window.location="/add_apppermission"</script>'''
    else:
        return render_template("student/LOGIN.html")
@app.route('/view_apppermission')
def view_apppermission():
    if session['lin'] == 'lin':
        db=Db()
        qry="select app_permission.*,staff.* from app_permission join staff on app_permission.staff_id=staff.staff_id WHERE staff.staff_id='"+str(session['login_id'])+"' "
        result = db.select(qry)
        return render_template('staff/Viewapppermission.html', value=result)
    else:
        return render_template("student/LOGIN.html")
@app.route('/delete_apppermission/<a>')
def delete_apppermission(a):
    if session['lin'] == 'lin':
        db = Db()
        db.delete("delete from app_permission where block_id='" + a + "'")
        return view_apppermission ()
    else:
        return render_template("student/LOGIN.html")
@app.route('/add_labexperiment')
def add_labexperiment():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from system")
        qry1=db.select(("select * from staff"))
        return render_template("staff/labexperiment.html", val=qry,value=qry1)
    else:
        return render_template("student/LOGIN.html")
@app.route('/add_labexperiment1', methods=['post'])
def add_labexperiment1():
    if session['lin'] == 'lin':
        db=Db()
        staff_name=request.form['select']
        question=request.form['textfield']
        system_mac=request.form['select2']
        status=request.form['textfield2']
        l_datetime=request.form['textfield3']
        qry="insert into lab_experiment values('','"+staff_name+"','"+question+"','"+system_mac+"','"+status+"','"+l_datetime+"')"
        db.insert(qry)
        return '<script>alert("successfully added");window.location="/add_labexperiment"</script>'
    else:
        return render_template("student/LOGIN.html")
@app.route('/add_labexamsystem')
def add_labexamsystem():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from student")
        qry1= db.select("select * from system")
        qry2= db.select("select * from subject")
        return render_template("staff/Addlabsystemallocation.html",value1=qry,value2=qry1,value3=qry2)
    else:
        return render_template("student/LOGIN.html")
@app.route('/add_labexamsystem1',methods=['post'])
def add_labexamsystem1():
    if session['lin'] == 'lin':
        db=Db()
        subject_name=request.form['select3']
        date_lab=request.form['textfield']
        time=request.form['textfield2']
        qry="insert into systemexam values('','"+subject_name+"','"+date_lab+"','"+time+"')"
        db.insert(qry)
        return '<script>alert("successfully added");window.location="/add_labexamsystem"</script>'
    else:
        return render_template("student/LOGIN.html")
@app.route('/view_labexamsystem')
def view_labexamsystem():
    if session['lin'] == 'lin':
        db=Db()
        qry="select * from systemexam,system,subject where systemexam.lab_subject_id=subject.sub_id  and subject.s_lab_id=system.lab_id"
        result = db.select(qry)
        return render_template('staff/Viewlabexamsystem.html', value=result)
    else:
        return render_template("student/LOGIN.html")
@app.route('/delete_labexamsystem/<a>')
def delete_labexamsystem(a):
    if session['lin'] == 'lin':
        db=Db()
        db.delete("delete from systemexam where timetable_id='"+a+"'")
        return view_labexamsystem()
    else:
        return render_template("student/LOGIN.html")

@app.route('/view_attendance')
def view_attendance():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.selectOne("select * from lab_in_charge,lab where lab.lab_id=lab_in_charge.l_lab_id and lab_in_charge.l_staff_id='"+str(session['login_id'])+"'")
        q=qry['lab_id']
        session['labids1']=q
        qry1=db.select("select * from subject,course where course.cid=subject.s_course_id and  s_lab_id='"+str(q)+"' group by subject.s_course_id")
        return render_template("staff/VIEWattendance.html",d=qry1)
    else:
        return render_template("student/LOGIN.html")

@app.route('/ajaxsem1/<eid>')
def ajaxsem1(eid):
    if session['lin'] == 'lin':
        db=Db()
        session['courseid']=eid
        return render_template("staff/ajaxsem.html")
    else:
        return render_template("student/LOGIN.html")

@app.route('/ajaxsub1/<eid>')
def ajaxsub1(eid):
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from subject where s_course_id='"+str(session['courseid'])+"' and s_lab_id='"+str(session['labids1'])+"' and semester='"+eid+"'")
        return render_template("staff/ajaxsub.html",data1=qry)
    else:
        return render_template("student/LOGIN.html")
# @app.route('/ajaxyear/<eid>')
# def ajaxyear(eid):
#     db=Db()
#     qry=db.select("select * from student where s_course_id='"+str(session['courseid'])+"' and s_lab_id='"+str(session['labids1'])+"' and semester='"+eid+"' and student_id='"+eid+"'")
#     return render_template("staff/ajaxyear.html", data1=qry)

@app.route('/view_attendence_post',methods=['post'])
def view_attendence_post():
    if session['lin'] == 'lin':
        db=Db()
        course=request.form['c']
        sem=request.form['sem']
        subject=request.form['sub']
        year=request.form['year']
        qry2=db.select("select student.*,count(stud_id) as total_att,attendence.* from student,rfid,attendence where student.student_id=rfid.stud_id and rfid.id=attendence.rid and student.student_course_id=3 and student.student_sem='"+sem+"'and student.student_year='"+year+"' and attendence.subid='"+subject+"'")
        # qry2=db.select("select student.*,count(stud_id) as total_att,subject.*,course.*,attendence.* from student,rfid,subject,course,attendence where student.student_course_id='"+course+"' and student.student_sem='"+sem+"' and student.student_year='"+year+"' and subject.s_course_id=course.cid and subject.sub_id='"+subject+"' and rfid.stud_id=student.student_id and rfid.id=attendence.rid  group by rfid.stud_id")
        if qry2 is not None:

            return render_template("staff/VIEWattendance.html",data=qry2)
        else:
            return '''<script>alert("No data");window.location="/view_attendance"</script>'''
    else:
        return render_template("student/LOGIN.html")

@app.route('/send_request')
def send_request():
        if session['lin'] == 'lin':
            db = Db()
            qry = db.select("select * from lab")
            qry1 = db.select("select * from staff")
            return render_template("admin/Addlabcharge.html", data=qry, data1=qry1)
        else:
            return render_template("student/LOGIN.html")


#==========================================================================================================================================================
@app.route('/viewlabsubschedule')
def viewlabsubschedule():
    if session['lin'] == 'lin':
        db=Db()
        qry="select subject.sub_name,lab_schedule.*,staff.staff_name from subject,lab_schedule,staff where subject.sub_id=lab_schedule.lab_subject_id and lab_schedule.staff_id=staff.staff_id"
        result = db.select(qry)
        return render_template('student/viewlabsubschedule.html', value=result)
    else:
        return render_template("student/LOGIN.html")

@app.route('/viewexamschedule')
def viewexamschedule():
    if session['lin'] == 'lin':
        db=Db()
        q=db.selectOne("select * from student where student_id='"+str(session['login_id'])+"'")
       # print(q)
        qry="select subject.sub_name,lab.lab_name,labexam.*,systemexam.* from lab,subject,systemexam,labexam where lab.lab_id=subject.s_lab_id and subject.sub_id=labexam.l_subject_id and systemexam.lab_subject_id=subject.sub_id and subject.s_course_id='"+str(q['student_course_id'])+"' and subject.semester='"+str(q['student_sem'])+"'"
        result = db.select(qry)
        return render_template('student/viewexamschedule.html', value=result)
    else:
        return render_template("student/LOGIN.html")




if __name__ == '__main__':
    app.run(debug=True,port=4000)

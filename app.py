from flask import Flask, render_template, request
import pickle
import os
from database import all_students
app = Flask(__name__)


@app.route("/")
def main():
    return render_template('_page.html')
@app.route("/clogin",methods=["GET","POST"])
def clogin():
    #all_class=[f.name for f in os.scandir("C:\\Divyaman\\img_detect\\train_folder") if f.is_dir() ]
    if request.method=='POST':
        data=request.form.to_dict()
        usr=request.form["usr"]
        password=request.form["password"]
        if (usr=="spsv1" and password=="123dt"):
            return render_template('main_page.html')
        else:
            return("Check Your Entered Details !!!")

app.config["IMAGE_UPLOADS"]="uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"]=["PNG","JPG","JPEG","png","jpg","jpeg"]


def allow(filename):
    if not '.' in filename:
        return False
    extension = filename.rsplit(".",1)[1]

    if extension in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route("/upload",methods=["POST","GET"])
def upload():
    all_class=[f.name for f in os.scandir("train_folder") if f.is_dir() ]
    data=request.form.to_dict()
    sclass=data['sclass']
    if sclass not in all_class:
        return "Wrong Class"
    file = request.files['pic']

    if allow(file.filename):

        file.save(os.path.join(app.config["IMAGE_UPLOADS"],file.filename))
        
        print("Saved")
        detect = os.path.join('static','detect')
        app.config['detect_folder'] = detect
        import img_p
        b=set()
        b=img_p.img(sclass,file.filename)
        temp_list=list()
        #names=list()
        #email=list()
        #ad=list()
        for i in list(b):
            try:
                from database import all_students
                temp=all_students.get_info(i)
                temp_dict=dict()
                temp_dict['name']=temp[0]
                temp_dict['email']=temp[1]
                temp_dict['ad']=temp[2]
                temp_list.append(temp_dict)
            except:
                pass
        #for j in temp_list:
          #  names.append(j[0])
            #email.append(j[1])
            #ad.append(j[2])
        image = os.path.join(app.config['detect_folder'],file.filename)
        print(image)
        return render_template('detected.html',image =image, students=temp_list)
    else:
        return("WRONG FILE...!! IMAGES ONLY")

@app.route("/add2db",methods=["POST"])
def add2db():
    if request.method=='POST':
        data=request.form.to_dict()
        if(all_students.check(data["adno"])):
            if(all_students.add_data(data["name"],data["eid"],data["ph"],data["class"],data["adno"])):

                if not os.path.exists("train_folder/"+data["class"]):
                    os.makedirs("train_folder/"+data["class"])
                os.makedirs("train_folder/"+data["class"]+"/"+data["adno"])
                app.config["image_upload"]="train_folder/"+data["class"]+"/"+data["adno"]
                file1 = request.files['pic1']
                file2 = request.files['pic2']
                file3 = request.files['pic3']
                file4 = request.files['pic4']
                file5 = request.files['pic5']
                file6 = request.files['pic6']
                try:
                    file1.save("train_folder/"+data["class"]+"/"+data["adno"]+"/"+file1.filename)
                    file2.save("train_folder/"+data["class"]+"/"+data["adno"]+"/"+file2.filename)
                    file3.save("train_folder/"+data["class"]+"/"+data["adno"]+"/"+file3.filename)
                    file4.save("train_folder/"+data["class"]+"/"+data["adno"]+"/"+file4.filename)
                    file5.save("train_folder/"+data["class"]+"/"+data["adno"]+"/"+file5.filename)
                    file6.save("train_folder/"+data["class"]+"/"+data["adno"]+"/"+file6.filename)
                except:
                    return "IMAGE NOT UPLOADED"
                return render_template('_page.html')
            else:
                return("Check Your Connection!!")
        else:
            return("Already Registered")

@app.route("/add")
def add():
    return render_template('add2db.html')

@app.route("/dataset")
def dataset():
    return render_template('dataset.html')

@app.route("/refresh_data",methods=["POST"])
def refresh_data():
    all_class=[f.name for f in os.scandir("train_folder") if f.is_dir() ]
    if request.method=='POST':
        data=request.form.to_dict()
        sclass=request.form["class"]
        password=request.form["password"]
        if (sclass in all_class and password=="dvah"):
            import facetrain
            return facetrain.train(sclass)
    


if __name__=='__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(debug=True,port=port)

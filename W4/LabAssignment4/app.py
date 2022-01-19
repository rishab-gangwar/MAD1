from flask import Flask, render_template, request
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('Agg')
app = Flask(__name__)
# Desktop/MAD1/W4/ASSIGN


@app.route('/', methods=["POST", "GET"])
def simple():
    if request.method == "GET":
        return render_template("main.html")
    else:
        csvdata = open("data.csv", 'r')
        data = csvdata.read()
        data = data.strip()
        data = data.replace(',', "")
        data1 = data.split("\n")

        final = []
        stringheader = data1[0]  # Student id Course id Marks
        Student_id = stringheader[0:10]
        Course_id = stringheader[11:20]
        Marks = stringheader[21:]
        finalsFirstlist = []
        finalsFirst = []
        finalsFirst.append(Student_id)
        finalsFirst.append(Course_id)
        finalsFirst.append(Marks)
        finalsFirstlist.append(finalsFirst)
        for item in data1[1:]:
            # print(item)
            final.append(list(map(int, item.split())))
        final = finalsFirstlist+final
        if request.form["ID"] == "student_id":
            exactstudent = []
            total = 0
            if request.form["id_value"].isnumeric():
                for i in final:
                    if i[0] == int(request.form["id_value"]):
                        exactstudent.append(i)
                        total += i[2]
            if total != 0:
                return render_template("student.html", student_info=exactstudent, totalmarks=total)
            else:
                return render_template("error.html")

        else:
            exactcourse = []
            ploting = []
            total = 0
            maxi = -1
            if request.form["id_value"].isnumeric():
                for i in final:
                    if i[1] == int(request.form["id_value"]):
                        exactcourse.append(i)
                        total += i[2]
                        ploting.append(i[2])
                        if i[2] > maxi:
                            maxi = i[2]

            if total != 0:
                avg = total/len(exactcourse)
                ploting.sort()
                plt.hist(ploting)
                plt.xlabel('Marks')
                plt.ylabel('Frequency')
                plt.savefig('static//report.jpg')
                return render_template("course.html", max=maxi, average=avg)
            else:
                return render_template("error.html")


if __name__ == "__main__":
    app.debug = True
    app.run()

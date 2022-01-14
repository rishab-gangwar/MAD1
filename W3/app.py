ttemplate1="""<!DOCTYPE html>
<html>
<style>
table, th, td {
  border:1px solid black;
}
</style>
<body>

<h1>Students Details</h1>

<table>
  <tr>
    <th>Student id</th>
    <th>Course id</th>
    <th>Marks</th>
  </tr>
  {% for i in ans %}
  <tr>
    <td>{{i[0]}}</td>
    <td>{{i[1]}}</td>
    <td>{{i[2]}}</td>
  </tr>
  {% endfor %}
  <tr>
  <td colspan="2">Total Marks</td>
  <td>{{totmarks}}</td>
  </tr>
</table>

</body>
</html>
"""
error="""
<!DOCTYPE html>
<html>
<body>

<h1>Wrong Inputs</h1>
<p> something went wrong</p>

</body>
</html>"""
ttemplate2="""
<!DOCTYPE html>
<html>
<style>
table, th, td {
  border:1px solid black;
}
</style>
<body>

<h1>Course Details</h1>

<table>
  <tr>
    <td>Average Marks</td>
    <td>Maximum Marks</td>
  </tr>
  <tr>
    <td>{{avg}}</td>
    <td>{{high}}</td>
  </tr>
</table>
<img src="report.jpg">
</body>
</html>
 """
from jinja2 import Template
import sys
import matplotlib.pyplot as plt

def f1(arg):

  f=open('data.csv',"r")
  Master=[]
  data=f.readlines()
  for i in data:
    ni=i.strip('\n')
    nni=ni.split(', ')
    Master.append(nni)
  #print(Master[1][1])
    ans=[]
    totmarks=0
    for i in Master:
      if i[0]==arg:
        totmarks+=int(i[2])
        ans.append(i)
  #print(ans)
  if len(ans)==0:
    template=Template(error)
    output=(template.render())
    with open("output.html", "w") as fh:
      fh.write(output)
  else:
    template=Template(ttemplate1)
    output=(template.render(ans=ans,totmarks=totmarks))
    with open("output.html", "w") as fh:
      fh.write(output)

def f2(arg):
  f=open('data.csv',"r")
  Master=[]
  data=f.readlines()
  for i in data:
    ni=i.strip('\n')
    nni=ni.split(', ')
    Master.append(nni)
  #print(Master[1][1])
  totmarks=0
  markslist=[]
  maxmarks=0
  for i in Master:
    if i[1]==arg:
      totmarks+=int(i[2])
      if int(i[2])>maxmarks:
        maxmarks=int(i[2])
      markslist.append(i[2])        
  #print(ans)
  markslist.sort()
  plt.hist(markslist)
  plt.xlabel('Marks')
  plt.ylabel('Frequency')
  plt.savefig('report.jpg')
  avg=totmarks/len(markslist)
  if len(markslist)==0:
    template=Template(error)
    
    output=(template.render())
    with open("output.html", "w") as fh:
      fh.write(output)
  else:
    template=Template(ttemplate2)
    output=(template.render(avg=avg,high=maxmarks))
    with open("output.html", "w") as fh:
      fh.write(output)

if __name__=="__main__":
  if sys.argv[1]=='-s':
    f1(sys.argv[2])
  else:
    f2(sys.argv[2])
  


from flask import Flask, render_template, request
import pandas as pd
import numpy as np


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/data", methods=["GET", "POST"])
def data():
    try:
        if request.method == "POST":
            file = request.form["upload-file"]
            data = pd.read_excel(file)
            arr = np.array(data)
            N = arr[2][0]
            N = int(N[2:])
            col = []
            stu = []
            for i in range(N):
                col.append(arr[0][i])
            for i in range(N):
                stu.append(arr[1][i])
            college = []
            student = []
            # college array
            for i in range(4, 4 + N):
                tmp = []
                for j in range(0, N):
                    x = stu.index(arr[i][j + 1])
                    tmp.append(x + N)
                college.append(tmp)
            # student array
            for i in range(5 + N, 5 + (2 * N)):
                tmp = []
                for j in range(0, N):
                    x = col.index(arr[i][j + 1])
                    tmp.append(x)
                student.append(tmp)

            ans = []
            prefer = []
            for i in range(0, len(college)):
                prefer.append(college[i])
            for i in range(0, len(student)):
                prefer.append(student[i])

            def sPrefersC1OverC(prefer, s, c, c1):
                for i in range(N):
                    if prefer[s][i] == c1:
                        return True
                    if prefer[s][i] == c:
                        return False

            def stablMatch(prefer):
                sPartner = [-1 for i in range(N)]
                cFree = [False for i in range(N)]
                freeCount = N
                while freeCount > 0:
                    c = 0
                    while c < N:
                        if cFree[c] == False:
                            break
                        c += 1
                    i = 0
                    while i < N and cFree[c] == False:
                        s = prefer[c][i]
                        if sPartner[s - N] == -1:
                            sPartner[s - N] = c
                            cFree[c] = True
                            freeCount -= 1
                        else:
                            c1 = sPartner[s - N]
                            if sPrefersC1OverC(prefer, s, c, c1) == False:
                                sPartner[s - N] = c
                                cFree[c] = True
                                cFree[c1] = False
                        i += 1
                for i in range(N):
                    tmp = []
                    tmp.append(stu[((i + N) % N)])
                    tmp.append(col[sPartner[i]])
                    ans.append(tmp)

            stablMatch(prefer)

            return render_template(
                "data.html",
                arr=arr,
                N=N,
                college=college,
                student=student,
                prefer=prefer,
                ans=ans,
                stu=stu,
                col=col,
            )
    except:
        return render_template("error.html")


if __name__ == "__main__":
    app.run(debug=True)

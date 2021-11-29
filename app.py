from flask import Flask, render_template, request
import requests

app = Flask(__name__)


# helper function

def getdata():

    r = requests.get(
        'https://s3-ap-southeast-1.amazonaws.com/he-public-data/chart2986176.json')
    arr = list(r.json())

    barcharts = []
    piecharts = []
    for i in range(len(arr)):
        if arr[i]['type'] == 'Bar':
            barcharts.append(arr[i])
        else:
            piecharts.append(arr[i])

    barchartdata = {i+1: barcharts[i]['elements']
                    for i in range(len(barcharts))}
    piechartdata = {i+1: piecharts[i]['elements']
                    for i in range(len(piecharts))}

    return barchartdata, piechartdata


@app.route("/", methods=['GET', 'POST'])
def hello_world():

    displaybar = False
    displaypie = False
    showerror = False

    barchartdata, piechartdata = getdata()
    if request.method == 'POST':

        getchart = request.form.get('charts')

        if str(getchart) == 'Bar':
            displaybar = True
            return render_template('bar.html', barchartdata=barchartdata)

        elif str(getchart) == 'Pie':
            displaypie = True
            return render_template('pie.html', piechartdata=piechartdata)

        else:
            showerror = True
            return render_template('index.html', barchartdata=barchartdata, piechartdata=piechartdata)

    return render_template('index.html', barchartdata=barchartdata, piechartdata=piechartdata)


if __name__ == '__main__':
    app.run(debug=True)

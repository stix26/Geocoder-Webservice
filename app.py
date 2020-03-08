from flask import Flask, render_template, request, send_file
import pandas
from geopy.geocoders import ArcGIS
import datetime


app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    global filename
    if request.method=='POST':
        file=request.files["file"]
        try:
            df=pandas.read_csv(file)
            nom=ArcGIS()
            n=nom.geocode("")
            #df["Address"]=df["Address"]+", "+df["City"] + ", "+ df["State"]+ ", " + df["Country"]
            df["Coordinates"]=df["Address"].apply(nom.geocode)
            df["Latitude"]=df["Coordinates"].apply(lambda x: x.latitude if x != None else None)
            df["Longitude"]=df["Coordinates"].apply(lambda x: x.longitude if x != None else None)
            #df=df.drop("Coordinates", 1)
            filename=datetime.datetime.now().strftime("uploads/%Y-%m-%d-%H-%M-%S-%f"+".csv")
            df.to_csv(filename, index=None)
            return render_template("index.html", text=df.to_html(), btn="download.html")
        except:
            return render_template("index.html", text="Missing address in column of your CSV file!")

@app.route("/download")
def download():
    return send_file(filename, attachment_filename="uploadedfile.csv", as_attachment=True)


if __name__=='__main__':
    #app.debug=False
    app.debug=True
    app.run()
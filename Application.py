from flask import Flask, request, render_template
import requests


# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "YOUR CLOUD API KEY HERE"
token_response = requests.post('https://iam.eu-gb.bluemix.net/identity/token',
                               data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
print(token_response)
mltoken = token_response.json()["access_token"]
print("mltoken",mltoken)

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
# payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored, another_array_of_values_to_be_scored]}]}


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('final.html')


@app.route('/predict', methods=['POST','GET'])
def predict():
    #print('inside y_predict')
    batterypower = request.form["batterypower"]
    bluetooth = request.form["bluetooth"]
    clockspeed = request.form["clockspeed"]
    dualsim = request.form["dualsim"]
    fc = request.form["fc"]
    fourg = request.form["fourg"]
    intmemory = request.form["intmemory"]
    memdep = request.form["memdep"]
    mobilewt= request.form["mobilewt"]
    ncores = request.form["ncores"]
    primecam = request.form["primecam"]
    pxheight = request.form["pxheight"]
    pxwidth = request.form["pxwidth"]
    ram = request.form["ram"]
    sch = request.form["sch"]
    scw = request.form["scw"]
    talktime = request.form["talktime"]
    threeg = request.form["threeg"]
    touchscreen = request.form["touchscreen"]
    wifi = request.form["wifi"]

    t = [[int(batterypower), int(bluetooth), float(clockspeed), int(dualsim), int(fc), int(fourg), int(intmemory),
          int(memdep),
          int(mobilewt), int(ncores), int(primecam), int(pxheight), int(pxwidth), int(ram), int(sch), int(scw),
          int(talktime),
          int(threeg), int(touchscreen), int(wifi)]]
    print(t)
    payload_scoring = {"input_data": [
        {"field": [["batterypower", "bluetooth", "clockspeed", "dualsim", "fc", "fourg", "intmemory", "memdep",
                                                                                                      "mobilewt",
                    "ncores", "primecam", "pxheight", "pxwidth", "ram", "sch", "scw", "talktime", "threeg",
                    "touchscreen", "wifi"]], "values": t}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/aa50c3e0-54d6-4af3-921c-e5919fac9758/predictions?version=2021-04-09',
        json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    print(predictions)

    pred = predictions['predictions'][0]['values'][0][0]
    print(pred)
    if (pred == 0):
        output = "Low Range"
        return ("Low Range: 500 - 10000")
    elif (pred == 1):
        output = "Medium Range"
        return("Medium Range: 10000 - 20000")
    elif (pred == 2):
        output = "High Range "
        return("High Range: 20000 - 30000")
    else:
        output = "Very High"
        return("Very High: 30000 and above")
    return render_template('final.html', prediction_text=output)

if __name__ == '__main__':
    app.run(port=8000,debug=True)

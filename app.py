from flask import Flask, render_template, request, jsonify
from model import transform_and_predict
import pandas as pd
import datetime as dt

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/predict/', methods=['POST']) 
def test_predict():
    # receive data from form
    input_data = request.form
    floor_area = input_data.get('floor-area', type=float)
    lease_year = input_data.get('lease-commencement-date', type=int)
    lat, long = input_data.get('lat', type=float), input_data.get('long', type=float)
    flat_type = input_data.get('flat-type', type=int)
    flat_model = input_data.get('flat-model', type=int)
    town = input_data.get('town', type=int)
    date = input_data.get('date', type=str)

    # preprocess
    lease_commencement_date = 1950 + lease_year
    sell_date = dt.datetime.strptime(date, '%Y-%m-%d')
    months_since_2012 = (sell_date.year - 2012) * 12 + sell_date.month
    age_years = sell_date.year - lease_commencement_date

    # construct input
    df_input = pd.DataFrame({
        'floor_area_sqm': [floor_area],
        'lease_commencement_date': [lease_commencement_date],
        'lat': [lat], 'long': [long],
        'flat_type_rank': [flat_type],
        'flat_model_rank': [flat_model],
        'town_rank': [town],
        'months_since_2012': [months_since_2012],
        'age_years': [age_years]
    })

    # input validation
    if df_input.isnull().values.any():
        cols = df_input.isnull().any()[lambda x: x]
        data = {'prediction': f'Error: the values in the fields: {cols.index.values} are invalid.'}
        data = jsonify(data)
        return data

    # get prediction
    try:
        pred = transform_and_predict(df_input)
        if not 0 < pred < 10_000_000:
            raise RuntimeError('The model produced a unreasonable output, possibly due to extreme '
                               'input values. Try using more sensible inputs. '
                               f'Returned value: ${pred:,.2f}')
    except Exception as e:
        data = {'prediction': f'Error: something went wrong during calculation: {e}.'}
        data = jsonify(data)
        return data

    # format and return
    data = {'prediction': f'${pred:,.2f}'} 
    data = jsonify(data) 
    return data 


if __name__ == '__main__':
    app.run(port=1313)  # the google maps api key requires this port, cba changing it
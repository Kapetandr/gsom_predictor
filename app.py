from flask import Flask, request
import numpy
import joblib

RF_MODEL_PATH = 'ml_models/random_forest_model.pkl'
CB_MODEL_PATH = 'ml_models/catboost_model.pkl'

SCALER_X_PATH = 'ml_models/scaler_x.pkl'

SCALER_Y_PATH = 'ml_models/scaler_y.pkl'

app = Flask(__name__)

@app.route('/predict_price', methods=['GET'])
def predict():
    args = request.args
    model = args.get('model', default=-1, type=int)
    open_plan = args.get('open_plan', default = -1, type = int)
    rooms = args.get('rooms', default = -1, type = int)
    area = args.get('area', default = -1, type = float)
    kitchen_area = args.get('kitchen_area', default = -1, type = float)
    living_area = args.get('living_area', default = -1, type = float)


    if model == 1:

        # response = 'open_plan:{}, rooms:{}, area:{}, renovation:{}'.format(open_plan, rooms, area, renovation)
        model = joblib.load(RF_MODEL_PATH)
        sc_x = joblib.load(SCALER_X_PATH)
        sc_y = joblib.load(SCALER_Y_PATH)

        x = numpy.array([open_plan, rooms, area, kitchen_area, living_area]).reshape(1,-1)
        x = sc_x.transform(x)
        result = model.predict(x)
        result = sc_y.inverse_transform(result.reshape(1, -1))

        return str(result[0][0])

    if model == 2:

        # response = 'floor:{}, open_plan:{}, rooms:{}, area:{}.format(floor, open_plan, rooms, area, renovation)

        model = joblib.load(CB_MODEL_PATH)
        sc_x = joblib.load(SCALER_X_PATH)
        sc_y = joblib.load(SCALER_Y_PATH)

        x = numpy.array([open_plan, rooms, area, kitchen_area, living_area]).reshape(1, -1)
        x = sc_x.transform(x)
        result = model.predict(x)
        result = sc_y.inverse_transform(result.reshape(1, -1))

        return str(result[0][0])

    else:
        return "not a valid model"


if __name__ == '__main__':
    app.run(debug=True, port=5444, host='0.0.0.0')
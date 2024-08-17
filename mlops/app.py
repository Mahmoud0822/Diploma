import numpy as np
from flask import Flask,render_template,request
import pickle
model = pickle.load(open(r'C:\Users\mahmo\Downloads\mlops\Model.pkl','rb'))
type_of_meal =  pickle.load(open(r'C:\Users\mahmo\Downloads\mlops\t_l.pkl','rb'))
room_type = pickle.load(open(r'C:\Users\mahmo\Downloads\mlops\R_L.pkl','rb'))
Market_segment = pickle.load(open(r'C:\Users\mahmo\Downloads\mlops\M_S.pkl','rb'))
book_status = pickle.load(open(r'C:\Users\mahmo\Downloads\mlops\b_s.pkl','rb'))


app = Flask(__name__)
@app.route('/')
def home():
    return render_template('page.html')


columns = ['no_of_adults','no_of_children','no_of_weekend_nights','no_of_week_nights','type_of_meal_plan','required_car_parking_space','room_type_reserved','lead_time','arrival_year','arrival_month','arrival_date','market_segment_type','repeated_guest','no_of_previous_cancellations','no_of_previous_bookings_not_canceled','avg_price_per_room','no_of_special_requests']

cat_columns = ['type_of_meal_plan','room_type_reserved','market_segment_type']


@app.route('/pred',methods=['POST'])
def predict():
    features = []
    for column in columns:
        value = request.form.get(column)
        if column == 'type_of_meal_plan':
            value = type_of_meal.transform([value])
        elif column == 'room_type_reserved':
            value = room_type.transform([value])
        elif column == 'market_segment_type':
            value = Market_segment.transform([value])
        features.append(float(value))
    features = np.array(features)
    features = features.reshape(1,17)
    pred = model.predict(features)
    pred = book_status.inverse_transform(pred)
    return render_template('result.html',pred=pred)    

if __name__ == '__main__':
    app.run()
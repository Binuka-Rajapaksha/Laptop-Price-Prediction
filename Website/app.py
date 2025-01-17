from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

def predict(list):
    filename = 'model/predictor.pickle'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    predicted_value = model.predict([list])

    return predicted_value


@app.route('/', methods=['POST', 'GET'])
def index():
    predicted_price = 0
    if request.method == 'POST':
        ram = request.form['ram']
        weight = request.form['weight']
        company = request.form['company']
        typename = request.form['typename']
        opsys = request.form['opsys']
        cpu = request.form['cpuname']
        gpu = request.form['gpuname']
        touchscreen = request.form.getlist('touchscreen')
        ips = request.form.getlist('ips')


        feature_list = []
        feature_list.append(int(ram))
        feature_list.append(float(weight))
        feature_list.append(len(touchscreen))
        feature_list.append(len(ips))

        company_list = ['acer', 'apple', 'asus', 'dell', 'hp', 'lenovo', 'msi', 'other', 'toshiba']
        typename_list = ['2in1convertible', 'gaming', 'netbook', 'notebook', 'ultrabook', 'workstation']
        opsys_list = ['linux', 'mac', 'other', 'windows']
        cpu_list = ['amd', 'intelcorei3', 'intelcorei5', 'intelcorei7', 'other']
        gpu_list = ['amd', 'intel', 'nvidia']

        def traverse(item_list, value):
            for item in item_list:
                if item == value:
                    feature_list.append(1)
                else:
                    feature_list.append(0)

        
        traverse(company_list, company)
        traverse(typename_list, typename)
        traverse(opsys_list, opsys)
        traverse(cpu_list ,cpu)
        traverse(gpu_list, gpu)

        predicted_price = predict(feature_list)

        predicted_price = predicted_price*300
        predicted_price = np.round(predicted_price[0])

        print(predicted_price)

    return render_template('index.html', pred_value = predicted_price)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify
from Functions import *
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
contentlab = ContentLab()

variables = {}

@app.route('/what_to_accomplish', methods=['POST'])
def api_what_to_accomplish():
    data = request.get_json()
    user_question = data.get('user_question')  # Assuming the JSON contains 'user_question' field
    variables['user_question']= user_question
    if user_question:
        output = contentlab.what_to_accomplish(user_question)
        # x = output.split("{")[1].split("}")[0]
        output = output.replace("python","").replace("json","").replace("'''","")
        print(output)
        out_res = json.loads(output)
        out_res["prompt"]=user_question
        return jsonify(out_res)
    else:
        return jsonify({'error': 'Invalid data provided'}), 400

@app.route('/options_in_funnel_focus', methods=['POST'])
def api_options_in_funnel_focus():
    data = request.get_json()
    funnel = data.get('funnel')
    user_question = variables["user_question"]
    print("variablesss---------",variables,user_question)
    variables["funnel_focus"] = funnel
    if funnel:
        output = contentlab.options_in_funnel_focus(funnel)
        # x=output.split("{")[1].split("}")[0]
        output = str(output.replace("python", "").replace("json", "").replace('\n', ''))
        if output[0] != "{":
            output = output[3:-3]
        print(output)
        out_res = json.loads(output)
        return jsonify(out_res)
    else:
        return jsonify({'error': 'Invalid data provided'}), 400

@app.route('/generate_KPI', methods=['POST'])
def api_generate_KPI():
    data = request.get_json()
    option = data.get('option')
    funnel = variables["funnel_focus"]
    user_question = variables["user_question"]
    if option:
        output = contentlab.generate_KPI(funnel, option, user_question)
        # x = output.split("{")[1].split("}")[0]
        output = output.replace("python", "").replace("json", "").replace("\n", "")
        if output[0] != "{":
            output = output[3:-3]
        print(output)
        out_res = json.loads(output)
        return jsonify(out_res)
    else:
        return jsonify({'error': 'Invalid data provided'}), 400


@app.route('/generate_activity_theme', methods=['POST'])
def api_generate_activity_theme():
    data = request.get_json()
    KPI = data.get('kpi')
    variables["kpi"] = KPI
    values = data.get('values')
    variables["kpi_vals"] = values
    # company = data.get('paypal')  # hardcode company='paypal'
    if KPI and values:
        output = contentlab.generate_activity_theme(KPI,values,"paypal")
        # x = output.split("{")[1].split("}")[0]
        output = output.replace("python", "").replace("json", "").replace("\n", "")
        if output[0] != "{":
            output = output[3:-3]
        print(output)
        out_res = json.loads(output)
        return jsonify(out_res)
    else:
        return jsonify({'error': 'Invalid data provided'}), 400
@app.route('/prescrt_analy_recommendations', methods=['POST'])
def api_prescrt_analy_recommendations():
    data = request.get_json()

    activity_theme = data.get('activity_theme')
    KPI = variables["kpi"]
    values = variables["kpi_vals"]
    if activity_theme:
        output = contentlab.priscript_analy_recommendations(KPI,values,activity_theme)
        # x = output.split("{")[1].split("}")[0]
        output = output.replace("python", "").replace("json", "").replace("\n", "")
        if output[0] != "{":
            output = output[3:-3]
        print(output)
        out_res = json.loads(output)
        return jsonify(out_res)
    else:
        return jsonify({'error': 'Invalid data provided'}), 400

@app.route('/idea_detail_view', methods=['POST'])
def api_idea_detail_view():
    data = request.get_json()
    user_feedback = data.get('user_feedback')
    ai_recom = data.get("ai_recommendation")

    if user_feedback and ai_recom:
        output = contentlab.idea_detail_view(user_feedback, ai_recom)
        # x = output.split("{")[1].split("}")[0]
        output = output.replace("python", "").replace("json", "").replace("\n", "")
        if output[0] != "{":
            output = output[3:-3]
        print(output)
        out_res = json.loads(output)
        return jsonify(out_res)
    else:
        return jsonify({'error': 'Invalid data provided'}), 400


if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, render_template, request
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/chart/sankey", methods=['GET'])  # post not working
def sankey():
    if request.method == 'GET':
        from_ = request.args.getlist('from')
        to = request.args.getlist('to')
        values = request.args.getlist('values')
        if len(from_) == 1:
            from_ = from_[0].split(',')
        if len(to) == 1:
            to = to[0].split(',')
        if len(values) == 1:
            values = values[0].split(',')
        values = [float(v) for v in values]
        data = [[f, t, v] for f, t, v in zip(from_, to, values)]
        label = request.args.get('label')
        return render_template('google_sankey.html', label=label, data=data)
    # if request.method == 'POST':
    #     form_data = request.form
    #     label = form_data.get('label')
    #     data = form_data.get('data_json')
    #     return render_template('google_sankey.html', label=label, data=data)


@app.route("/chart/zoom_sunburst", methods=['GET'])  # post not working
def zoom_sunburst():
    if request.method == 'GET':
        sequences = request.args.getlist('sequences')
        values = request.args.getlist('values')
        add_end = request.args.get('add_end', '')
        root_name = request.args.get('root_name', '')
        return render_template(
            'zoom_sunburst.html',
            sequences=sequences, values=values, add_end=add_end, root_name=root_name)


@app.route("/chart/sunburst", methods=['GET'])  # post not working
def sunburst():
    if request.method == 'GET':
        sequences = request.args.getlist('sequences')
        values = request.args.getlist('values')
        add_end = request.args.get('add_end', '')
        root_name = request.args.get('root_name', '')
        return render_template(
            'sunburst.html',
            sequences=sequences, values=values, add_end=add_end, root_name=root_name)


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request
from pokemon_typing_tools import *
app = Flask(__name__)

@app.route("/")
def welcome():
    return '''<p>Welcome to my collection of api tools :)</p>
    try <a href="/get_gen_type_chart">this</a>'''

@app.route('/print_arg/<arf>', methods=['GET'])
def do_arg_stuff(arf):
    return f"<p>{arf}</p>"

@app.route('/get_gen_type_chart', methods=['GET'])
def get_gen_type_chart_api():
    gen = request.args.get('gen')
    if not gen:
        form_text = '''
        <form action="/get_gen_type_chart">
            <label for="title">Generation Number</label>
            <br>
            <input type="text" name="gen"
                placeholder="Generation Number"
                value=""></input>
            <br>
            <button type="submit">Submit</button>
        </form>
        '''
        return form_text

    try:
        int(gen)
    except:
        return 'gave non num'

    if not get_gen_name_from_num(int(gen)):
        return 'gen not released'

    chart_no_titles = get_gen_type_chart(int(gen))
    chart = [[' '] + TYPE_LIST[:len(chart_no_titles)]]
    for i, record in enumerate(chart_no_titles):
        chart.append([TYPE_LIST[i]] + record)
    print_chart = ''.join(['<tr>' + ''.join(['<th>' + str(x) + '</th>' for x in chart[i]]) + '</tr>' for i in range(len(chart))])
    style_string = 'th {border-style: inset;}'
    return f"<style>{style_string}</style><table>{print_chart}</table>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
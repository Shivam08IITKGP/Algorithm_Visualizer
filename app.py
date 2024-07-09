from flask import Flask, render_template, request
import os
import subprocess
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/gifs'


@app.route('/')
def index():
    distances = {}
    traversal_order = []
    sorted_array = []
    mst = []
    level_order = []
    matches = []
    z_array = []
    prefix_array = []
    result_matrix = []
    bridges = []
    ap = []
    max_value = []
    suffix_array=[]
    test_case_type = ""
    array=[]
    s = ""
    algorithm = ""
    return render_template('index.html', algorithm=algorithm, filename=None, distances=distances,
                           traversal_order=traversal_order, sorted_array=sorted_array, mst=mst,
                           level_order=level_order, matches=matches, z_array=z_array, prefix_array=prefix_array, ap=ap,
                           result_matrix=result_matrix, bridges=bridges, max_value=max_value, s=s,suffix_array=suffix_array,test_case_type=test_case_type,array=array,
                           inf=float('inf'))


@app.route('/run', methods=['POST'])
def run():
    algorithm = request.form.get('algorithm')
    custom_input = request.form.get('custom_input')
    test_case_type = request.form.get('test_case')
    print(custom_input)
    print(algorithm)
    print(test_case_type)
    output_file = os.path.join(app.config['UPLOAD_FOLDER'], 'output.gif')
    cmd = ['python3', 'main.py', algorithm, test_case_type, custom_input, output_file]

    result = subprocess.run(cmd, capture_output=True, text=True)

    print("STDOUT:", result.stdout)
    # print("STDERR:", result.stderr)
    result_file = 'result.json'
    if os.path.exists(result_file):
        with open(result_file, 'r') as json_file:
            try:
                result_data = json.load(json_file)
            except json.JSONDecodeError:
                print(f"Error: Could not decode JSON from {result_file}")
                result_data = {}

        distances = result_data.get('distances', {})
        traversal_order = result_data.get('traversal_order', [])
        sorted_array = result_data.get('sorted_array', [])
        mst = result_data.get('mst', [])
        level_order = result_data.get('level_order', [])
        matches = result_data.get('matches', [])
        z_array = result_data.get('z_array', [])
        prefix_array = result_data.get('positions', [])
        result_matrix = result_data.get('result_matrix', [])
        bridges = result_data.get('bridges', [])
        ap = result_data.get('ap', [])
        max_value = result_data.get('max_value', [])
        algorithm = result_data.get('algorithm', "")
        s = result_data.get('string', "")
        suffix_array = result_data.get('suffix_array', [])
        array = result_data.get('array', [])
        
        print("Result data loaded from file")
        print("Distances:", distances)
        print("Traversal order:", traversal_order)
        print("Sorted array:", sorted_array)
        print("MST:", mst)
        print("Level order:", level_order)
        print("Matches:", matches)
        print("Z Array:", z_array)
        print("Result Matrix:", result_matrix)
        print("Bridges:", bridges)
        print("Articulation Points: ", ap)
        print("Max Value: ", max_value)
        print("Prefix Array: ", prefix_array)
        print("Algorithm: ", algorithm)
        print("String: ", s)
        print("Suffix Array: ", suffix_array)
        print("Test Case: ", test_case_type)
        print("Array: ", array)

    else:
        distances = {}
        traversal_order = []
        sorted_array = []
        mst = []
        level_order = []
        matches = []
        z_array = []
        result_matrix = []
        bridges = []
        ap = []
        max_value = []
        prefix_array = []
        array = []
        algorithm = ""
        s = ""

    inf = float('inf')
    return render_template('index.html', filename='gifs/output.gif', algorithm=algorithm, 
                           distances=distances, s=s,
                           traversal_order=traversal_order, sorted_array=sorted_array, mst=mst,
                           level_order=level_order, matches=matches,
                           z_array=z_array, result_matrix=result_matrix, prefix_array=prefix_array,suffix_array=suffix_array,
                           max_value=max_value, bridges=bridges, ap=ap, test_case_type=test_case_type, array = array, inf=inf)


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

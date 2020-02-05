# CS 329 Elements of Web Programming
#
# assignment 1
#
# Jeffrey E. Cordes
#
# jec4443

from flask import Flask
from flask import request   # To access query parameters
import requests
import xml.etree.ElementTree as ET

# our instantiated flask application
app = Flask(__name__)

@app.route("/")
def handler_method():
    # retrieve data from the online page containing the XML data
    pools_data = 'https://raw.githubusercontent.com/devdattakulkarni/elements-of-web-programming/' \
                 'master/data/austin-pool-timings.xml'

    # convert XML to a string
    pools_data_to_str = requests.get(pools_data).text

    # parse the XML string
    root = ET.fromstring(pools_data_to_str)

    # retrieve searched parameters
    searched_parameters = {}
    numOfParameters = 0

    weekend = request.args.get('weekend')
    if weekend is not None:
        numOfParameters += 1
        searched_parameters['weekend'] = weekend

    pool_type = request.args.get('pool_type')
    if pool_type is not None:
        numOfParameters += 1
        searched_parameters['pool_type'] = pool_type

    weekday_closure = request.args.get('weekday_closure')
    if weekday_closure is not None:
        numOfParameters += 1
        searched_parameters['weekday_closure'] = weekday_closure

    # filter pools based on requested parameters
    filtered_pools = []

    # print(root, root[0], root[0][1], root[0][1].tag, root[0][1].text)
    # print(len(root), len(root[0]), len(root[0][1]), len(root[0][1].tag), len(root[0][1].text))

    for i in range(len(root)):
        matching_parameters = 0
        for j in root[i]:
            if j.tag in searched_parameters and searched_parameters[j.tag] == j.text:
                matching_parameters += 1
                if matching_parameters >= numOfParameters:
                    filtered_pools.append(root[i][0].text)
                    break
                    
    result_pool_names = ""

    header_num = 1
    for i in filtered_pools:
        result_pool_names += '<h' + str(header_num) + '>' + i + '</h' + str(header_num) + '>'

    # for p in filtered_pools:
    #     print(p)

    # print the names of those pools to the web page
    return result_pool_names


# TODO ask about this if __name__ block
if __name__ == '__main__':
    app.run(debug=True)

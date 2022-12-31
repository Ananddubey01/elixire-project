from flask import Flask, request, jsonify
from flask import send_from_directory, abort
from flask_cors import CORS


from utils import getSingleProductDetailFromAmazon, getSearchQueryResult, getSearchQueryResultFrom1Mg, getSingleResultFrom1Mg
app = Flask(__name__)
CORS(app)

path = "./cities.csv"
app.config["CLIENT_FILES"] = "./tempCSVFiles"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding": "utf-8,gzip, deflate",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}


@app.route("/", methods=['GET'])
def server_info():
    return {"END Points": {
        "/amazonsingle": "GET",
        "/amazonquery": "GET",
        "/tata1mgquery": "GET"
    }}


@app.route("/amazonsingle", methods=['POST'])
def get_single_amazon():
    try:
    
        req = request.json
        fileId = getSingleProductDetailFromAmazon(req['url'], headers)
        return {"data": fileId}
    except FileNotFoundError:
        abort(404)


@app.route("/amazonsingle/<id>")
def download_CSV_single_amazon(id):
    try:
        return send_from_directory(app.config['CLIENT_FILES'], path=id, as_attachment=False)
    except FileNotFoundError:
        abort(404)


@app.route("/amazonquery", methods=["POST"])
def get_amazonquery():
    try:
        req = request.json
        fileId = getSearchQueryResult(req['url'], headers, 10)
        return {"data": fileId}
    except FileNotFoundError:
        abort(404)


@app.route("/amazonquery/<id>", methods=["GET"])
def download_CSV_query_amazon(id):
    try:
        return send_from_directory(app.config['CLIENT_FILES'], path=id, as_attachment=False)
    except FileNotFoundError:
        abort(404)


@app.route("/tata1mgquery", methods=["POST"])
def get_tata1mg_query():
    print("hi")
    try:
        req = request.json
        fileId = getSearchQueryResultFrom1Mg(req['url'], headers)
        return {"data": fileId}
    except FileNotFoundError:
        abort(404)


@app.route("/tata1mgquery/<id>", methods=["GET"])
def download_CSV_query_tata1Mg(id):
    try:
        return send_from_directory(app.config['CLIENT_FILES'], path=id, as_attachment=False)
    except FileNotFoundError:
        abort(404)

@app.route("/tata1mgsingle", methods=['POST'])
def get_single_tata1Mg():
    try:
        req = request.json
        fileId = getSingleResultFrom1Mg(req['url'], headers)
        return {"data": fileId}
    except FileNotFoundError:
        abort(404)


@app.route("/tata1mgsingle/<id>")
def download_CSV_single_tata1Mg(id):
    try:
        return send_from_directory(app.config['CLIENT_FILES'], path=id, as_attachment=False)
    except FileNotFoundError:
        abort(404)


if __name__ == "__main__":
    app.run(debug=True)

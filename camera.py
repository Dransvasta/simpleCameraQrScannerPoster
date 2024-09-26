from flask import Flask,render_template,request,jsonify,redirect

app = Flask(__name__)
g_list = dict()
@app.route('/camera',methods=["GET","POST"])
def camera():
    if request.method == "POST":
        # Redirect should be returned
        # Note: You likely don't want to redirect on a POST request immediately, so I removed it
        global g_list
        
        # Check if the request is JSON or form data
        if request.is_json:
            data = request.json
            post_id = data.get('post_id')
            qrdata = data.get('qr_code')
        else:
            post_id = request.form.get('post_id')

        # Ensure post_id exists
        if not post_id:
            return jsonify({"error": "post_id is required"}), 400
        
        g_list[post_id]=qrdata
        print(g_list)  # For debugging, outputs the list of post_ids
        
        return jsonify({"message": "Data received", "post_id": post_id}), 200
    else:
        post_id = request.args.get("post_id")
        return render_template("camera.html", post_id=post_id)
@app.route("/g_list/<int:id>",methods=["GET"])
def get(id):
    result_dict=dict()
    if id in g_list:
        result_dict['status']=1
        result_dict['result']="data with given id is found"
    else:
        result_dict['status']=0
        result_dict['result']="no data found with the given id"
    return jsonify(result_dict)
if __name__=="__main__":
    app.run(debug=True)
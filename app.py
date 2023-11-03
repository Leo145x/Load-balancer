from flask import *
import boto3
from App.AWS import Aws
from App.mysqlPool import Mysql
import uuid

app = Flask(__name__, static_folder="static", static_url_path="/",template_folder="templates")

aws = Aws()

session = boto3.Session(
    aws_access_key_id=aws.get_access_key(),
    aws_secret_access_key=aws.get_secret_key(),
    region_name=aws.get_bucket_region()
)
s3 = session.client("s3")
mysql_pool = Mysql()
connection_pool = mysql_pool.create_connect_pool()

@app.route("/")
def index():
    try:
        con = connection_pool.get_connection()
        cursor = con.cursor()
        cursor.execute(
            """
                SELECT
                    message,uuid
                FROM
                    message
            """
        )
        message_db = cursor.fetchall()
        # message = [i[0] for i in message_db]
        origin_url = aws.get_origin_url()
        # img_urls = [origin_url + i[1] for i in message_db]
        data = []
        for i in message_db:
            dic = {
                "message":i[0],
                "url":origin_url + i[1]
            }
            data.append(dic)

    except Exception as e:
        return make_response(f'Error: {str(e)}', 400)
    
    finally:
        con.close()
        
    return make_response(render_template("index.html",data=data))


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    message = request.form["message"]
    uni_id = str(uuid.uuid4())
    uni_id = uni_id + ".jpg"
    try:
        con = connection_pool.get_connection()
        cursor = con.cursor()
        cursor.execute(
            """
                INSERT INTO
                    message(message, uuid)
                VALUES(%s, %s)
            """,(message,uni_id,)
        )
        con.commit()
    except Exception as e:
        return make_response(f'Error: {str(e)}', 400)

    finally:
        con.close()

    try:
        s3.upload_fileobj(file, aws.get_bucket_name(), f"{uni_id}")
    except Exception as e:
        return make_response(f'Error: {str(e)}')
    
    return redirect("/")
    
@app.route("/delete", methods=["POST"])
def delete():
    url = request.form.get("url")
    url = url.split("/")[-1]
    try:
        con = connection_pool.get_connection()
        cursor = con.cursor()
        cursor.execute(
            """
                DELETE FROM
                    message
                WHERE
                    uuid=%s
            """,(url,)
        )
        con.commit()
        # s3.delete_object(Bucket=aws.get_bucket_name(), Key=f"{url}")

    except Exception as e:
        return make_response(f'Error: {str(e)}')
    
    finally:
        con.close()
    try:
        s3.delete_object(Bucket=aws.get_bucket_name(), Key=url)
    except Exception as e:
        return make_response(f'Error: {str(e)}')
    
    return redirect("/")

@app.route("/loaderio-06991c412126391d7737a8f597bcefd5/")
def verify():
    data = "loaderio-06991c412126391d7737a8f597bcefd5"
    return jsonify(data)

if __name__ == "__main__":
    app.json.ensure_ascii = False
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["JSON_SORT_KEYS"] = False
    app.run(host="0.0.0.0", port=3000)
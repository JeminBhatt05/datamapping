from flask import Flask, render_template, request
import pandas as pd
import mysql.connector
import os

app = Flask(__name__)

# MySQL Connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'port': 3306,
    'password': 'Riddhi@123',
    'database': 'Jemin'
}
path="jemin_test1.xlsx"
fd=pd.read_excel(path)
items=fd.columns.to_list()
# items = ['', 'id', 'name', 'mn', 'language', 'gender']
uploaded_data = pd.DataFrame()


def get_db_connection():
    return mysql.connector.connect(**db_config)


@app.route('/')
def upload():
    return render_template('select1.html', items=items)

@app.route('/view', methods=['POST','GET'])
# @app.post('/view')
def view():
    global uploaded_data

    file = request.files['file']
    if file.filename == '':
        return "No file selected."

    filepath = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(filepath)

    try:
        uploaded_data = pd.read_excel(filepath)
        uploaded_data.columns = uploaded_data.columns.str.strip()
    except Exception as e:
        return f"Error reading Excel file: {e}"
    finally:
        os.remove(filepath)

    return render_template('select2.html', items=items, success="File uploaded. Now select column mappings.")


@app.route('/submit_selection', methods=['POST'])
def submit_selection():
    global uploaded_data

    if uploaded_data.empty:
        return render_template('select2.html', items=items, error="No data found. Upload an Excel file first.")

    selections = [
        request.form.get('selected_item'),
        request.form.get('selected_item1'),
        request.form.get('selected_item2'),
        request.form.get('selected_item3'),
        request.form.get('selected_item4'),
    ]
    connection = get_db_connection()
    cursor = connection.cursor()
    if 'item1' in request.form:
        sql="ALTER TABLE employe ADD UNIQUE (id);"
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
    elif 'item2' in request.form:
        sql="ALTER TABLE employe ADD UNIQUE (name);"
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
    elif 'item3' in request.form:
        sql="ALTER TABLE employe ADD UNIQUE (mn);"
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
    elif 'item4' in request.form:
        sql="ALTER TABLE employe ADD UNIQUE (language);"
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
    elif 'item5' in request.form:
        sql="ALTER TABLE employe ADD UNIQUE (gender);"
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
    #No Mapping code        
    # if '' in selections or len(selections) != len(set(selections)):
    #     return render_template('select1.html', items=items, error="Please select different columns for each field.")

    # try:
    #     deleted_ids = sync_data(*selections)
    #     message = "Data synchronized successfully."
    #     if deleted_ids:
    #         message += f" Deleted IDs: {', '.join(deleted_ids)}"
    #     return render_template('select1.html', items=items, success=message)
    # except Exception as e:
    #     return render_template('select1.html', items=items, error=f"Error syncing data: {e}")
    if len(selections) != len(set(selections)):
        return render_template('select2.html', items=items, error="Please select different columns for each field.")

    try:
        sync_data(*selections)
        return render_template('select2.html', items=items, success="Data inserted successfully.")
    except Exception as e:
        return render_template('select2.html', items=items, error=f"Error inserting data: {e}")


def sync_data(s, s1, s2, s3, s4):
    global uploaded_data

    mapping = {'id': s, 'name': s1, 'mn': s2, 'language': s3, 'gender': s4}
    df = uploaded_data[[v for v in mapping.values()]].copy()
    df.columns = list(mapping.keys())

    df['id'] = df['id'].astype(str).str.strip()
    df = df.dropna(subset=['id'])
    df.set_index('id', inplace=True)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM employe")
    db_data = pd.DataFrame(cursor.fetchall())

    if not db_data.empty:
        db_data['id'] = db_data['id'].astype(str).str.strip()
        db_data.set_index('id', inplace=True)

    deleted_ids = []

    # Insert 
    new_ids = df.index.difference(db_data.index if not db_data.empty else [])
    if not new_ids.empty:
        insert_data(df.loc[new_ids].reset_index().to_dict(orient='records'), cursor)

    # Update 
    if not db_data.empty:
        common_ids = df.index.intersection(db_data.index)
        for idx in common_ids:
            excel_row = df.loc[idx].fillna("").astype(str)
            db_row = db_data.loc[idx].fillna("").astype(str)
            if not excel_row.equals(db_row):
                update_data(idx, excel_row.to_dict(), cursor)

        # Delete 
        delete_ids = db_data.index.difference(df.index)
        if not delete_ids.empty:
            deleted_ids = delete_ids.tolist()
            delete_data(deleted_ids, cursor)

    conn.commit()
    cursor.close()
    conn.close()

    return deleted_ids


def insert_data(records, cursor):
    sql = "INSERT INTO employe (id, name, mn, language, gender) VALUES (%s, %s, %s, %s, %s)"
    values = [(r['id'], r['name'], r['mn'], r['language'], r['gender']) for r in records]
    cursor.executemany(sql, values)


def update_data(id_val, row_dict, cursor):
    sql = "UPDATE employe SET name=%s, mn=%s, language=%s, gender=%s WHERE id=%s"
    cursor.execute(sql, (row_dict['name'], row_dict['mn'], row_dict['language'], row_dict['gender'], id_val))


def delete_data(id_list, cursor):
    if not id_list:
        return
    format_strings = ','.join(['%s'] * len(id_list))
    sql = f"DELETE FROM employe WHERE id IN ({format_strings})"
    cursor.execute(sql, id_list)


if __name__ == '__main__':
    app.run(debug=True)


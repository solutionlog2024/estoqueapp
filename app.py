from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='solution_bi.mysql.dbaas.com.br',
            database='solution_bi',
            user='solution_bi',
            password='J3aQqCZ5j32Eq@'
        )
        return conn
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None
    
@app.route("/",methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nome = request.form.get("nome")
        senha = request.form.get("senha")
        if nome == "admin" and senha == "123":
            session['usuario'] = nome
            return redirect(url_for('ocorrencia'))
        else:
            return render_template("login.html", erro="Usuário ou senha inválidos")
    return render_template("login.html")

 
@app.route("/ocorrencia", methods=["GET", "POST"])
def ocorrencia():
    if request.method == "POST":
        ocorrencia = request.form.get("ocorrencia")
        data_hora = request.form.get("data-hora")
        posicao = request.form.get("barcode")
        usuario = request.form.get("usuario")
        foto_file = request.files.get("foto_ocorrencia")
        foto_ocorrencia = None

        # Salva a foto em uma pasta local e armazena o caminho no banco
        if foto_file and foto_file.filename != '':
            foto_path = os.path.join("static", "uploads", foto_file.filename)
            os.makedirs(os.path.dirname(foto_path), exist_ok=True)
            foto_file.save(foto_path)
            foto_ocorrencia = foto_path
        else:
            foto_ocorrencia = ""

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            sql = """
                INSERT INTO tbl_ocorrencias_diaria_estoque
                (ocorrencia, data_hora, posicao, foto_ocorrencia, usuario)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (ocorrencia, data_hora, posicao, foto_ocorrencia, usuario))
            conn.commit()
            cursor.close()
            conn.close()
        return redirect(url_for('ocorrencia'))

    # GET: mostra as ocorrências já registradas
    conn = get_db_connection()
    ocorrencias = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tbl_ocorrencias_diaria_estoque")
        ocorrencias = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template("ocorrencia.html", ocorrencias=ocorrencias)


@app.route("/main")
def main():
    return render_template("main.html")


@app.route("/expedicao")
def expedicao():
    return render_template("expedicao.html")

@app.route("/ocorrencia")
def ocorrencia_redirect():
    if 'usuario' in session:
        return redirect(url_for('ocorrencia'))
    else:
        return redirect(url_for('login'))
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
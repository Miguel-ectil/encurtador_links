from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash 
from app.database import get_db_connection
from flask_cors import cross_origin

bp = Blueprint("routes", __name__)

@bp.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "Campos obrigatórios!"}), 400
    
    password_hash = generate_password_hash(password)

    # Criação do usuário no banco
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (name, email, password_hash) 
        VALUES (%s, %s, %s) RETURNING id, name, email;
    """, (name, email, password_hash))
    user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": user[0], "name": user[1], "email": user[2]}), 201


# Criar um link encurtado
@bp.route("/api/links/register", methods=["POST"])
def create_link():
    data = request.get_json()
    original_url = data.get("original_url")
    short_url = data.get("short_url")
    user_id = data.get("user_id")  

    if not original_url or not short_url or not user_id:
        return jsonify({"error": "Campos obrigatórios!"}), 400

    # Criação do link associado ao usuário
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO links (original_url, short_url, user_id) 
        VALUES (%s, %s, %s) RETURNING id;
    """, (original_url, short_url, user_id))
    link_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": link_id, "original_url": original_url, "short_url": short_url, "user_id": user_id}), 201


# Listar links criados
@bp.route("/api/links", methods=["GET"])
@cross_origin(origins="http://localhost:3000")  # Permite requisições apenas do localhost:3000
def get_links():
    user_id = request.args.get('id')
    
    if not user_id:
        return jsonify({"error": "Usuário não informado"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    
    print(f"Buscando links para user_id: {user_id}")  # <-- Depuração

    cur.execute("SELECT id, original_url, short_url, clicks FROM links WHERE user_id = %s;", (user_id,))
    links = cur.fetchall()
    
    print(f"Links encontrados: {links}")  # <-- Verifique se está vindo algum dado

    cur.close()
    conn.close()

    if not links:
        return jsonify({"message": "Nenhum link encontrado"}), 404

    return jsonify([{"id": link[0], "original_url": link[1], "short_url": link[2], "clicks": link[3]} for link in links])

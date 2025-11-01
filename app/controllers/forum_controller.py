from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.post import Post

forum_bp = Blueprint("forum", __name__, url_prefix="/api")

# ---- READ: listar posts (más recientes primero)
@forum_bp.get("/posts")
@login_required
def list_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    out = []
    for p in posts:
        out.append({
            "id": p.id,
            "user_id": p.user_id,
            "author": getattr(p.author, "nombre", getattr(p.author, "email", "Usuario")),
            "content": p.content,
            "created_at": p.created_at.isoformat(),
            "updated_at": p.updated_at.isoformat() if p.updated_at else None,
            "editable": (p.user_id == current_user.id),
        })
    return jsonify(out), 200

# ---- CREATE: crear post
@forum_bp.post("/posts")
@login_required
def create_post():
    data = request.get_json(silent=True) or {}
    content = (data.get("content") or "").strip()
    if not content:
        return jsonify({"error": "El contenido no puede estar vacío."}), 400

    post = Post(user_id=current_user.id, content=content)
    db.session.add(post)
    db.session.commit()
    return jsonify({"id": post.id}), 201

# ---- UPDATE: actualizar post propio
@forum_bp.put("/posts/<int:post_id>")
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        return jsonify({"error": "No puedes editar esta publicación."}), 403

    data = request.get_json(silent=True) or {}
    content = (data.get("content") or "").strip()
    if not content:
        return jsonify({"error": "El contenido no puede estar vacío."}), 400

    post.content = content
    db.session.commit()
    return jsonify({"ok": True}), 200

# ---- DELETE: borrar post propio
@forum_bp.delete("/posts/<int:post_id>")
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        return jsonify({"error": "No puedes eliminar esta publicación."}), 403

    db.session.delete(post)
    db.session.commit()
    return jsonify({"ok": True}), 200

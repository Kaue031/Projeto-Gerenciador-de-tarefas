from flask import Flask, render_template, request, redirect, url_for
import db

app = Flask(__name__)

# Inicializa DB (cria arquivo tasks.db se necessário)
db.init_db()

@app.route('/')
def index():
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id, title FROM tasks ORDER BY id DESC')
    tasks = cur.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/create', methods=['POST'])
def create():
    title = request.form.get('title','').strip()
    desc = request.form.get('desc','').strip()
    if title:
        conn = db.get_conn()
        cur = conn.cursor()
        cur.execute('INSERT INTO tasks (title, desc) VALUES (?,?)', (title, desc))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/task/<int:id>')
def task_detail(id):
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks WHERE id=?', (id,))
    t = cur.fetchone()
    conn.close()
    if not t:
        return 'Tarefa não encontrada', 404
    return render_template('task.html', t=t)

@app.route('/edit/<int:id>')
def edit(id):
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks WHERE id=?', (id,))
    t = cur.fetchone()
    conn.close()
    if not t:
        return 'Tarefa não encontrada', 404
    return render_template('edit.html', t=t)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    title = request.form.get('title','').strip()
    desc = request.form.get('desc','').strip()
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute('UPDATE tasks SET title=?, desc=? WHERE id=?', (title, desc, id))
    conn.commit()
    conn.close()
    return redirect(url_for('task_detail', id=id))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute('DELETE FROM tasks WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

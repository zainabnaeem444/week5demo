from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pymysql
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

def get_db_connection():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )

# Home route
@app.route('/')
def index():
    return redirect(url_for('films'))

# Films Routes
@app.route('/films')
def films():
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute('''
                SELECT f.film_id, f.title, f.release_year, f.rental_rate, 
                       f.length, f.rating, c.name as category
                FROM film f
                LEFT JOIN film_category fc ON f.film_id = fc.film_id
                LEFT JOIN category c ON fc.category_id = c.category_id
                ORDER BY f.title
                LIMIT 100
            ''')
            films = cur.fetchall()
        conn.close()
        return render_template('films.html', films=films)
    except Exception as e:
        flash(f'Error fetching films: {str(e)}', 'error')
        return render_template('films.html', films=[])

@app.route('/films/add', methods=['GET', 'POST'])
def add_film():
    if request.method == 'POST':
        try:
            title = request.form['title']
            description = request.form['description']
            release_year = request.form['release_year'] or None
            language_id = request.form['language_id']
            rental_duration = request.form['rental_duration'] or 3
            rental_rate = request.form['rental_rate'] or 4.99
            length = request.form['length'] or None
            replacement_cost = request.form['replacement_cost'] or 19.99
            rating = request.form['rating']
            special_features = request.form.get('special_features', '')

            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute('''
                    INSERT INTO film (title, description, release_year, language_id, 
                                    rental_duration, rental_rate, length, replacement_cost, 
                                    rating, special_features)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (title, description, release_year, language_id, rental_duration,
                      rental_rate, length, replacement_cost, rating, special_features))
                
                conn.commit()
            conn.close()
            flash('Film added successfully!', 'success')
            return redirect(url_for('films'))
            
        except Exception as e:
            flash(f'Error adding film: {str(e)}', 'error')
    
    # Get languages for dropdown
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute('SELECT language_id, name FROM language')
            languages = cur.fetchall()
        conn.close()
    except Exception as e:
        languages = []
        flash(f'Error loading languages: {str(e)}', 'error')
    
    return render_template('film_form.html', film=None, languages=languages)

@app.route('/films/edit/<int:film_id>', methods=['GET', 'POST'])
def edit_film(film_id):
    conn = get_db_connection()
    
    if request.method == 'POST':
        try:
            title = request.form['title']
            description = request.form['description']
            release_year = request.form['release_year'] or None
            language_id = request.form['language_id']
            rental_duration = request.form['rental_duration'] or 3
            rental_rate = request.form['rental_rate'] or 4.99
            length = request.form['length'] or None
            replacement_cost = request.form['replacement_cost'] or 19.99
            rating = request.form['rating']
            special_features = request.form.get('special_features', '')

            with conn.cursor() as cur:
                cur.execute('''
                    UPDATE film 
                    SET title=%s, description=%s, release_year=%s, language_id=%s,
                        rental_duration=%s, rental_rate=%s, length=%s, 
                        replacement_cost=%s, rating=%s, special_features=%s
                    WHERE film_id=%s
                ''', (title, description, release_year, language_id, rental_duration,
                      rental_rate, length, replacement_cost, rating, special_features, film_id))
                
                conn.commit()
            conn.close()
            flash('Film updated successfully!', 'success')
            return redirect(url_for('films'))
            
        except Exception as e:
            flash(f'Error updating film: {str(e)}', 'error')
    
    # Get film data
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM film WHERE film_id = %s', (film_id,))
            film = cur.fetchone()
        
        # Get languages for dropdown
        with conn.cursor() as cur:
            cur.execute('SELECT language_id, name FROM language')
            languages = cur.fetchall()
        conn.close()
        
        if not film:
            flash('Film not found!', 'error')
            return redirect(url_for('films'))
        
        return render_template('film_form.html', film=film, languages=languages)
    except Exception as e:
        conn.close()
        flash(f'Error loading film: {str(e)}', 'error')
        return redirect(url_for('films'))

@app.route('/films/delete/<int:film_id>')
def delete_film(film_id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute('DELETE FROM film WHERE film_id = %s', (film_id,))
            conn.commit()
        conn.close()
        flash('Film deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting film: {str(e)}', 'error')
    
    return redirect(url_for('films'))

# Actors Routes
@app.route('/actors')
def actors():
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute('''
                SELECT actor_id, first_name, last_name, last_update
                FROM actor 
                ORDER BY first_name, last_name
                LIMIT 100
            ''')
            actors = cur.fetchall()
        conn.close()
        return render_template('actors.html', actors=actors)
    except Exception as e:
        flash(f'Error fetching actors: {str(e)}', 'error')
        return render_template('actors.html', actors=[])

@app.route('/actors/add', methods=['POST'])
def add_actor():
    try:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute('INSERT INTO actor (first_name, last_name) VALUES (%s, %s)', 
                       (first_name, last_name))
            conn.commit()
        conn.close()
        flash('Actor added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding actor: {str(e)}', 'error')
    
    return redirect(url_for('actors'))

@app.route('/actors/edit/<int:actor_id>', methods=['POST'])
def edit_actor(actor_id):
    try:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute('UPDATE actor SET first_name=%s, last_name=%s WHERE actor_id=%s', 
                       (first_name, last_name, actor_id))
            conn.commit()
        conn.close()
        flash('Actor updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating actor: {str(e)}', 'error')
    
    return redirect(url_for('actors'))

@app.route('/actors/delete/<int:actor_id>')
def delete_actor(actor_id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute('DELETE FROM actor WHERE actor_id = %s', (actor_id,))
            conn.commit()
        conn.close()
        flash('Actor deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting actor: {str(e)}', 'error')
    
    return redirect(url_for('actors'))

# API Routes for film details
@app.route('/api/film/<int:film_id>')
def get_film_details(film_id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            # Get film basic info
            cur.execute('''
                SELECT f.*, l.name as language_name, c.name as category
                FROM film f
                LEFT JOIN language l ON f.language_id = l.language_id
                LEFT JOIN film_category fc ON f.film_id = fc.film_id
                LEFT JOIN category c ON fc.category_id = c.category_id
                WHERE f.film_id = %s
            ''', (film_id,))
            film = cur.fetchone()
            
            # Get actors in the film
            cur.execute('''
                SELECT a.actor_id, a.first_name, a.last_name
                FROM actor a
                JOIN film_actor fa ON a.actor_id = fa.actor_id
                WHERE fa.film_id = %s
            ''', (film_id,))
            actors = cur.fetchall()
        
        conn.close()
        
        return jsonify({
            'film': film,
            'actors': actors
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
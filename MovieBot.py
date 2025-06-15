import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
import urllib.parse

OMDB_API_KEY = "e8bd375c"
OMDB_BASE_URL = "http://www.omdbapi.com/"

# 🎬 Genre to movie recommendations map
genre_recommendations = {
    "Action": ["John Wick", "Mad Max: Fury Road", "Die Hard", "Gladiator", "The Dark Knight"],
    "Comedy": ["The Hangover", "Superbad", "Step Brothers", "Mean Girls", "The Mask"],
    "Drama": ["The Shawshank Redemption", "Forrest Gump", "The Godfather", "Fight Club", "A Beautiful Mind"],
    "Romance": ["The Notebook", "Titanic", "La La Land", "Pride & Prejudice", "Before Sunrise"],
    "Sci-Fi": ["Inception", "Interstellar", "The Matrix", "Blade Runner 2049", "Arrival"],
    "Horror": ["The Conjuring", "Hereditary", "Get Out", "It", "A Quiet Place"]
}

def get_movie_details(movie_name):
    params = {'t': movie_name, 'apikey': OMDB_API_KEY}
    try:
        response = requests.get(OMDB_BASE_URL, params=params, timeout=5)
        data = response.json()
        if data['Response'] == 'True':
            imdb_rating = data.get('imdbRating')
            try:
                rating_float = float(imdb_rating)
                if rating_float >= 8.5:
                    comment = "🌟 Absolute masterpiece. Even your grandma has seen it twice."
                elif rating_float >= 7.0:
                    comment = "👍 Solid pick. You won't regret it."
                elif rating_float >= 5.5:
                    comment = "😐 Meh. Watchable if you’ve already scrolled Netflix for 3 hours."
                elif rating_float >= 4.0:
                    comment = "😬 Good luck staying awake."
                else:
                    comment = "💀 Warning: May cause extreme boredom and regret."
            except (TypeError, ValueError):
                comment = "❓ No rating. Suspiciously mysterious."

            youtube_search = f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(movie_name + ' trailer')}"

            details = {
                '🎬 Title': data.get('Title'),
                '📅 Year': data.get('Year'),
                '🔞 Rated': data.get('Rated'),
                '🗓 Released': data.get('Released'),
                '⏱️ Runtime': data.get('Runtime'),
                '🎭 Genre': data.get('Genre'),
                '🎬 Director': data.get('Director'),
                '📝 Plot': data.get('Plot'),
                '⭐ IMDb Rating': f"{imdb_rating} — {comment}",
                '📺 YouTube Trailer': youtube_search,
                'Poster': data.get('Poster') if data.get('Poster') != "N/A" else None
            }
            return details, data.get('Genre')
        else:
            return None, None
    except Exception:
        return None, None

def recommend_movies_by_genre(genre):
    if not genre:
        return []
    main_genre = genre.split(",")[0].strip()
    return genre_recommendations.get(main_genre, [])

def show_movie():
    movie_name = entry.get().strip()
    if not movie_name:
        messagebox.showwarning("Input Error", "Please enter a movie name.")
        return

    details, genre = get_movie_details(movie_name)
    if not details:
        messagebox.showerror("Not Found", f"Movie '{movie_name}' not found.")
        clear_display()
        return

    clear_display()

    # Get recommendations
    recommendations = recommend_movies_by_genre(genre)
    if recommendations:
        rec_text = "🍿 You might also like:\n" + "\n".join(f" - {title}" for title in recommendations) + "\n\n"
    else:
        rec_text = "🍿 No recommendations available.\n\n"

    # Prepare movie details (excluding poster)
    info = ""
    for key, value in details.items():
        if key != 'Poster':
            info += f"{key}: {value}\n\n"

    # Display recommendations + movie details in the white text box
    text_box.config(state='normal')
    text_box.insert(tk.END, rec_text + info)
    text_box.config(state='disabled')

    # Display poster image
    if details['Poster']:
        try:
            response = requests.get(details['Poster'])
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img.thumbnail((300, 450))
            poster_img = ImageTk.PhotoImage(img)
            poster_label.config(image=poster_img)
            poster_label.image = poster_img
        except Exception:
            poster_label.config(text="Poster not available")
    else:
        poster_label.config(text="Poster not available")

def clear_display():
    text_box.config(state='normal')
    text_box.delete(1.0, tk.END)
    text_box.config(state='disabled')
    poster_label.config(image='', text='')

# 🖥 GUI Setup
root = tk.Tk()
root.title("🎥 MovieBot GUI")
root.geometry("700x800")

entry = tk.Entry(root, font=("Arial", 14))
entry.pack(pady=10, fill=tk.X, padx=10)

search_button = tk.Button(root, text="Search", font=("Arial", 14), command=show_movie)
search_button.pack(pady=5)

text_box = tk.Text(root, height=18, font=("Arial", 12), wrap=tk.WORD)
text_box.pack(padx=10, pady=10, fill=tk.X)
text_box.config(state='disabled')

poster_label = tk.Label(root, text="Poster will appear here", font=("Arial", 12))
poster_label.pack(pady=10)

root.mainloop()

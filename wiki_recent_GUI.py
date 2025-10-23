import tkinter as tk
from tkinter import ttk, messagebox
import urllib.error
from wiki_recent import get_wikipedia_data


def fetch_revisions():
    article_title = textboxArticle.get().strip()

    # Validate input
    if not article_title:
        messagebox.showwarning("Input Error", "Please enter an article title.")
        return

    # Update UI
    labelStatus.config(text="Fetching data...", fg="blue")
    textResults.delete(1.0, tk.END)
    window.update_idletasks()

    try:
        parsed = get_wikipedia_data(article_title)

        # Handle redirects
        if "query" in parsed and "redirects" in parsed["query"]:
            redirect_from = parsed["query"]["redirects"][0]["from"]
            redirect_to = parsed["query"]["redirects"][0]["to"]
            labelStatus.config(
                text=f"Redirected from '{redirect_from}' to '{redirect_to}'", fg="orange"
            )
        else:
            labelStatus.config(text=f"Results for '{article_title}':", fg="green")

        # Find page and revisions
        pages = parsed.get("query", {}).get("pages", {})
        if not pages:
            textResults.insert(tk.END, "No article found.\n")
            labelStatus.config(text="Error: Article not found", fg="red")
            return

        page = next(iter(pages.values()))

        if "missing" in page:
            textResults.insert(tk.END, f"The article '{article_title}' does not exist.\n")
            labelStatus.config(text="Error: Missing article", fg="red")
            return

        revisions = page.get("revisions", [])
        if not revisions:
            textResults.insert(tk.END, "No revisions available.\n")
            labelStatus.config(text="No revisions found.", fg="orange")
            return

        # Display up to 30 revisions
        for rev in revisions:
            timestamp = rev.get("timestamp", "N/A")
            user = rev.get("user", "N/A")
            textResults.insert(tk.END, f"{timestamp} — {user}\n")

    except urllib.error.HTTPError as e:
        textResults.insert(tk.END, f"HTTP error: {e.code} {e.reason}\n")
        labelStatus.config(text="HTTP error occurred.", fg="red")
    except urllib.error.URLError as e:
        textResults.insert(tk.END, f"Network error: {e.reason}\n")
        labelStatus.config(text="Network error.", fg="red")
    except Exception as e:
        textResults.insert(tk.END, f"Unexpected error: {e}\n")
        labelStatus.config(text="Unexpected error occurred.", fg="red")


window = tk.Tk()
window.title("Wikipedia Revision Tracker")
window.geometry("650x450")

labelArticle = tk.Label(window, text="Enter Wikipedia Article:")
textboxArticle = tk.Entry(window, width=50)
buttonFetch = tk.Button(window, text="Get Revisions", command=fetch_revisions)
labelStatus = tk.Label(window, text="", fg="black")

# Textbox with scrollbar
textResults = tk.Text(window, height=18, width=80, wrap="word")
scrollbar = tk.Scrollbar(window, command=textResults.yview)
textResults.config(yscrollcommand=scrollbar.set)

# Layout (Grid)
labelArticle.grid(column=0, row=0, padx=10, pady=10, sticky="w")
textboxArticle.grid(column=1, row=0, padx=10, pady=10, sticky="w")
buttonFetch.grid(column=2, row=0, padx=10, pady=10)
labelStatus.grid(column=0, row=1, columnspan=3, padx=10, sticky="w")
textResults.grid(column=0, row=2, columnspan=3, padx=10, pady=10)
scrollbar.grid(column=3, row=2, sticky="ns")

window.mainloop()

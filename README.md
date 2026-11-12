# Euclidean Ear Test: putting it online

This folder is the whole game. Once it is on GitHub Pages it lives at a normal web address that anyone can open, with no accounts and nothing to install on their side.

What is in here:

| File or folder | What it is |
|---|---|
| `index.html` | The game and the About page, in one file |
| `tracks.json` | The list of clips. **Generated** by `build_tracks.py`, never edited by hand |
| `rhythms.json` | Names, descriptions and mnemonics. **You edit this one** |
| `build_tracks.py` | Reads `audio/` and `cards/` and writes `tracks.json` |
| `audio/` | Your MP3 clips |
| `cards/` | Your card images. `back.webp` is the card back, leave it where it is |

---

## Part 1. Fill the folder on your computer

1. **Clips.** Put the MP3s in `audio/`, named like `e4-15_Duh_Poteca.mp3`: `e`, then k, a dash, n, an underscore, then the title with underscores instead of spaces. Only that start and the `.mp3` ending matter. The title can use capitals, Greek, Cyrillic and accented letters, and the reveal shows it exactly as written. Avoid these characters in titles: `# % ? : * " < > |` and backslash (the script warns you). Several clips for one rhythm are fine, they just share the same `e4-15` start.
2. **Cards.** Put the card images in `cards/`, named `e4-15.webp` (`.png` works too). Same proportions as the cards you already made.
3. **Texts.** Open `rhythms.json` in any text editor and fill in the blanks. Every entry has `name`, `description` and `mnemonic`. A mnemonic has one syllable per step, `k` of them in CAPITALS, with hyphens between syllables and `_` for a rest.
4. **Build the list.** Open Terminal (Mac) or Command Prompt (Windows) in this folder and run:

   ```
   python3 build_tracks.py
   ```

   On Windows, `python build_tracks.py` or `py build_tracks.py` is the usual spelling. The script prints what it found. Lines starting with `check` mean a mnemonic does not have the right number of syllables or capitals. Lines starting with `warn` mean a clip has no card. Run it again after every change to `audio/`, `cards/` or `rhythms.json`.
5. **Try it.** In the same window run:

   ```
   python3 -m http.server 8000
   ```

   and open <http://localhost:8000> in your browser. Opening `index.html` with a double click will not work, because browsers refuse to read `tracks.json` from a plain file. Press `Ctrl+C` in the terminal when you are done.

---

## Part 2. Put it on GitHub (first time)

### Make an account and a repository

1. Go to <https://github.com> and click **Sign up**. Confirm your email address when GitHub asks.
2. Click the **+** at the top right and choose **New repository**.
3. **Repository name:** `euclidean-ear-test` (lowercase, no spaces). This becomes part of the web address.
4. Choose **Public**. GitHub Pages is free only for public repositories. This also means anyone can download the clips and cards.
5. Leave "Add a README file" **unticked**, then click **Create repository**.

### Upload the files: two ways

With about 80 clips (roughly 170 MB), **GitHub Desktop is the easier route**. The browser route needs no install, but you have to upload in batches.

#### Option A. GitHub Desktop (recommended)

1. Download it from <https://desktop.github.com>, install it and sign in with your GitHub account.
2. Choose **File → Add local repository…** and pick this folder (`euclidean-ear-test`). It will say the folder is not a Git repository. Click the **create a repository** link, then **Create repository**.
3. The left side lists every file. In the **Summary** box at the bottom left type something like `First version`, then click **Commit to main**.
4. Click **Publish repository** at the top. **Untick** "Keep this code private". Publish.
5. Later, when you add clips or change texts: run `build_tracks.py`, open GitHub Desktop, write a summary, click **Commit to main**, then **Push origin**.

#### Option B. The browser

GitHub's limits for browser uploads: **100 files at a time** and **25 MiB per file**. Your clips are about 2 MB each, so the size is fine, the count is the thing to watch.

1. Open your new repository and click **uploading an existing file** (or **Add file → Upload files**).
2. **Batch 1:** drag in `index.html`, `build_tracks.py`, `rhythms.json`, `tracks.json` and `README.md`, and drag the whole `cards` folder too. Folders keep their structure when dragged. Write a short message such as `Game and cards`, choose **Commit directly to the main branch**, and click **Commit changes**.
3. **Create the audio folder:** click **Add file → Create new file**. In the name box type `audio/readme.txt` (typing the slash makes the folder), put any text in the file, and commit.
4. **Batch 2 and onward:** click the new `audio` folder to open it, then **Add file → Upload files**, and drop in 25 to 40 clips at a time. Commit each batch. Repeat until all clips are in.

### Switch on the website

1. In your repository click **Settings** (top row of tabs).
2. In the left sidebar click **Pages**.
3. Under **Build and deployment**, set **Source** to **Deploy from a branch**.
4. Under **Branch**, choose **main** and the folder **/ (root)**, then click **Save**.
5. Wait a minute or two (GitHub says up to ten). Reload the Pages settings screen: the address appears at the top, in the form `https://YOURNAME.github.io/euclidean-ear-test/`. That is your game. Bookmark it.

---

## Part 3. Adding more later

1. Add or change files in `audio/`, `cards/` or `rhythms.json`.
2. Run `python3 build_tracks.py` again. It rewrites `tracks.json`.
3. Send the changes to GitHub: with GitHub Desktop, commit and push. In the browser, upload the new files again (a file with the same name is replaced). **Always include the new `tracks.json`.**
4. Give GitHub a minute or two, then reload the game with `Ctrl+Shift+R` (Mac: `Cmd+Shift+R`) so the browser fetches the fresh list.

---

## Good to know

- **Capital letters and other alphabets.** You do not need to rename files. The script copies each name into `tracks.json` exactly as it is on your disk, and the game asks for that same name, so the two always agree. Online, `Track.mp3` and `track.mp3` are different files, so if you rename a file later, run `build_tracks.py` again before uploading.
- **About page links** are near the top of the script at the bottom of `index.html`, in the line that starts with `const LINKS`.
- **Size and traffic.** GitHub Pages sites should stay under 1 GB and about 100 GB of traffic a month. One round of the game is roughly 3 MB, so that is a very large number of rounds. If you ever outgrow it, the audio can move to Cloudflare R2 with one change to the file paths.

## If something goes wrong

| What you see | Most likely cause |
|---|---|
| "Could not load tracks.json" | `tracks.json` was not uploaded, or you opened `index.html` by double click. Use the web address or `http.server` |
| "No clips found" | `tracks.json` is the empty starter file. Run `build_tracks.py`, then upload the new one |
| A clip says it would not load | The file was renamed after running the script, or that batch has not been uploaded yet |
| A card does not appear after solving | No file called `e{k}-{n}.webp` in `cards/` for that rhythm |
| The address shows a 404 page | Pages is not live yet (wait a few minutes), or Settings → Pages is not set to `main` and `/ (root)` |
| "File too large" on upload | The file is over 25 MiB. Re-export the MP3 at a lower bitrate, or use GitHub Desktop |

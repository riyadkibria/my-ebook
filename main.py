from pathlib import Path
import zipfile
import shutil
import re
from bs4 import BeautifulSoup


# ==================================================
# SETTINGS
# ==================================================

EPUB_FOLDER = Path(
    r"D:\epub_processor\books"
)

OUTPUT_FOLDER = Path(
    r"D:\epub_processor\output"
)

TEMP_FOLDER = Path(
    r"D:\epub_processor\temp"
)


# ==================================================
# CLEAN TEXT
# ==================================================

def clean_text(text):

    # remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    # remove leading/trailing spaces
    text = text.strip()

    return text



# ==================================================
# EXTRACT EPUB
# ==================================================

def extract_epub(epub_file, extract_path):

    if extract_path.exists():

        shutil.rmtree(
            extract_path
        )

    extract_path.mkdir(
        parents=True,
        exist_ok=True
    )


    with zipfile.ZipFile(
        epub_file,
        "r"
    ) as zip_ref:

        zip_ref.extractall(
            extract_path
        )



# ==================================================
# FIND XHTML FILES
# ==================================================

def find_chapters(epub_folder):

    files = []

    for file in epub_folder.rglob("*"):

        if file.suffix.lower() in [
            ".xhtml",
            ".html",
            ".htm"
        ]:

            files.append(file)


    return sorted(files)



# ==================================================
# CONVERT XHTML TO MARKDOWN
# ==================================================

def xhtml_to_markdown(file):


    try:

        html = file.read_text(
            encoding="utf-8"
        )


    except UnicodeDecodeError:


        html = file.read_text(
            encoding="latin-1"
        )


    soup = BeautifulSoup(
        html,
        "lxml"
    )


    # remove unwanted elements

    for tag in soup(
        [
            "script",
            "style",
            "nav"
        ]
    ):

        tag.decompose()



    text = soup.get_text(
        "\n"
    )


    text = clean_text(
        text
    )


    return text



# ==================================================
# SAVE MARKDOWN CHAPTERS
# ==================================================

def process_book(epub_file):


    book_name = epub_file.stem


    print(
        "\n======================"
    )

    print(
        "Processing:",
        book_name
    )

    print(
        "======================"
    )



    temp_book = TEMP_FOLDER / book_name


    extract_epub(
        epub_file,
        temp_book
    )



    chapters = find_chapters(
        temp_book
    )


    if not chapters:

        print(
            "No chapters found"
        )

        return



    output_book = OUTPUT_FOLDER / book_name


    output_book.mkdir(
        parents=True,
        exist_ok=True
    )



    chapter_number = 1



    for chapter in chapters:


        text = xhtml_to_markdown(
            chapter
        )


        if len(text) < 100:

            continue



        markdown_content = f"""
# {chapter.stem}


{text}

"""



        output_file = (
            output_book /
            f"chapter_{chapter_number:03}.md"
        )


        output_file.write_text(
            markdown_content,
            encoding="utf-8"
        )


        print(
            "Saved:",
            output_file.name
        )


        chapter_number += 1



    print(
        "\nCompleted:",
        book_name
    )



# ==================================================
# MAIN
# ==================================================

def main():


    if not EPUB_FOLDER.exists():

        print(
            "EPUB folder missing:",
            EPUB_FOLDER
        )

        return



    OUTPUT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )



    epub_files = list(
        EPUB_FOLDER.glob(
            "*.epub"
        )
    )



    if not epub_files:

        print(
            "No EPUB files found"
        )

        return



    print(
        f"Found {len(epub_files)} EPUB file(s)"
    )



    for epub in epub_files:

        process_book(
            epub
        )



    print(
        "\n======================"
    )

    print(
        "ALL BOOKS COMPLETED"
    )

    print(
        "======================"
    )



if __name__ == "__main__":

    main()
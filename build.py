
from pathlib import Path
import markdown
import re
import shutil


# ==========================
# SETTINGS
# ==========================

SOURCE_FOLDER = Path(
    r"D:\epub_processor\output"
)

OUTPUT_FOLDER = Path(
    r"D:\epub_processor\generated"
)


ASSET_FOLDER = OUTPUT_FOLDER / "assets"



# ==========================
# CLEAN OLD OUTPUT
# ==========================

def clean_output():

    if OUTPUT_FOLDER.exists():

        for item in OUTPUT_FOLDER.iterdir():

            if item.name != "":

                if item.is_dir():

                    shutil.rmtree(item)

                else:

                    item.unlink()



# ==========================
# SAFE FILE NAME
# ==========================

def slugify(text):

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9]+",
        "-",
        text
    )

    return text.strip("-")



# ==========================
# CREATE ASSETS
# ==========================

def create_assets():

    ASSET_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )


    style = """

body{

background:#f4f4f4;
font-family:Georgia,serif;
line-height:1.8;
padding:20px;

}


.container{

max-width:900px;
margin:auto;

}


h1{

text-align:center;

}


.book{

background:white;
padding:30px;
margin-bottom:30px;
border-radius:12px;

}


.chapter{

background:white;
padding:30px;
margin-bottom:40px;
border-radius:12px;

}


.content{

font-size:20px;

}


button{

padding:12px;
margin:8px;
cursor:pointer;
border-radius:8px;
border:none;

}



@media(max-width:600px){

button{

width:100%;

}


.content{

font-size:18px;

}


}

"""


    (ASSET_FOLDER / "style.css").write_text(
        style,
        encoding="utf-8"
    )



    js = """

function getText(id){

return document
.getElementById(id)
.innerText
.trim();

}



function copyText(text){

if(navigator.clipboard){

navigator.clipboard.writeText(text)
.then(()=>alert("Copied"));

}

else{

let box=document.createElement("textarea");

box.value=text;

document.body.appendChild(box);

box.select();

document.execCommand("copy");

box.remove();

alert("Copied");

}

}



function sentenceCut(words,limit){

if(words.length<=limit)

return words.length;


for(let i=limit;i<words.length;i++){

if(/[.!?]["']?$/.test(words[i]))

return i+1;

}


return words.length;

}




function copyFirst(id){

let words=getText(id)
.split(/\\s+/);


let end=sentenceCut(words,1500);


copyText(

words.slice(0,end)
.join(" ")

);

}



function copyRemaining(id){

let words=getText(id)
.split(/\\s+/);


let end=sentenceCut(words,1500);


copyText(

words.slice(end)
.join(" ")

);

}



function copyFull(id){

copyText(
getText(id)
);

}

"""


    (ASSET_FOLDER / "app.js").write_text(
        js,
        encoding="utf-8"
    )



# ==========================
# CREATE BOOK HTML
# ==========================

def create_book(book):


    chapters = sorted(
        book.glob("*.md")
    )


    if not chapters:

        return None



    filename = (
        slugify(book.name)
        +
        ".html"
    )


    html = f"""

<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width,initial-scale=1">

<title>{book.name}</title>


<link rel="stylesheet"
href="assets/style.css">

</head>


<body>


<div class="container">


<h1>{book.name}</h1>

"""


    for index,chapter in enumerate(chapters,1):


        text = chapter.read_text(
            encoding="utf-8"
        )


        converted = markdown.markdown(
            text,
            extensions=[
                "extra",
                "tables"
            ]
        )


        cid = f"chapter{index}"


        html += f"""

<div class="chapter">


<h2>{chapter.stem}</h2>


<div class="content"
id="{cid}">

{converted}

</div>


<button onclick="copyFirst('{cid}')">

COPY FIRST 1500 WORDS

</button>


<button onclick="copyRemaining('{cid}')">

COPY REMAINING

</button>


<button onclick="copyFull('{cid}')">

COPY FULL CHAPTER

</button>


</div>


"""


    html += """

</div>


<script src="assets/app.js"></script>


</body>

</html>

"""


    output = OUTPUT_FOLDER / filename


    output.write_text(
        html,
        encoding="utf-8"
    )


    return (
        book.name,
        filename
    )



# ==========================
# CREATE INDEX
# ==========================

def create_index(books):


    html = """

<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width,initial-scale=1">


<title>Book Library</title>


<link rel="stylesheet"
href="assets/style.css">


</head>


<body>


<div class="container">


<h1>

MY BOOK LIBRARY

</h1>

"""


    for name,file in books:


        html += f"""

<div class="book">


<h2>{name}</h2>


<a href="{file}">

<button>

OPEN BOOK

</button>

</a>


</div>


"""


    html += """

</div>


</body>

</html>

"""


    (
        OUTPUT_FOLDER / "index.html"
    ).write_text(
        html,
        encoding="utf-8"
    )



# ==========================
# MAIN
# ==========================

def main():


    clean_output()


    OUTPUT_FOLDER.mkdir(
        exist_ok=True
    )


    create_assets()


    books=[]


    for folder in SOURCE_FOLDER.iterdir():

        if folder.is_dir():

            result=create_book(folder)

            if result:

                books.append(result)



    create_index(books)


    print()

    print(
        "WEBSITE GENERATED SUCCESSFULLY"
    )



if __name__=="__main__":

    main()
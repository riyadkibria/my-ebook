

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
.split(/\s+/);


let end=sentenceCut(words,1500);


copyText(

words.slice(0,end)
.join(" ")

);

}



function copyRemaining(id){

let words=getText(id)
.split(/\s+/);


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


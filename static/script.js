// =========================
// GLOBALS
// =========================

let currentPdf = null;

let recentQuestions = [];


// =========================
// DOM
// =========================

const uploadBtn =
document.getElementById("uploadBtn");

const pdfInput =
document.getElementById("pdfFile");

const askBtn =
document.getElementById("askBtn");

const questionInput =
document.getElementById("questionInput");

const answerCard =
document.getElementById("answerCard");

const answerText =
document.getElementById("answerText");

const sourceCard =
document.getElementById("sourceCard");

const sourcePage =
document.getElementById("sourcePage");

const pdfName =
document.getElementById("pdfName");

const removePdfBtn =
document.getElementById("removePdfBtn");

const openPdfBtn =
document.getElementById("openPdfBtn");

const openSourceBtn =
document.getElementById("openSourceBtn");

const recentQuestionsBox =
document.getElementById("recentQuestions");

const pagesCount =
document.getElementById("pagesCount");

const wordsCount =
document.getElementById("wordsCount");

const chunksCount =
document.getElementById("chunksCount");


// =========================
// UPLOAD PDF
// =========================

uploadBtn.addEventListener(
"click",
async () => {

    const file =
    pdfInput.files[0];

    if(!file){

        alert(
        "Please select a PDF first."
        );

        return;
    }

    const formData =
    new FormData();

    formData.append(
        "pdf",
        file
    );

    uploadBtn.innerText =
    "Uploading...";

    try{

        const response =
        await fetch(
            "/upload",
            {
                method:"POST",
                body:formData
            }
        );

        const data =
        await response.json();

        if(data.success){

            currentPdf =
            data.pdf_name;

            pdfName.innerText =
            data.pdf_name;

            pagesCount.innerText =
            data.stats.pages;

            wordsCount.innerText =
            data.stats.words;

            chunksCount.innerText =
            data.stats.chunks;

            alert(
            "PDF uploaded successfully."
            );
        }

    }catch(error){

        alert(
        "Upload failed."
        );

        console.log(error);
    }

    uploadBtn.innerText =
    "Upload PDF";

});


// =========================
// ASK QUESTION
// =========================

askBtn.addEventListener(
"click",
async () => {

    const question =
    questionInput.value.trim();

    if(question === ""){

        alert(
        "Enter a question."
        );

        return;
    }

    askBtn.innerText =
    "Thinking...";

    try{

        const response =
        await fetch(
            "/ask",
            {
                method:"POST",

                headers:{
                    "Content-Type":
                    "application/json"
                },

                body:JSON.stringify(
                    {
                        question
                    }
                )
            }
        );

        const data =
        await response.json();

        answerCard.classList.remove(
            "hidden"
        );

        answerText.innerText =
        data.answer;

        if(data.page){

            sourceCard.classList.remove(
                "hidden"
            );

            sourcePage.innerText =
            `Page ${data.page}`;
        }

        addRecentQuestion(
            question
        );

    }catch(error){

        alert(
        "Failed to generate answer."
        );

        console.log(error);
    }

    askBtn.innerText =
    "Ask Question";

});


// =========================
// REMOVE PDF
// =========================

removePdfBtn.addEventListener(
"click",
async () => {

    try{

        const response =
        await fetch(
            "/remove_pdf",
            {
                method:"POST"
            }
        );

        const data =
        await response.json();

        if(data.success){

            currentPdf = null;

            pdfName.innerText =
            "No PDF Uploaded";

            pagesCount.innerText =
            "0";

            wordsCount.innerText =
            "0";

            chunksCount.innerText =
            "0";

            answerCard.classList.add(
                "hidden"
            );

            sourceCard.classList.add(
                "hidden"
            );

            alert(
            "PDF removed."
            );
        }

    }catch(error){

        console.log(error);
    }

});


// =========================
// OPEN PDF
// =========================

openPdfBtn.addEventListener(
"click",
() => {

    window.open(
        "/pdf",
        "_blank"
    );

});

openSourceBtn.addEventListener(
"click",
() => {

    window.open(
        "/pdf",
        "_blank"
    );

});


// =========================
// SUGGESTIONS
// =========================

document
.querySelectorAll(
".suggestion-btn"
)
.forEach(btn => {

    btn.addEventListener(
    "click",
    () => {

        questionInput.value =
        btn.innerText;

        questionInput.focus();
    });

});


// =========================
// RECENT QUESTIONS
// =========================

function addRecentQuestion(
question
){

    if(
        recentQuestions.includes(
        question
        )
    ){
        return;
    }

    recentQuestions.unshift(
        question
    );

    if(
        recentQuestions.length > 10
    ){
        recentQuestions.pop();
    }

    renderRecentQuestions();
}

function renderRecentQuestions(){

    recentQuestionsBox.innerHTML =
    "";

    recentQuestions.forEach(
    question => {

        const div =
        document.createElement(
        "div"
        );

        div.className =
        "recent-item";

        div.innerText =
        question;

        div.onclick = () => {

            questionInput.value =
            question;
        };

        recentQuestionsBox.appendChild(
            div
        );

    });
}


// =========================
// TOGGLE SIDEBAR HISTORY
// =========================

function toggleRecentQuestions(){

    const container =
    document.getElementById(
    "recentQuestions"
    );

    const arrow =
    document.getElementById(
    "recentArrow"
    );

    container.classList.toggle(
        "hidden"
    );

    if(
        container.classList.contains(
        "hidden"
        )
    ){

        arrow.innerText =
        "▼";
    }
    else{

        arrow.innerText =
        "▲";
    }
}
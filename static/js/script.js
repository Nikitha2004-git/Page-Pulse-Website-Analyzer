let history = [];
let latestData = {};

async function analyzeWebsite() {

    document.getElementById("error").style.display = "none";
    document.getElementById("copyBtn").style.display = "none";

    const url = document.getElementById("url").value.trim();

    if (url === "") {
        showError("Please enter a website URL.");
        return;
    }

    document.getElementById("loading").style.display = "block";

    try {

        const response = await fetch("/analyze/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                url: url
            })
        });

        const data = await response.json();

        document.getElementById("loading").style.display = "none";

        if (data.error) {
            showError(data.error);
            return;
        }

        latestData = data;

        // ---------- HISTORY ----------

        history.unshift(url);

        history = [...new Set(history)];

        if(history.length > 5){

            history.pop();

        }

        const list = document.getElementById("historyList");

        list.innerHTML = "";

        history.forEach(site=>{

            const li=document.createElement("li");

            li.innerHTML="🌐 "+site;

            list.appendChild(li);

        });

        document.getElementById("copyBtn").style.display = "inline-block";

        // SEO Score
        document.getElementById("seo").innerHTML =
            data.seo_score + " / 100";

        const grade = document.getElementById("grade");

        grade.innerHTML = data.grade;

        grade.className = "grade";

        if(data.grade === "A")
            grade.classList.add("gradeA");

        else if(data.grade === "B")
            grade.classList.add("gradeB");

        else if(data.grade === "C")
            grade.classList.add("gradeC");

        else if(data.grade === "D")
            grade.classList.add("gradeD");

        else
            grade.classList.add("gradeF");

        // -------- Status Badge --------

        const badge = document.getElementById("statusBadge");

        let statusClass = "";
        let statusText = "";

        if (data.status >= 200 && data.status < 300) {

            statusClass = "badge success";
            statusText = "🟢 " + data.status + " OK";

        } else if (data.status >= 300 && data.status < 400) {

            statusClass = "badge redirect";
            statusText = "🔵 " + data.status + " Redirect";

        } else if (data.status >= 400 && data.status < 500) {

            statusClass = "badge client-error";
            statusText = "🟠 " + data.status + " Client Error";

        } else if (data.status >= 500) {

            statusClass = "badge server-error";
            statusText = "🔴 " + data.status + " Server Error";

        } else {

            statusClass = "badge unknown";
            statusText = data.status;

        }

        badge.className = statusClass;
        badge.innerHTML = statusText;

        // Other Results
        document.getElementById("time").innerHTML = data.response_time;
        document.getElementById("title").innerHTML = data.title;

        const icon = document.getElementById("favicon");

        icon.src = data.favicon;
        icon.style.display = "block";
        document.getElementById("meta").innerHTML = data.meta_description;
        document.getElementById("h1").innerHTML = data.h1_count;
        document.getElementById("alt").innerHTML = data.images_missing_alt;
        document.getElementById("words").innerHTML = data.word_count;
        document.getElementById("images").innerHTML = data.total_images;
        document.getElementById("links").innerHTML = data.total_links;

    }
    catch (error) {

        document.getElementById("loading").style.display = "none";

        showError("Something went wrong. Please try again.");

        console.error(error);

    }

}

function showError(message) {

    const box = document.getElementById("error");

    box.innerHTML = message;

    box.style.display = "block";

}

document.getElementById("copyBtn").onclick = function () {

    navigator.clipboard.writeText(
        JSON.stringify(latestData, null, 4)
    );

    this.innerHTML = "✅ Copied";

    setTimeout(() => {

        this.innerHTML = "Copy JSON";

    }, 2000);

};

// ---------------- PDF REPORT ----------------

document.getElementById("downloadPdf").onclick=function(){

    if(Object.keys(latestData).length===0){

        alert("Analyze a website first.");

        return;

    }

    const report=`
PAGE PULSE REPORT

----------------------------

Status : ${latestData.status}

SEO Score : ${latestData.seo_score}/100

Response Time : ${latestData.response_time}

Title :

${latestData.title}

Meta Description :

${latestData.meta_description}

H1 Count :

${latestData.h1_count}

Missing ALT :

${latestData.images_missing_alt}

Word Count :

${latestData.word_count}

Total Images :

${latestData.total_images}

Total Links :

${latestData.total_links}

`;

    const blob=new Blob([report],{

        type:"text/plain"

    });

    const link=document.createElement("a");

    link.href=URL.createObjectURL(blob);

    link.download="PagePulse_Report.txt";

    link.click();

};
// ---------------- DARK MODE ----------------

function toggleTheme(){

    document.body.classList.toggle("dark");

    const btn=document.getElementById("themeBtn");

    if(document.body.classList.contains("dark")){

        btn.innerHTML="☀️ Light Mode";

    }
    else{

        btn.innerHTML="🌙 Dark Mode";

    }

}
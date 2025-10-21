let courtComplex = document.getElementById('complex')
let courtName = document.getElementById('courtName')
let civil = document.getElementById('civil')
let criminal = document.getElementById('criminal')
let image = document.getElementById('captchaImage')
let submitButton = document.getElementById('submitBtn')
let data = null
let count = 1

window.onload = ()=>{
    creatingSession()
}

async function creatingSession() {
    // Your code here
    img = await fetch(`http://127.0.0.1:60/creatingSession`)
    jsonImg = await img.json()
    image.src = jsonImg
}

function emptyCourtName(){
    courtName.innerHTML = ""
    let option = document.createElement('option')
    option.value=''
    option.text = '-- Select Court Name --'
    courtName.append(option) 
}

let pointerArray = []
function loading(){
    document.querySelector('.body').style.opacity = '0.6'
    document.querySelector('.loader').style.visibility = 'visible'
    pointerArray = document.querySelectorAll('.select-tags,.btn')
    pointerArray.forEach((ele) => {
        ele.style.pointerEvents = 'none'
    })
}

function unload(){
    document.querySelector('.loader').style.visibility = 'hidden'
    document.querySelector('.body').style.opacity = '1'
    pointerArray.forEach((ele) => {
        ele.style.pointerEvents = 'auto'
    })
    pointerArray = []
}

async function fillCourtNames(){
    emptyCourtName()
    let civcri
    if(civil.checked){
        civcri = 2
    }
    else{
        civcri = 3
    }
    if (courtComplex.value != -1) {
        let jsondata
        if (data == null || data == undefined) {
            loading()
            data = await fetch(`http://127.0.0.1:60/gettingCourtNames/${civcri}`)
            jsondata = await data.json()
            data = null
        }
        for(const i of jsondata){
            if(i['code'] == ""){
                continue
            }   
            let createOption = document.createElement('option')
            createOption.textContent = `${i['courtName']}`
            createOption.value =  `${i['code']}`
            courtName.append(createOption)
        }
        unload()
    }
}

function causingLoading(){
    popup.innerHTML = `Fetching causelist of court ${courtName[count].innerHTML}`
    document.querySelector('.body').style.opacity = '0.6'
    pointerArray = document.querySelectorAll('.select-tags,.btn')
    pointerArray.forEach((ele) => {
        ele.style.pointerEvents = 'none'
    })
}

function causingUnloading(){
    popup.style.display = "none";
    document.querySelector('.body').style.opacity = '1'
    pointerArray.forEach((ele) => {
        ele.style.pointerEvents = 'auto'
    })
    pointerArray = []
}

async function fetchingCauseList(e){
    e.preventDefault()
    let date = document.getElementById('date').value
    const reversed = date.split("-").reverse().join("-");
    let civcri
    if(civil.checked){
        civcri = 2
    }
    else{
        civcri = 3
    }
    let captcha;
    captcha = document.getElementById('captcha').value
    const popup = document.getElementById("popup");

  // show popup before fetch
    causingLoading()
    popup.style.display = "block";
    try {
        const response = await fetch(`http://127.0.0.1:60/fetchingEachCauseList/${courtName[count].value}/${reversed}/${civcri}/${captcha}/${count}`);
        if (!response.ok) throw new Error("Please enter correct captcha");
        courtName.selectedIndex = count
        count += 1
        creatingSession()
  } catch (err) {
        alert(err)
        console.error("Error fetching:", err);
  } 
  finally{
    causingUnloading()
  }
    // let data = await fetch(`http://127.0.0.1:60/fetchingEachCauseList/${courtName[count].value}/${reversed}/${civcri}/${captcha}/${count}`)
}

courtComplex.addEventListener('change',fillCourtNames)
submitButton.addEventListener('click',fetchingCauseList)
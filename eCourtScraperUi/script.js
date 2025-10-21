let states = document.getElementById('state')
let districts = document.getElementById('district')
let courtComplexes = document.getElementById('complex')
let courtNames = document.getElementById('courtName')
let courtEstablishments = document.getElementById('establishment')
let data = null;

function emptyDistrict(){
    // districts.previousElementSibling.style.display = 'block'
    districts.innerHTML = ""
    let option = document.createElement('option')
    option.value=''
    option.text = '-- Select District --'
    districts.append(option)
}

function emptyCourtComplex(){
    courtComplexes.previousElementSibling.style.display = 'none'
    courtComplexes.innerHTML = ""
    let option = document.createElement('option')
    option.value=''
    option.text = '-- Select Court Complex --' 
    courtComplexes.append(option)
}

function emptyCourtEstablishment(){
    courtEstablishments.previousElementSibling.style.display = 'none'
    courtEstablishments.innerHTML = ""
    let option = document.createElement('option')
    option.value=''
    option.text = '-- Select Court Establishment --' 
    courtEstablishments.append(option)
}

function emptyCourtName(){
    courtNames.previousElementSibling.style.display = 'none'
    courtNames.innerHTML = ""
    let option = document.createElement('option')
    option.value=''
    option.text = '-- Select Court Name --'
    courtNames.append(option) 
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

(async function fillstates(){
    // states.previousElementSibling.style.display = 'block'
    let jsondata
    if (data == null || data == undefined) {
        loading()
        data = await fetch('http://127.0.0.1:60/fetchingstates')
        jsondata = await data.json()
        data = null
    }
    for(const i of jsondata){
        let createOption = document.createElement('option')
        createOption.textContent = `${i['stateName']}`
        createOption.value =  `${i['stateCode']}`
        states.append(createOption)
    }
    unload()
}
)();

async function filldistricts(){
    emptyDistrict()
    emptyCourtComplex()
    emptyCourtEstablishment()
    emptyCourtName()
    let jsondata
    if (data == null || data == undefined) {
        let stateValue = states.value
        loading()
        data = await fetch(`http://127.0.0.1:60/fetchingdistricts/${stateValue}`)
        jsondata = await data.json()
        data = null
    }

    for(const i of jsondata){
        if(i['code'] == ""){
            continue
        }
        let createOption = document.createElement('option')
        createOption.textContent = `${i['district']}`
        createOption.value =  `${i['code']}`
        districts.append(createOption)
    }
    unload()
}

async function fillCourtComplexes(){
    emptyCourtComplex()
    emptyCourtEstablishment()
    emptyCourtName()
    let jsondata
    if (data == null || data == undefined) {
        let stateValue = states.value
        let districtValue = districts.value
        loading()
        data = await fetch(`http://127.0.0.1:60/fetchingCourtComplex/${stateValue}/${districtValue}`)
        jsondata = await data.json()
        data = null
    }
    if (jsondata.length != 1) {
        courtComplexes.previousElementSibling.style.display = 'block'
    }
    for(const i of jsondata){
        if(i['code'] == ""){
            continue
        }
        let createOption = document.createElement('option')
        createOption.textContent = `${i['courtComplex']}`
        createOption.value =  `${i['code']}`
        courtComplexes.append(createOption)
    }
    unload()
}

async function fillCourtEstablishments(){
    emptyCourtEstablishment()
    let jsondata
    if (data == null || data == undefined) {
        let stateValue = states.value
        let districtValue = districts.value
        let courtComplexValue = courtComplexes.value
        loading()
        data = await fetch(`http://127.0.0.1:60/fetchingCourtEstablishment/${stateValue}/${districtValue}/${courtComplexValue}`)
        jsondata = await data.json()
        data = null
    }
    if (jsondata.length != 1) {
        courtEstablishments.previousElementSibling.style.display = 'block'
    }
    for(const i of jsondata){
        if(i['code'] == ""){
            continue
        }
        let createOption = document.createElement('option')
        createOption.textContent = `${i['courtEstablishment']}`
        createOption.value =  `${i['code']}`
        courtEstablishments.append(createOption)
    }
    unload()
}

async function fillCourtNames(){
    emptyCourtName()
    let jsondata
    if (data == null || data == undefined) {
        let stateValue = states.value
        let districtValue = districts.value
        let courtComplexValue = courtComplexes.value
        loading()
        data = await fetch(`http://127.0.0.1:60/fetchingCourtNames/${stateValue}/${districtValue}/${courtComplexValue}`)
        jsondata = await data.json()
        data = null
    }
    if (jsondata.length != 1) {
        courtNames.previousElementSibling.style.display = 'block'
    }
    for(const i of jsondata){
        if(i['code'] == ""){
            continue
        }
        let createOption = document.createElement('option')
        if(i['code'] == 'D'){
            createOption.disabled = true
        }
        createOption.textContent = `${i['courtName']}`
        createOption.value =  `${i['code']}`
        courtNames.append(createOption)
    }
    unload()
}
states.addEventListener('change',filldistricts)
districts.addEventListener('change',fillCourtComplexes)
courtComplexes.addEventListener('change',fillCourtEstablishments)
courtComplexes.addEventListener('change',fillCourtNames)
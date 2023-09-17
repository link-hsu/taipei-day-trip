//  全域變數
//getUrl/<id>
let urlAttraction = "";
let urlModel = "/api";
urlAttraction = urlModel + location.pathname;

//sectionLeft
const imgBackground = document.querySelector(".imgBackground");
let imgBackgroundList = [];
let imgAmounts = 0;

//sectionRight
const attractionName = document.querySelector(".attractionName");
const attractionSort = document.querySelector(".attractionSort");
const Btnmorning = document.querySelector(".Btnmorning");
const Btnnoon = document.querySelector(".Btnnoon");
const fee = document.querySelector(".fee");

const describe = document.querySelector(".describe");
const address = document.querySelector(".address");
const transport = document.querySelector(".transport");

//===========   set the date of today
let Today = new Date();
let dateIn = document.querySelector(".dateIn");
todayModel =
    String(Today.getFullYear()) +
    "-" +
    String(Today.getMonth() + 1) +
    "-" +
    String(Today.getDate());
dateIn = document.querySelector(".dateIn");
dateIn.value = todayModel;
dateIn.min = todayModel;

//===========   Price of morning & noon
Btnmorning.addEventListener(
    "click",
    function (e) {
        fee.textContent = "新台幣 2000 元";
    },
    false
);
Btnnoon.addEventListener(
    "click",
    function (e) {
        fee.textContent = "新台幣 2500 元";
    },
    false
);

//===========   getAttractionDatas  ===========
//urlAttraction=urlModel+"{id}"
function getAttractionData() {
    fetch(urlAttraction)
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            imgBackgroundList = data["data"]["images"];
            imgBackground.setAttribute("src", imgBackgroundList[0]);
            attractionName.textContent = data["data"]["name"];
            attractionSort.textContent =
                data["data"]["category"] + "at" + data["data"]["mrt"];
            describe.textContent = data["data"]["description"];
            address.textContent = data["data"]["address"];
            transport.textContent = data["data"]["transport"];
            carouselFunction();
        });
}
getAttractionData();

//===========   carouselfunction    ===========
let carousePosition = 0;
let eachCarouselInturnID = 0;
function carouselFunction() {
    carousePosition = 0;
    imgAmounts = imgBackgroundList.length;
    let carouselUnderBlock = document.querySelector(".carouselUnderBlock");
    for (let i = 0; i < imgAmounts; i++) {
        let carouselInturn = document.createElement("div");
        carouselInturn.setAttribute("class", "carouselInturn");
        //carouselInturn add id attribute by img position
        carouselInturn.setAttribute("id", i);
        let carouselInturnshow = document.createElement("div");
        carouselInturnshow.setAttribute("class", "carouselInturnshow");
        //carouselInturnshow add id attribute by img position
        carouselInturnshow.setAttribute("id", i);
        carouselInturn.appendChild(carouselInturnshow);
        carouselUnderBlock.appendChild(carouselInturn);
        //set listener to each BlackPointBlock
        eachCarouselInturnID = i;
        setListenerforEachCarouselInturn();
    }
    //Default Black Point show the first one
    const carouseBlackPoint = document.querySelectorAll(".carouselInturnshow");
    carouseBlackPoint[0].style.display = "block";

    //BtnLeft
    const BtnLeft = document.querySelector(".carouselBtnleft");
    BtnLeft.addEventListener(
        "click",
        function (e) {
            carousePosition -= 1;
            carouseReturnJudge();
            setBlackPoint();
        },
        false
    );

    //BtnRight
    const BtnRight = document.querySelector(".carouselBtnright");
    BtnRight.addEventListener(
        "click",
        function (e) {
            carousePosition += 1;
            carouseReturnJudge();
            setBlackPoint();
        },
        false
    );
}

//===========   ReturnJudge
function carouseReturnJudge() {
    if (carousePosition < 0) {
        carousePosition = imgAmounts - 1;
    } else if (carousePosition == imgAmounts) {
        carousePosition = 0;
    }
}

//===========  displayNoneBlackPoint and set the BlackPoint
function setBlackPoint() {
    //  displayNoneBlackPoint
    let carouseBlackPoint = document.querySelectorAll(".carouselInturnshow");
    let length = carouseBlackPoint.length;
    for (let i = 0; i < length; i++) {
        carouseBlackPoint[i].style.display = "none";
    }
    //  set the position
    carouseBlackPoint[carousePosition].style.display = "block";
    imgBackground.setAttribute("src", imgBackgroundList[carousePosition]);
}

//===========   替每個白球設置監聽事件  ===========
function setListenerforEachCarouselInturn() {
    let CarouselInturnListener = document.getElementById(eachCarouselInturnID);
    CarouselInturnListener.onclick = function (event) {
        carousePosition = Number(event.target.id);
        setBlackPoint();
    };
}

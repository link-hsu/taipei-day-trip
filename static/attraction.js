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
// let Today = new Date();
// let dateIn = document.querySelector(".dateIn");
// todayModel =
//     String(Today.getFullYear()) +
//     "-" +
//     String(Today.getMonth() + 1) +
//     "-" +
//     String(Today.getDate());
// dateIn = document.querySelector(".dateIn");
// dateIn.value = todayModel;
// dateIn.min = todayModel;

// ====
// 获取当前日期
let Today = new Date();
// 获取年份、月份和日期并格式化为两位数字
let year = Today.getFullYear();
let month = (Today.getMonth() + 1).toString().padStart(2, "0");
let day = Today.getDate().toString().padStart(2, "0");
// 拼接成符合 "yyyy-MM-dd" 格式的日期字符串
let todayModel = `${year}-${month}-${day}`;

// 设置日期输入框的值和最小值
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

// ====== link to booking page
const orderBtn = document.querySelector(".orderBtn");
orderBtn.addEventListener(
    "click",
    function () {
        checkAttractionToken();
    },
    false
);

function checkAttractionToken() {
    if (localStorage.getItem("token")) {
        let url = "/api/user/auth";
        let token = localStorage.getItem("token");
        fetch(url, {
            method: "GET",
            headers: { authorization: `Bearer ${token}` },
        })
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                if (data["data"] === null) {
                    opensigninModal();
                } else {
                    bookingData = getDataForBooking();
                    postBookingDataToBackEnd(bookingData);
                }
            });
    } else {
        opensigninModal();
    }
}

function opensigninModal() {
    const filmBackground = document.querySelector(".filmBackground");
    const signinBlock = document.querySelector(".signinBlock");
    filmBackground.style.display = "flex";
    signinBlock.style.display = "block";
}

function getDataForBooking() {
    const attractionUrl = window.location.pathname;
    const attractionId = attractionUrl.replace("/attraction/", "");
    let attractionPrice = fee.textContent
        .replaceAll(" ", "")
        .replace("新台幣", "")
        .replace("元", "");
    let time = "";
    if (attractionPrice == "2000") {
        time = "morning";
    } else {
        time = "afternoon";
    }
    bookingData = {
        attractionId: attractionId,
        date: dateIn.value,
        price: attractionPrice,
        time: time,
    };
    return bookingData;
}

const orderMessage = document.querySelector(".orderMessage");
function postBookingDataToBackEnd(bookingData) {
    let token = localStorage.getItem("token");
    fetch("/api/booking", {
        method: "POST",
        body: JSON.stringify(bookingData),
        headers: {
            "content-type": "application/json",
            authorization: `Bearer ${token}`,
        },
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            if (data["ok"] == true) {
                orderMessage.style.display = "block";
                orderMessage.textContent = "資料填寫無誤";
                orderMessage.style.color = "green";
                orderBtn.style.marginTop = "10px";
                window.location.href = "/booking";
            } else {
                orderMessage.style.display = "block";
                orderMessage.style.color = "red";
                orderMessage.textContent = data["message"];
                orderBtn.style.marginTop = "10px";
            }
        });
}

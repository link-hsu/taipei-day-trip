let attractions_container = document.querySelector(".attractions_container");
let searchBtn = document.querySelector(".search_bar_button");
let searchInput = document.querySelector(".search_bar_input");
let leftArrow = document.querySelector(".search_list_left_arrow");
let rightArrow = document.querySelector(".search_list_right_arrow");
let container = document.querySelector(".container");

// 捲動捷運list
leftArrow.addEventListener("click", () => {
    container.scrollLeft -= container.clientWidth - 90;
});
rightArrow.addEventListener("click", () => {
    container.scrollLeft += container.clientWidth - 90;
});

let nextPage = 0;
let keyword = "";

const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting && nextPage != null) {
        getAttractionsData(nextPage, keyword);
        observer.unobserve(entries[0].target);
    } else if (nextPage == null) {
        observer.disconnect();
    }
});

// 捷運站清單按鈕
function searchMrt(btn) {
    searchInput.value = btn.textContent;
    searchBtn.click();
}

// 取得捷運列表
function getMrts() {
    fetch("/api/mrts")
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            for (let i = 0; i < data["data"].length; i++) {
                if (data["data"][i] != "None") {
                    let mrtButton = document.createElement("button");
                    mrtButton.className = "list_item";
                    mrtButton.setAttribute("onclick", "searchMrt(this)");
                    mrtButton.textContent = data["data"][i];
                    container.appendChild(mrtButton);
                }
            }
        })
        .catch(function (error) {
            alert(error["message"]);
        });
}

getMrts();

// 將取得的data渲染到畫面
function renderAttractions(api) {
    for (i = 0; i < api["data"].length; i++) {
        let attractionBoxDiv = document.createElement("div");
        attractionBoxDiv.className = "attraction_box";

        let attractionImg = document.createElement("img");
        attractionImg.setAttribute("src", api["data"][i]["images"][0]);

        let attractionNameDiv = document.createElement("div");
        attractionNameDiv.className = "attraction_name";
        attractionNameDiv.textContent = api["data"][i]["name"];

        let attractionDetailDiv = document.createElement("div");
        attractionDetailDiv.className = "attraction_detail";

        let mrtDiv = document.createElement("div");
        mrtDiv.textContent = api["data"][i]["mrt"];

        let catDiv = document.createElement("div");
        catDiv.textContent = api["data"][i]["category"];
        attractions_container.appendChild(attractionBoxDiv);

        let attractionBoxElem = document.querySelector(
            ".attractions_container"
        ).lastChild;

        attractionBoxElem.appendChild(attractionImg);
        attractionBoxElem.appendChild(attractionNameDiv);
        attractionBoxElem.appendChild(attractionDetailDiv);

        let attractionDetailElem = attractionBoxElem.lastChild;
        attractionDetailElem.appendChild(mrtDiv);
        attractionDetailElem.appendChild(catDiv);
    }
}
// 首先取得景點
function getAttractionsData(page, keyword) {
    fetch(
        `/api/attractions?page=${encodeURIComponent(
            page
        )}&keyword=${encodeURIComponent(keyword)}`
    )
        .then((response) => response.json())
        .then((data) => {
            nextPage = data["nextPage"];
            if (data["data"].length == 0) {
                attractions_container.textContent = "查無景點";
            } else {
                // render 及 滾動效果
                renderAttractions(data);
                observer.observe(
                    document.querySelector(".attractions_container").lastChild
                );
            }
        })
        .catch(function (error) {
            alert(error["message"]);
        });
}

// 點擊搜尋後效果
searchBtn.addEventListener("click", function (e) {
    e.preventDefault();
    keyword = searchInput.value;
    nextPage = 0;
    while (attractions_container.hasChildNodes()) {
        attractions_container.removeChild(attractions_container.lastChild);
    }
    getAttractionsData(nextPage, keyword);
});
getAttractionsData(nextPage, keyword);

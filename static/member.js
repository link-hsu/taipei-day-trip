// ====== auth_check
window.addEventListener("load", async function () {
    try {
        const islogin = await async_checkToken();
        if (islogin == false) {
            let url = "/";
            window.location.href = url;
        } else {
            console.log("/booking auth驗證成功");
        }
    } catch (error) {
        console.log("member.js loading error");
    }
});

const memberName = document.querySelector(".memberName");
const memberEmail = document.querySelector(".memberEmail");
const memberPassword = document.querySelector(".memberPassword");
const memberMessage = document.querySelector(".memberMessageTitle");

// ====== render current member information
function getMemberInformation() {
    let token = localStorage.getItem("token");
    fetch("/api/member", {
        method: "GET",
        headers: {
            "content-type": "application/json",
            authorization: `Bearer ${token}`,
        },
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            console.log("/api/member/get: ", data);
            key_in_member_information(data);
        });
}
function key_in_member_information(data) {
    memberName.value = data.name;
    memberEmail.value = data.email;
    memberPassword.value = data.password;
}

getMemberInformation();

// ====== change_member_inforamtion
const changeInformationBtn = document.querySelector(".changeInformationBtn");
changeInformationBtn.addEventListener("click", function () {
    let newMemberData = {
        name: memberName.value,
        email: memberEmail.value,
        password: memberPassword.value,
    };
    postNewMemberData(newMemberData);
});

function postNewMemberData(newMemberData) {
    let token = localStorage.getItem("token");
    console.log("/api/member/post: ", token);
    fetch("/api/member", {
        method: "POST",
        body: JSON.stringify(newMemberData),
        headers: {
            "content-type": "application/json",
            authorization: `Bearer ${token}`,
        },
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            console.log("api/member/post: ", data);
            if (data.error) {
                memberMessage.style.visibility = "visible";
                memberMessage.style.color = "red";
                memberMessage.textContent = data.message;
            } else {
                localStorage.removeItem("token");
                localStorage.setItem("token", data.token);
                memberMessage.style.visibility = "visible";
                memberMessage.style.color = "green";
                memberMessage.textContent = "更改成功";
            }
        });
}

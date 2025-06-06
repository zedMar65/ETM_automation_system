async function update_user_list() {
    const user_list = document.getElementById("user-list");
    const users = await query("users");  // Wait for fetch to complete
    user_list.innerHTML = "";

    for (let key in users) {
        const user = users[key];
        user_list.innerHTML += "<div class=\"user-row\">";
        user_list.innerHTML += user["id"] + " - ";
        user_list.innerHTML += user["name"] + " - ";
        user_list.innerHTML += user["email"] + " - ";
        user_list.innerHTML += user["auth"] + " | ";
        user_list.innerHTML += "<button onclick=\"remove_user(" + user["id"] + ")\">Delete</button>";
        user_list.innerHTML += "</div><br>";
    }
}

function query(type){
    return fetch("fetch-"+type, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: ""
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        response = response.json();
        return response;
    });
}

function remove_user(user_id){
    return fetch("remove-user", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: user_id
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        update_user_list();
    });
}   

document.getElementById("new-user").addEventListener("submit", (e) => {
    e.preventDefault();
    namee = document.getElementById("user-name").value
    mail = document.getElementById("user-email").value
    pass = document.getElementById("user-password").value
    auth = document.getElementById("user-auth").value
    jsonOBJ = {
        name: namee,
        email: mail,
        password: pass,
        auth: auth
    }
    console.log(JSON.stringify(jsonOBJ))
    sucess = fetch("new-user", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(jsonOBJ)
  })
  .then(response => {
    if (!response.ok) {
      return;
    }
      update_user_list()
  })
})

function new_user(data){
    return fetch("remove-user", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        update_user_list();
    });
}   

update_user_list()
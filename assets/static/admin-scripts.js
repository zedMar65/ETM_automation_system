async function update_user_list() {
    const user_list = document.getElementById("user-list");
    const users = await query("users");  // Wait for fetch to complete
    user_list.innerHTML = "";

    for (let key in users) {

        const user = users[key];
        const selectedAuth = user["auth"];

        user_list.innerHTML +=  `
<div class=\"row\">
<input type=\"text\" value=\"${user["id"]}\" disabled id=\"user-id-${user["id"]}\">
<input type=\"text\" value=\"${user["email"]}\" id=\"user-email-${user["id"]}\">
<input type=\"text\" value=\"${user["name"]}\" id=\"user-name-${user["id"]}\">
<select name="user-auth" id="user-auth-${user["id"]}">
<option value="admin" ${selectedAuth === "admin" ? "selected" : ""}>Admin</option>
<option value="mod" ${selectedAuth === "mod" ? "selected" : ""}>Mod</option>
<option value="guide" ${selectedAuth === "guide" ? "selected" : ""}>Guide</option>
</select>
<button onclick=\"mod_user('${user["id"]}')\">Set</button>
<button onclick=\"remove_user('${user["id"]}')\">Delete</button>
</div><br>`;
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
    fetch("/remove-user", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ user_id })
})
.then(response => {
    if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
    }
    update_user_list();
})
.catch(error => {
    console.error("Failed to delete user:", error);
});
}   

function mod_user(user_id){
  let user_name = document.getElementById("user-name-"+user_id).value
  let user_email = document.getElementById("user-email-"+user_id).value
  let user_auth = document.getElementById("user-auth-"+user_id).value
  
fetch("/mod-user", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ user_id, user_name, user_email, user_auth })
})
.then(response => {
    if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
    }
    update_user_list();
})
.catch(error => {
    console.error("Failed to delete user:", error);
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

update_user_list()
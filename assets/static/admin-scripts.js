async function update_user_list() {
    const user_list = document.getElementById("user-list");
    const users = await query("users");  // Wait for fetch to complete
    user_list.innerHTML = "";

    for (let key in users) {

        const user = users[key];
        const selectedAuth = user["auth"];

        user_list.innerHTML +=  `
<div class=\"row\">
<input class="id" type=\"text\" value=\"${user["id"]}\" disabled id=\"user-id-${user["id"]}\">
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

// ----------------------------

async function update_event_list() {
    const event_list = document.getElementById("event-list");
    const events = await query("events");  // Wait for fetch to complete
    event_list.innerHTML = "";

    for (let key in events) {

        const event = events[key];

        event_list.innerHTML +=  `
<div class=\"row\">
<input class="id" type=\"text\" value=\"${event["id"]}\" disabled id=\"event-id-${event["id"]}\">
<input type=\"text\" value=\"${event["name"]}\" id=\"event-name-${event["id"]}\">
<button onclick=\"mod_event('${event["id"]}')\">Set</button>
<button onclick=\"remove_event('${event["id"]}')\">Delete</button>
</div><br>`;
    }
}

function remove_event(event_id){
    fetch("/remove-event", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ event_id })
})
.then(response => {
    if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
    }
    update_event_list();
})
.catch(error => {
    console.error("Failed to delete event:", error);
});
}   

function mod_event(event_id){
  let event_name = document.getElementById("event-name-"+event_id).value
  
fetch("/mod-event", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ event_id, event_name })
})
.then(response => {
    if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
    }
    update_event_list();
})
.catch(error => {
    console.error("Failed to delete event:", error);
});
}

document.getElementById("new-event").addEventListener("submit", (e) => {
    e.preventDefault();
    namee = document.getElementById("event-name").value
    jsonOBJ = {
        name: namee,
    }
    console.log(JSON.stringify(jsonOBJ))
    sucess = fetch("new-event", {
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
      update_event_list()
  })
})

// --------------

async function update_room_list() {
    const room_list = document.getElementById("room-list");
    const rooms = await query("rooms");  // Wait for fetch to complete
    room_list.innerHTML = "";

    for (let key in rooms) {

        const room = rooms[key];
        room_list.innerHTML +=  `
<div class=\"row\">
<input class="id" type=\"text\" value=\"${room["id"]}\" disabled id=\"room-id-${room["id"]}\">
<input type=\"text\" value=\"${room["name"]}\" id=\"room-name-${room["id"]}\">
<input class="num" type="number" value="${room["capacity"]}" id="room-capacity-${room["id"]}">
<button onclick=\"mod_room('${room["id"]}')\">Set</button>
<button onclick=\"remove_room('${room["id"]}')\">Delete</button>
</div><br>`;
    }
}

function remove_room(room_id){
    fetch("/remove-room", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ room_id })
})
.then(response => {
    if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
    }
    update_room_list();
})
.catch(error => {
    console.error("Failed to delete room:", error);
});
}   

function mod_room(room_id){
  let room_name = document.getElementById("room-name-"+room_id).value
  
fetch("/mod-room", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ room_id, room_name })
})
.then(response => {
    if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
    }
    update_room_list();
})
.catch(error => {
    console.error("Failed to delete room:", error);
});
}

document.getElementById("new-room").addroomListener("submit", (e) => {
    e.prroomDefault();
    namee = document.getElementById("room-name").value
    jsonOBJ = {
        name: namee,
    }
    console.log(JSON.stringify(jsonOBJ))
    sucess = fetch("new-room", {
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
      update_room_list()
  })
})

update_room_list()
update_event_list()
update_user_list()
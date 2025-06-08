async function update_user_list() {
    const user_list = document.getElementById("user-list");
    const users = await query("user");  // Wait for fetch to complete
    user_list.innerHTML = "";
    let list = document.getElementById("event-guide-guide-name")
    list.innerHTML = "";
    let list2 = document.getElementById("guide-hour-name")
    list2.innerHTML = "";
    for (let key in users) {
        
        const user = users[key];
        const selectedAuth = user["auth"];
        if (user["auth"] == "guide"){
          list.innerHTML += "<option value=\""+user["name"]+"\">"+user["name"]+"</option>"
          list2.innerHTML += "<option value=\""+user["name"]+"\">"+user["name"]+"</option>"
        }

        user_list.innerHTML +=  `
<div class=\"row\">
<input class="num" type=\"text\" value=\"${user["id"]}\" disabled id=\"user-id-${user["id"]}\">
<input type=\"text\" value=\"${user["email"]}\" id=\"user-email-${user["id"]}\">
<input type=\"text\" value=\"${user["name"]}\" id=\"user-name-${user["id"]}\">
<select name="user-auth" id="user-auth-${user["id"]}">
<option value="admin" ${selectedAuth === "admin" ? "selected" : ""}>Admin</option>
<option value="mod" ${selectedAuth === "mod" ? "selected" : ""}>Mod</option>
<option value="guide" ${selectedAuth === "guide" ? "selected" : ""}>Guide</option>
</select>
<button onclick=\"mod('${user["id"]}', 'user')\">Set</button>
<button onclick=\"remove('${user["id"]}', 'user')\">Delete</button>
</div>`;
    }
}

async function update_room_list() {
    const room_list = document.getElementById("room-list");
    const rooms = await query("room");  // Wait for fetch to complete
    room_list.innerHTML = "";
    let list = document.getElementById("event-room-room-name")
    list.innerHTML = "";
        
    for (let key in rooms) {

        const room = rooms[key];

        list.innerHTML += "<option value=\""+room["name"]+"\">"+room["name"]+"</option>"
        room_list.innerHTML +=  `
<div class=\"row\">
<input class="num" type=\"text\" value=\"${room["id"]}\" disabled id=\"room-id-${room["id"]}\">
<input type=\"text\" value=\"${room["name"]}\" id=\"room-name-${room["id"]}\">
<input class="num" type="number" value="${room["capacity"]}" id="room-capacity-${room["id"]}">
<button onclick=\"mod('${room["id"]}', 'room')\">Set</button>
<button onclick=\"remove('${room["id"]}', 'room')\">Delete</button>
</div>`;
    }
}  

async function update_event_list() {
    const event_list = document.getElementById("event-list");
    const events = await query("event");  // Wait for fetch to complete
    event_list.innerHTML = "";
    let list1 = document.getElementById("event-room-event-name")
    list1.innerHTML = "";
    let list2 = document.getElementById("event-guide-event-name")
    list2.innerHTML = "";
    for (let key in events) {

        const event = events[key];
        list1.innerHTML += "<option value=\""+event["name"]+"\">"+event["name"]+"</option>"
        list2.innerHTML += "<option value=\""+event["name"]+"\">"+event["name"]+"</option>"
        event_list.innerHTML +=  `
<div class=\"row\">
<input class="num" type=\"text\" value=\"${event["id"]}\" disabled id=\"event-id-${event["id"]}\">
<input type=\"text\" value=\"${event["name"]}\" id=\"event-name-${event["id"]}\">
<input class="num" type=\"number\" value=\"${event["duration"]}\" id=\"event-duration-${event["id"]}\">
<button onclick=\"mod('${event["id"]}', 'event')\">Set</button>
<button onclick=\"remove('${event["id"]}', 'event')\">Delete</button>
</div>`;
    }
}

async function update_guide_hour_list() {
    const guide_hour_list = document.getElementById("guide-hour-list");
    const guide_hours = await query("guide-hour");  // Wait for fetch to complete
    guide_hour_list.innerHTML = "";
    for (let key in guide_hours) {

        const guide_hour = guide_hours[key];
        guide_hour_list.innerHTML +=  `
<div class=\"row\">
<input class="num" type=\"text\" value=\"${guide_hour["id"]}\" disabled id=\"guide-hour-id-${guide_hour["id"]}\">
<input disabled locked type=\"text\" value=\"${guide_hour["name"]}\" id=\"guide-hour-name-${guide_hour["id"]}\">
<select name="guide-hour-day" value="${guide_hour["day"]}" id="guide-hour-day-${guide_hour["id"]}">
            <option ${guide_hour["day"] === 1 ? "selected" : ""} value="1">Monday</option>
            <option ${guide_hour["day"] === 2 ? "selected" : ""} value="2">Tuesday</option>
            <option ${guide_hour["day"] === 3 ? "selected" : ""} value="3">Wendsday</option>
            <option ${guide_hour["day"] === 4 ? "selected" : ""} value="4">Thursday</option>
            <option ${guide_hour["day"] === 5 ? "selected" : ""} value="5">Friday</option>
            <option ${guide_hour["day"] === 6 ? "selected" : ""} value="6">Saturnday</option>
            <option ${guide_hour["day"] === 7 ? "selected" : ""} value="7">Sunday</option>
        </select>
<input class="num" type="number" value="${guide_hour["start-hour"]}" id="guide-hour-start-${guide_hour["id"]}">
<input class="num" type="number" value="${guide_hour["end-hour"]}" id="guide-hour-end-${guide_hour["id"]}">
<button onclick=\"mod('${guide_hour["id"]}', 'guide-hour')\">Set</button>
<button onclick=\"remove('${guide_hour["id"]}', 'guide-hour')\">Delete</button>
</div>`;
    }
}

async function update_even_room_list() {
    const event_list = document.getElementById("event-room-list");
    const events = await query("event-room");  // Wait for fetch to complete
    event_list.innerHTML = "";

    for (let key in events) {

        const event = events[key];

        event_list.innerHTML +=  `
<div class=\"row\">
<input class="num" type=\"text\" value=\"${event["id"]}\" disabled id=\"event-room-id-${event["id"]}\">
<input disabled type=\"text\" value=\"${event["event-name"]}\" id=\"event-room-event-name-${event["id"]}\">
<input disabled type=\"text\" value=\"${event["room-name"]}\" id=\"event-room-room-name-${event["id"]}\">
<button onclick=\"remove('${[event["event-name"], event["room-name"]]}', 'event-room')\">Delete</button>
</div>`;
    }
}

async function update_event_guide_list() {
    const event_list = document.getElementById("event-guide-list");
    const events = await query("event-guide");  // Wait for fetch to complete
    event_list.innerHTML = "";

    for (let key in events) {

        const event = events[key];

        event_list.innerHTML +=  `
<div class=\"row\">
<input class="num" type=\"text\" value=\"${event["id"]}\" disabled id=\"event-guide-id-${event["id"]}\">
<input disabled type=\"text\" value=\"${event["event-name"]}\" id=\"event-guide-event-name-${event["id"]}\">
<input disabled type=\"text\" value=\"${event["guide-name"]}\" id=\"event-guide-guide-name-${event["id"]}\">
<button onclick=\"remove('${[event["event-name"], event["guide-name"]]}', 'event-guide')\">Delete</button>
</div>`;
    }
}

async function update_all(){
  await update_event_list()
  await update_room_list()
  await update_user_list()
  await update_even_room_list()
  await update_event_guide_list()
  await update_guide_hour_list()
}

function query(type){
    return fetch("/fetch", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ option: type })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        response = response.json();
        return response;
    });
}

function remove(id, option){
    fetch("/remove", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ id, option })
})
.then(response => {
    if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
    }
    update_all();
})
.catch(error => {
    console.error("Failed to delete room:", error);
});
} 

function cnew(option){
  let jsonOBJ = {};
  if (option == "user"){
    let namee = document.getElementById("user-name").value
    let mail = document.getElementById("user-email").value
    let pass = document.getElementById("user-password").value
    let auth = document.getElementById("user-auth").value
    jsonOBJ = {
        option: option,
        name: namee,
        email: mail,
        password: pass,
        auth: auth
    };
  } else if (option == "event"){
    let namee = document.getElementById("event-name").value
    let namee1 = document.getElementById("event-duration").value
    jsonOBJ = {
      option: option,
      name: namee,
      duration: namee1 
    };
  } else if (option == "room"){
    let namee = document.getElementById("room-name").value
    let namee1 = document.getElementById("room-capacity").value
    jsonOBJ = {
        option: option,
        name: namee,
        capacity: namee1
      };
  }else if (option == "event-room"){
    let namee = document.getElementById("event-room-event-name").value
    let namee1 = document.getElementById("event-room-room-name").value
    jsonOBJ = {
        option: option,
        "event-name": namee,
        "room-name": namee1
      };
  }else if (option == "event-guide"){
    let namee = document.getElementById("event-guide-event-name").value
    let namee1 = document.getElementById("event-guide-guide-name").value
    jsonOBJ = {
        option: option,
        "event-name": namee,
        "guide-name": namee1
      };
  }else if (option == "guide-hour"){
    let namee = document.getElementById("guide-hour-name").value
    let namee1 = document.getElementById("guide-hour-day").value
    let namee2 = document.getElementById("guide-hour-start").value
    let namee3 = document.getElementById("guide-hour-end").value
    jsonOBJ = {
        option: option,
        "name": namee,
        "day": namee1,
        "start-time": namee2,
        "end-time": namee3
      };
  }else{
    return
  }

    fetch("/new", {
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
    update_all()
  })

}

function mod(id, option){
  let jsonOBJ;
  if (option == "user"){
    jsonOBJ = {
      option: option,
      id: id,
      name: document.getElementById("user-name-"+id).value,
      email: document.getElementById("user-email-"+id).value,
      auth: document.getElementById("user-auth-"+id).value
    };
  }
  else if (option == "event"){
    jsonOBJ = {
      option: option,
      id: id,
      name: document.getElementById("event-name-"+id).value,
      duration: document.getElementById("event-duration-"+id).value
    };
  }
  else if (option == "room"){
    jsonOBJ = {
      option: option,
      id: id,
      name: document.getElementById("room-name-"+id).value,
      capacity: document.getElementById("room-capacity-"+id).value,
    };
  }else if (option == "guide-hour"){
    jsonOBJ = {
      option: option,
      id: id,
      day: document.getElementById("guide-hour-day-"+id).value,
      "start-hour": document.getElementById("guide-hour-start-"+id).value,
      "end-hour": document.getElementById("guide-hour-end-"+id).value
    };
  }else{
    return
  }
fetch("/mod", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(jsonOBJ)
})
.then(response => {
    if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
    }
    update_user_list();
})
.catch(error => {
    console.error("Failed to Mod:", error);
});
}

update_all()
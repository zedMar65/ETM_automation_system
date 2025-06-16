async function update_user_list() {
    const user_list = document.getElementById("user-list");
    const users = await query("user");  // Wait for fetch to complete
    user_list.innerHTML = "";
    let list = document.getElementById("event-guide-guide-name")
    list.innerHTML = "";
    let list2 = document.getElementById("guide-hour-name")
    list2.innerHTML = "";
    // let list3 = document.getElementById("callender-guide-name")
    // list3.innerHTML = "<option value=\"-\">-</option>";
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
    let list3 = document.getElementById("callendar-event-list")
    list3.innerHTML = "<div class=\"row_flex\"><input type=\"checkbox\" checked=\"true\" id=\"check_all\" onclick=\"check_all()\"><div class=\"alligned_name\">Check all</div></div>";
    for (let key in events) {

        const event = events[key];
        list1.innerHTML += "<option value=\""+event["name"]+"\">"+event["name"]+"</option>"
        list2.innerHTML += "<option value=\""+event["name"]+"\">"+event["name"]+"</option>"
        list3.innerHTML += "<div class=\"row_flex\"><input type=\"checkbox\" checked=\"true\" id=\""+event["id"]+"\"><div class=\"alligned_name\">"+event["name"]+"</div></div>"
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
<input type="time" class="time" value="${guide_hour["start-hour"]}" id="guide-hour-start-${guide_hour["id"]}">
<input type="time" class="time" value="${guide_hour["end-hour"]}" id="guide-hour-end-${guide_hour["id"]}">
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
    // console.log(events);
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

function full_update(){
  fetch("/full_update", {
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
    update_all();
})
.catch(error => {
    console.error("Failed to full_update:", error);
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

function check_all(){
  let children = document.getElementById("callendar-event-list").children;
  if (document.getElementById("check_all").checked){
    for (let i = 0; i < children.length; i++) {
      children[i].children[0].checked = true;
    }
  }else{
    for (let i = 0; i < children.length; i++) {
      children[i].children[0].checked = false;
    }
  }
  
}

async function calendar_filter(dateStr) {
  let selected_Events = [];

  let timeStart = document.getElementById("calendar-start-time").value;
  let timeEnd = document.getElementById("calendar-end-time").value;

  let children = document.getElementById("callendar-event-list").children;

  for (let i = 0; i < children.length; i++) {
    if (children[i].children[0].checked) {
      selected_Events.push(children[i].children[0].id);
    }
  }

  const jsonOBJ = {
    date: dateStr,
    time: [timeStart, timeEnd],
    events: selected_Events
  };

  try {
    const response = await fetch("/filter", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(jsonOBJ)
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();
    await update_callender(data);

  } catch (error) {
    console.error("Failed to Mod:", error);
    let times = document.getElementById("hours");
    times.innerHTML = "";
    times = document.getElementById("times")
    times.innerHTML = "";
  }
}

async function update_callender(data) {
  let min=2400
  let max= 0
  for (let key in data) {
    for (let key1 in data[key]){
      if (parseInt(data[key][key1]["start"].slice(8)) < min){
        min = parseInt(data[key][key1]["start"].slice(8));
      }
      if (parseInt(data[key][key1]["full_end"].slice(8)) > max){
        max = parseInt(data[key][key1]["full_end"].slice(8));
      }
    }
  }

  min = parseInt(min.toString().slice(0, 2))-Math.ceil(parseInt(min.toString().slice(2))/60)
  max = parseInt(max.toString().slice(0, 2))+Math.ceil(parseInt(max.toString().slice(2))/60)
  let times = document.getElementById("hours");
  times.innerHTML = "";
  for(let i = min; i <= max; i++){
    times.innerHTML+=`
    <div class="hour" id="hour-${i}">${i}:00</div>
    `
  }
  times = document.getElementById("times")
  times.innerHTML = "";
  for (let key in data) {
    let event_div = "";
    event_div += "<div class=\"cal_event\">"
    event_div += "<h4>"+key+"</h4>"
    event_div += "<div class=\"small_event\">"
    for (let i = 0; i < data[key].length; i++){
      let event_duration = data[key][i]["length"];
      let start = data[key][i]["start"].slice(8);
      let end = data[key][i]["end"].slice(8);
      start = parseInt(start.slice(0, 2)*60)+parseInt(start.slice(2))
      // console.log(parseInt(end.slice(2)))
      event_duration = parseInt(event_duration.slice(0, 2)*60)+parseInt(event_duration.slice(2))
      end = parseInt((parseInt(end.slice(0, 2))+1)*60)+parseInt(end.slice(2))-60
      // console.log(end)
      event_div += "<div class=\"hour_event\" onclick=\"form('"+data[key][i]["start"]+"', '"+data[key][i]["length"]+"', '"+key+"', '"+data[key][i]["end"]+"')\" style=\"width:"+100/(60*(max-min+1))*(end-start)+"%;left:" + 100/(60*(max-min+1))*(start-(60*min))  + "%;\"></div> <div class=\"hour_end\" style=\"width:"+100/(60*(max-min+1))*(event_duration)+"%;left:" + 100/(60*(max-min+1))*(end-(60*min))  + "%;\"></div>";
    }
    event_div += "</div>";
    event_div += "</div>";
    times.innerHTML += event_div;
  }
   
}

function form(start, duration, event_name, end){
  let form = document.getElementById("add_form")
  form.style.display = "block";

    // Temporarily show form offscreen to measure width
    form.style.left = "-9999px";
    form.style.top = "0px"; // Safe temp spot
    form.style.display = "block";

    const formWidth = form.offsetWidth;

    const pageWidth = window.innerWidth;

    // Calculate adjusted position
    let posX = mousePos.x;
    let posY = mousePos.y-50;

    // If the form would go off the right edge, move it left
    if (posX + formWidth > pageWidth) {
      posX = pageWidth - formWidth - 10; // Add small padding
    }

    

    // Apply adjusted position
    form.style.left = `${Math.max(10, posX)}px`; // Ensure it's not too far left
    form.style.top = `${Math.max(10, posY)}px`;
    document.getElementById("form_event_name").value = event_name
    document.getElementById("form_event_duration").value = duration.slice(0, 2)+":"+duration.slice(2)
    document.getElementById("form_start_time").value = start.slice(8, 10)+":"+start.slice(10);
    let end_time = parseInt(start.slice(10))+parseInt(duration.slice(2));
    let hour = 0;
    while(end_time >= 60){
      end_time -= 60;
      hour += 1;
    }
    end_time = (hour+parseInt(duration.slice(0, 2))+parseInt(start.slice(8, 10))).toString()+":"+end_time.toString();
    document.getElementById("form_end_time").value = end_time;
    document.getElementById("form_start_time").min = start.slice(8, 10)+":"+start.slice(10);
    document.getElementById("form_start_time").max = end.slice(8, 10)+":"+end.slice(10);
    document.getElementById("form_book").onclick = () => form_book(start);
  return;
}

function form_cancel(){
  let form = document.getElementById("add_form")
  form.style.display = "None";
}

let mousePos = { x: 0, y: 0 };

  // Track mouse position globally
document.addEventListener("mousemove", function(e) {
  mousePos.x = e.pageX;
  mousePos.y = e.pageY;
});

const input = document.getElementById("form_start_time");

input.addEventListener("input", () => {
  const time = input.value;
  if (time < input.min) {
    input.value = input.min;
  }else if(time > input.max){
    input.value = input.max
  } else {
    input.setCustomValidity("");
  }
  let end_time = parseInt(input.value.slice(3))+parseInt(document.getElementById("form_event_duration").value.slice(3));
  let hour = parseInt(input.value.slice(0, 2))+parseInt(document.getElementById("form_event_duration").value.slice(0, 2));
  while(end_time >= 60){
    end_time -= 60;
    hour += 1;
  }
  if(end_time.toString().length < 2){
    end_time = "0"+end_time.toString()
  }else{
    end_time = end_time.toString()
  }
  end_time = hour.toString()+":"+end_time;
  console.log(end_time);
  document.getElementById("form_end_time").value = end_time;

});

function form_book(date){
  let time = document.getElementById("form_start_time").value
  let event = document.getElementById("form_event_name").value
  let info = document.getElementById("form_info").value
  fetch("/book", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ 
    event, 
    time,
    date,
    info
  })
  })
  .then(response => {
      if (!response.ok) {
          throw new Error(`Server error: ${response.status}`);
      }
      update_all();
  })
  .catch(error => {
    console.error("Failed to book event:", error);
  });
}

update_all()
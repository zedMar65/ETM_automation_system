function toDatetimeLocal(date) {
        const utc3Date = new Date(date.getTime() );

        const year = utc3Date.getFullYear();
        const month = String(utc3Date.getMonth() + 1).padStart(2, '0');
        const day = String(utc3Date.getDate()).padStart(2, '0');
        const hours = String(utc3Date.getHours()).padStart(2, '0');
        const minutes = String(utc3Date.getMinutes()).padStart(2, '0');

        return `${year}-${month}-${day}T${hours}:${minutes}`;
    }


const now = new Date();
const time1Value = toDatetimeLocal(now);
const time1 = document.getElementById("time1");
time1.min = time1Value;
time1.placeholder = time1Value;
time1.value = time1Value;
// Create a date object for 1 day after time1's value
const oneDayLater = new Date(now.getTime() + 24 * 60 * 60 * 1000); // +1 day
const time2Value = toDatetimeLocal(oneDayLater);
const time2 = document.getElementById("time2");
time2.min = time1.value;
time2.placeholder = time2Value;
time2.value = time2Value;


// filter form handeling:
let time_frames = [];
let selected_events = [];
let selected_guides = [];
let selected_rooms = [];
let free_times = true
const form = document.getElementById("selection-form");
const saveDraftBtn = document.getElementById("saveDraft");
const realSubmitBtn = document.getElementById("submit-filter");
const selectedTimes = document.getElementById("selected-times");
var full_available_events = []


function inquiry(option) {
  const jsonObject = {
    option: option,
    free_time: free_times,
    time_frame: time_frames,
    guide: selected_guides,
    event: selected_events,
    room: selected_rooms
  };

  return fetch("filter", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(jsonObject)
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }
    response = response.json();
    // should refresh the available selections of form elements
    return response; // <- parses the returned JSON
  });
}



saveDraftBtn.addEventListener("click", () => {
  const time1 = document.getElementById("time1").value;
  const time2 = document.getElementById("time2").value;
  let id =  time_frames.length; 
  time_frames.push({
    startTime: time1,
    endTime: time2,
    id: id
  });

  selectedTimes.innerHTML += "<div class=\"selected-time-option\" id=\"selected-time-"+id+"\" onclick=\"remove_time("+id+")\">"+time1+"-"+time2+"</div>";

});

form.addEventListener("submit", (e) => {
    e.preventDefault();
    inquiry("no-reserve")
});

function remove_time(id){
        for(var i = 0; i < time_frames.length; i++){
            if (time_frames[i]["id"] == id){
                time_frames.splice(i, 1);
                break;
            }
        }
        document.getElementById("selected-time-"+id).remove();
}

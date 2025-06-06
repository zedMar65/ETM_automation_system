const form = document.getElementById("login-form")

form.addEventListener("submit", (e) => {
    e.preventDefault();
    pass = document.getElementById("password").value
    mail = document.getElementById("email").value
    jsonOBJ = {
        password: pass,
        email: mail
    }
    sucess = fetch("login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(jsonOBJ)
  })
  .then(response => {
    if (!response.ok) {
      document.getElementById("Error").innerHTML = "<p>Either email or password are incorrect</p>"
      return;
    }
      window.location.href = "/";
  })
})
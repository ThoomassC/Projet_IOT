const options = {methods: 'GET'};

fetch('http://localhost:5000/front/data/', options)
    .then(response => console.log(response.json()))
    .then(response =>
  document.write(`
 <html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="Style.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.3/dist/Chart.min.js"></script>
    <title>Station Météo</title>
  </head>
  <body class="nuage">
    <table>
        <thead>
          <tr>
            <th>Heure et date</th>
            <th>Température</th>
            <th>Pression</th>
            <th>Humidité</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>${response[0]['Date']}</td>
            <td>${response.temperature}</td>
            <td>${response.pressure}</td>
            <td>${response.humidity}</td>
          </tr>
        </tbody>
    </table>
    <div class="text-center">
        <br></br>
        <h1>Projet iOT</h1>
        <br></br>
        <div class="d-flex justify-content-center">
            <div class="btn-group" role="group">
            <a href="https://www.facebook.com/" target="_blank"><button type="button" class="btn btn-secondary">Partager sur Facebook</button></a>
            <a href="mailto:thomas.caron@viacesi.fr" target="_blank"><button type="button" class="btn btn-secondary">Partager via Mail</button></a>
            <button type="button" class="btn btn-secondary">Partager sur LinkedIn</button>
            </div>
        </div>
        <br></br>
    </div>
    
    <div id="myCarousel" class="carousel slide" data-ride="carousel">
      <ol class="carousel-indicators">
        <li data-target="#myCarousel" data-slide-to="0" class="active"></li>
        <li data-target="#myCarousel" data-slide-to="1"></li>
        <li data-target="#myCarousel" data-slide-to="2"></li>
      </ol>
      <div class="carousel-inner">
        <div class="carousel-item active">
          <canvas id="temperatureChart"></canvas>
        </div>
        <div class="carousel-item">
          <canvas id="humidityChart"></canvas>
        </div>
        <div class="carousel-item">
          <canvas id="pressureChart"></canvas>
        </div>
      </div>
      <a class="carousel-control-prev" href="#myCarousel" role="button" data-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="sr-only">Previous</span>
      </a>
      <a class="carousel-control-next" href="#myCarousel" role="button" data-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="sr-only">Next</span>
      </a>
      </div>
      {
      var temperatureData = {
        labels: ["January", "February", "March", "April", "May", "June", "July"],
        datasets: [{
            label: "Temperature (°C)",
            data: [response.datas.map(element => {
                element.temperature
            })],
            backgroundColor: "transparent",
            borderColor: "#ff5733",
            borderWidth: 2
            }]
        };

      var humidityData = {
        labels: ["January", "February", "March", "April", "May", "June", "July"],
        datasets: [{
            label: "Humidity (%)",
            data: [response.datas.map(element => {
                element.humidity
            })],
            backgroundColor: "transparent",
            borderColor: "#1e90ff",
            borderWidth: 2
          }]
        };

      var pressureData = {
        labels: ["January", "February", "March", "April", "May", "June", "July"],
        datasets: [
          {
            label: "Pressure (hPa)",
            data: [response.datas.map(element => {
                element.pressure
            })],
            backgroundColor: "transparent",
            borderColor: "#228b22",
            borderWidth: 2
          }
        ]
      };

      var options = {
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true
              }
            }
          ]
        }
      };

      var temperatureChart = new Chart(document.getElementById("temperatureChart"), {
        type: "line",
        data: temperatureData,
        options: options
      });

      var humidityChart = new Chart(document.getElementById("humidityChart"), {
        type: "line",
        data: humidityData,
        options: options
      });

      var pressureChart = new Chart(document.getElementById("pressureChart"), {
        type: "line",
        data: pressureData,
        options: options
      });
     }
  </body>
</html>
`))
    .catch(function (error) {
  console.error(error);
});


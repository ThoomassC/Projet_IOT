const FetchData = async() => {
    const routeData = await fetch('http://localhost:5000/front/data/')
    const newRouteData = await routeData.json()
    return newRouteData;
}

const FetchDatas = async() => {
    const routeDatas = await fetch('http://localhost:5000/front/datas/')
    const newRouteDatas = await routeDatas.json()
    return newRouteDatas;
}

class Chart { render(){

`<script type="text/javascript" src="Script.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.3/dist/Chart.min.js"></script>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
`
}
}

(async ()=> {
    const data = await FetchData();
    var tbody = document.getElementById('tbody')
    for (var i = 0; i < data.length ; i++){var row =`
        <tr>
            <td>${data[0]['date']}</td>
            <td>${data[0]['temperature']}</td>
            <td>${data[0]['pressure']}</td>
            <td>${data[0]['humidity']}</td>
        </tr>
    `} tbody.innerHTML += row
})()


            (async ()=> {
    const data = await FetchDatas();
                {`<script type="text/javascript" src="Script.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.3/dist/Chart.min.js"></script>`}
      var temperatureData = {
        labels: ["January", "February", "March", "April", "May", "June", "July"],
        datasets: [{
            label: "Temperature (°C)",
            data: [20, 25, 30, 35, 40, 35, 30],
            backgroundColor: "transparent",
            borderColor: "#ff5733",
            borderWidth: 2
            }]
        };

      var humidityData = {
        labels: ["January", "February", "March", "April", "May", "June", "July"],
        datasets: [{
            label: "Humidity (%)",
            data: [60, 65, 70, 75, 80, 75, 70],
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
            data: [1013, 1015, 1017, 1019, 1021, 1019, 1017],
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
    for (var i = 0; i < data.length ; i++){var row =`
        <tr>
            <td>${data[0]['date']}</td>
            <td>${data[0]['temperature']}</td>
            <td>${data[0]['pressure']}</td>
            <td>${data[0]['humidity']}</td>
        </tr>
    `} pressureChart.innerHTML += row, humidityChart.innerHTML += row, temperatureChart.innerHTML += row
})()




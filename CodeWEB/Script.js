const FetchData = async() => {
    const routeData = await fetch('http://localhost:5000/front/data/') // 192.168.137.164
    const newRouteData = await routeData.json()
    return newRouteData;
}

const FetchDatas = async() => {
    const routeDatas = await fetch('http://localhost:5000/front/datas/')
    const newRouteDatas = await routeDatas.json()
    return newRouteDatas;
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


const Graphs = (async() => {
    const datas = await FetchDatas();
      var temperatureData = {
        labels: datas.map(element => element['date']).reverse(),
        datasets: [{
            label: "Temperature (°C)",
            data: datas.map(element => element['temperature']).reverse(),
            backgroundColor: "transparent",
            borderColor: "#ff5733",
            borderWidth: 2
            }]
        };

      var humidityData = {
        labels: datas.map(element => element['date']).reverse(),
        datasets: [{
            label: "Humidity (%)",
            data: datas.map(element => element['humidity']).reverse(),
            backgroundColor: "transparent",
            borderColor: "#1e90ff",
            borderWidth: 2
          }]
        };

      var pressureData = {
        labels: datas.map(element => element['date']).reverse(),
        datasets: [
          {
            label: "Pressure (hPa)",
            data: datas.map(element => element['pressure']).reverse(),
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
     pressureChart.innerHTML, humidityChart.innerHTML, temperatureChart.innerHTML
})()




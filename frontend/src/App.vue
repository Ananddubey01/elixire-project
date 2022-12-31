<template>
  <div class="container">
    <SearchPage @searchParams="searchParams" />
  </div>
</template>

<script setup>
import SearchPage from "./SearchPage.vue";
import axios from "axios";

function searchParams(searchParams) {
  getID(searchParams.url, searchParams.queryType);
}
function getID(URL, queryType) {
  var data = JSON.stringify({
    url: URL,
  });

  var config = {
    method: "post",
    url: "http://127.0.0.1:5000/" + queryType,
    headers: {
      "Content-Type": "application/json",
    },
    data: data,
  };
  axios(config)
    .then(function (response) {
      getCSV(URL, queryType, response.data.data);
    })
    .catch(function (error) {
      console.log(error);
    });
}
function getCSV(URL, queryType, CSVID) {
  var data = JSON.stringify({
    url: URL,
  });

  var config = {
    method: "get",
    url: "http://127.0.0.1:5000/" + queryType + "/" + CSVID,
    headers: {
      "Content-Type": "application/json",
    },
    data: data,
  };
  axios(config)
    .then(function (response) {
      console.log(typeof(response.data));
      var csvFileData=response.data;
      download_csv_file(csvFileData);
    })
    .catch(function (error) {
      console.log(error);
    });
}
function download_csv_file(csvFileData) {
  var csv = csvFileData;
  //merge the data with CSV
  // csvFileData.forEach(function (row) {
  //   csv += row.join(",");
  //   csv += "\n";
  // });

  //display the created CSV data on the web browser
  //document.write(csv);

  var hiddenElement = document.createElement("a");
  hiddenElement.href = "data:text/csv;charset=utf-8," + encodeURI(csv);
  hiddenElement.target = "_blank";

  //provide the name for the CSV file to be downloaded
  hiddenElement.download = "File.csv";
  hiddenElement.click();
  alert("file downloaded!")
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>

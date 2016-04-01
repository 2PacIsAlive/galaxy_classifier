var Firebase  = require("firebase");
var firebase = new Firebase("https://galaxy-classifier.firebaseio.com/");

var err = firebase.child("error")

var data = [];

function compare(a,b) {
    if (a["n"] < b["n"])
        return -1;
    else if (a["n"] > b["n"])
        return 1;
    else 
        return 0 
};

function renderLiveGraph() {
    var mainGraph;
    err.on("value", function(snapshot) {
        data = snapshot.val();
    });
    mainGraph = Morris.Area({
        element: 'main-graph',
        data: data.sort(compare),
        xkey: 'epoch',
        ykeys: ['err'],
        lineColors: ['red'],
        labels: ['Error'],
        pointSize: 0,
        resize: true,
        parseTime: false,
        pointFillColors:['#ffffff'],
        pointStrokeColors: ['black'],
        behaveLikeLine: true,
        fillOpacity: 0.6,
        hideHover: 'auto' 
        });
    config.element = "curr_err";
    Morris.Line(config);
    setInterval(function() { updateLiveGraph(mainGraph); }, 20000);
}

function updateLiveGraph(mainGraph) {
    err.on("value", function(snapshot) {
        data = snapshot.val();
        mainGraph.setData(data.sort(compare));
        config.element = "curr_err";
        Morris.Line(config);
    });
}

renderLiveGraph();

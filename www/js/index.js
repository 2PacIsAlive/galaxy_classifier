var Firebase = require("firebase");
var firebase = new Firebase("https://galaxy-classifier.firebaseio.com/");

var err = firebase.child("error")

var data = [];

function compare(a,b) {
    if (a["epoch"] < b["epoch"])
        return -1;
    else if (a["epoch"] > b["epoch"])
        return 1;
    else 
        return 0 
};
/*
err.once("value", function(snapshot) {
    var obj = snapshot.val();
    var data = Object.keys(obj).map(function (key) {return obj[key]});
    var flattened = [];
    for (var i=0; i<data.length; i++) {
        flattened = flattened.concat(data[i]['err']);
    }
    var max = Math.max.apply(Math,flattened) + 2,
        min = Math.min.apply(Math,flattened) - 2; 
    config = {
        data: data.sort(compare),
        xkey: 'epoch',
        ykeys: ['err'],
        labels: ['Error'],
        fillOpacity: 0.6,
        hideHover: 'auto',
        behaveLikeLine: true,
        resize: true,
        pointFillColors:['#ffffff'],
        pointStrokeColors: ['black'],
        lineColors:['#5D3241'],
        pointSize: 0,
        parseTime: false
    };
    config.element = 'curr-err';
    Morris.Area(config);
});
*/

function renderLiveGraph() {
    console.log('rendering...');
    var mainGraph;
    mainGraph = Morris.Area({
        element: 'curr_err',
        data: data,
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
}

err.on("value", function(snapshot) {
    console.log('updating...');
    var obj = snapshot.val();
    data = Object.keys(obj).map(function (key) {return obj[key]});
    var flattened = [];
    for (var i=0; i<data.length; i++) {
        flattened = flattened.concat(data[i]['err']);
    }
    var max = Math.max.apply(Math,flattened) + 2,
        min = Math.min.apply(Math,flattened) - 2; 
    mainGraph.setData(data.sort(compare));
});

renderLiveGraph();



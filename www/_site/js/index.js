var firebase = new Firebase("https://sorting.firebaseio.com/");

var avgstream = firebase.child("stream/avg")
var maxstream = firebase.child("stream/max")

var insertionsort = firebase.child("Insertion Sort");
var mergesort     = firebase.child("Mergesort");
var quicksort     = firebase.child("Quicksort");

function compare(a,b) {
    if (a["n"] < b["n"])
        return -1;
    else if (a["n"] > b["n"])
        return 1;
    else 
        return 0 
};

insertionsort.on("value", function(snapshot) {
    var data = snapshot.val(),
        config = {
            data: data.sort(compare),
            xkey: 'n',
            ykeys: ['avg', 'max'],
            labels: ['Average Runtime', 'Worst Runtime'],
            fillOpacity: 0.6,
            hideHover: 'auto',
            behaveLikeLine: true,
            resize: true,
            pointFillColors:['#ffffff'],
            pointStrokeColors: ['black'],
            lineColors:['red','black'],
            parseTime: false
        };
    config.element = 'insertionsort';
    Morris.Area(config);
});

mergesort.on("value", function(snapshot) {
    var data = snapshot.val(),
        config = {
            data: data.sort(compare),
            xkey: 'n',
            ykeys: ['avg', 'max'],
            labels: ['Average Runtime', 'Worst Runtime'],
            fillOpacity: 0.6,
            hideHover: 'auto',
            behaveLikeLine: true,
            resize: true,
            pointFillColors:['#ffffff'],
            pointStrokeColors: ['black'],
            lineColors:['blue','black'],
            parseTime: false
        };
    config.element = 'mergesort';
    Morris.Area(config);
});

quicksort.on("value", function(snapshot) {
    var data = snapshot.val(),
        config = {
            data: data.sort(compare),
            xkey: 'n',
            ykeys: ['avg', 'max'],
            labels: ['Average Runtime', 'Worst Runtime'],
            fillOpacity: 0.6,
            hideHover: 'auto',
            behaveLikeLine: true,
            resize: true,
            pointFillColors:['#ffffff'],
            pointStrokeColors: ['black'],
            lineColors:['purple','black'],
            parseTime: false
        };
    config.element = 'quicksort';
    Morris.Area(config);
});

maxstream.on("value", function(snapshot) {
    var data = snapshot.val(),
        config = {
            data: data.sort(compare),
            xkey: 'n',
            ykeys: ['insertion', 'merge', 'quick'],
            labels: ['Insertion Sort Worst Time', 'Merge Sort Worst Time', 'Quick Sort Worst Time'],
            fillOpacity: 0.6,
            hideHover: 'auto',
            behaveLikeLine: true,
            resize: true,
            pointFillColors:['#ffffff'],
            pointStrokeColors: ['black'],
            lineColors:['red','blue','purple'],
            parseTime: false
        };
    config.element = 'maxstream';
    Morris.Line(config);
});

avgstream.on("value", function(snapshot) {
    var data = snapshot.val(),
        config = {
            data: data.sort(compare),
            xkey: 'n',
            ykeys: ['insertion', 'merge', 'quick'],
            labels: ['Insertion Sort Average Time', 'Merge Sort Average Time', 'Quick Sort Average Time'],
            fillOpacity: 0.6,
            hideHover: 'auto',
            behaveLikeLine: true,
            resize: true,
            pointFillColors:['#ffffff'],
            pointStrokeColors: ['black'],
            lineColors:['red','blue','purple'],
            parseTime: false
        };
    config.element = 'avgstream';
    Morris.Line(config);
});

function init() {
    if (myMap) {
        myMap.destroy()
    }
    var myMap = new ymaps.Map("map", {
        center: [55.76, 37.64],
        zoom: 7
    });

var myPolyline = new ymaps.Polyline([
    [55.86, 37.84],
    [55.70, 37.55],
    [55.8, 37.4]
], {},
{
    strokeWidth: 1,
    strokeColor: '#0000FF',
});

    myMap.geoObjects.add(myPolyline);
}

function draw_lines(){

var myPolyline1 = new ymaps.Polyline([
    [55.86, 37.84],
    [55.70, 37.55],
    [55.8, 37.4],
    [51.8, 38.4]
], {},
{
    strokeWidth: 1,
    strokeColor: '#0000FF',
});

    myMap.geoObjects.add(myPolyline1);

}
ymaps.ready(init);
setTimeout(draw_lines, 5000);

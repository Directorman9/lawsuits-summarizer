packages.config(function ($routeProvider) {

    $routeProvider
    .when("/", {
        templateUrl : "/static/htmls/packages.html"
    })
    .when("/packages", {
        templateUrl: "/static/htmls/packages.html"
    })
 });
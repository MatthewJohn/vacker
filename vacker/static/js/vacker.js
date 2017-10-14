(function() {
    var app = angular.module("vackerApp", []);

    var YearController = function($scope, $http) {

        var onYearsComplete = function(response) {
            $scope.years = response.data;
        };
        var onHttpError = function(reason) {
            alert("HTTP error: " + reason);
        };

        $http.get("http://localhost:5000/years")
            .then(onYearsComplete, onHttpError);

        $scope.get_thumbnail_url = function (year) {
            return "http://localhost:5000/years/" + year + "/thumbnail";
        };

    };

    app.controller("YearController", YearController);
})();

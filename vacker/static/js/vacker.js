(function() {
    var app = angular.module("vackerApp", []);

    var PhotoController = function($scope, $http) {

        $scope.selected_year = null;
        $scope.selected_month = null;
        $scope.show_month_selecter = true;
        $scope.show_day_selecter = true;
        $scope.show_event_selecter = false;
        $scope.show_set_selecter = false;
        $scope.show_media_selecter = false;
        $scope.years = [];
        $scope.months = [];
        $scope.days = [];
        $scope.month_names = {
            1: "Jan",
            2: "Feb",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "Aug",
            9: "Sept",
            10: "Oct",
            11: "Nov",
            12: "Dec"
        }

        var makeId = function makeid() {
          var text = "";
          var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

          for (var i = 0; i < 5; i++)
            text += possible.charAt(Math.floor(Math.random() * possible.length));

          return text;
        }
        $scope.year_random = makeId();

        var onYearsComplete = function(response) {
            $scope.years = response.data;
        };
        var onMonthsComplete = function(response) {
            $scope.months = response.data;
            $scope.show_day_selecter = false;
            $scope.show_event_selecter = false;
            $scope.show_set_selecter = false;
            $scope.show_media_selecter = false;
        };
        var onDaysComplete = function(response) {
            $scope.days = response.data;
            $scope.show_day_selecter = true;
            $scope.show_event_selecter = false;
            $scope.show_set_selecter = false;
            $scope.show_media_selecter = false;
        };
        var onEventsComplete = function(response) {
            if (response.data.length == 1) {
                $scope.select_event(response.data[0].id);
                $scope.show_set_selecter = true;
                $scope.show_event_selecter = false;
            } else {
                $scope.events = response.data;
                $scope.show_event_selecter = true;
                $scope.show_set_selecter = false;
            }
            $scope.show_media_selecter = false;
        };
        var onSetsComplete = function(response) {
            if (response.data.length == 1) {
                $scope.select_set(response.data[0]);
                $scope.show_media_selecter = true;
                $scope.show_set_selecter = false;
            } else {
                $scope.sets = response.data;
                $scope.show_set_selecter = true;
                $scope.show_media_selecter = false;
            }
        };
        var onMediaComplete = function(response) {
            $scope.media = response.data;
            $scope.show_media_selecter = true;
        };
        var onHttpError = function(reason) {
            alert("HTTP error: " + reason);
        };

        $http.get("http://localhost:5000/years")
            .then(onYearsComplete, onHttpError);

        $scope.get_thumbnail_url = function (base_url, random_value) {
            return "http://localhost:5000/" + base_url + "/thumbnail?" + random_value;
        };
        $scope.get_media_thumbnail_url = function(media_id) {
            return "http://localhost:5000/thumbnail/" + media_id
        }

        $scope.select_year = function(year) {
            $scope.month_random = makeId();
            $scope.months = [];
            $scope.days = [];
            $scope.events = [];
            $scope.sets = [];
            $scope.media = [];
            $http.get("http://localhost:5000/years/" + year + "/months")
                .then(onMonthsComplete, onHttpError);
            $scope.selected_year = year;
        };
        $scope.select_month = function(month) {
            $scope.day_random = makeId();
            $scope.days = [];
            $scope.events = [];
            $scope.sets = [];
            $scope.media = [];
            $http.get("http://localhost:5000/years/" + $scope.selected_year + "/months/" + month + '/days')
                .then(onDaysComplete, onHttpError);
            $scope.selected_month = month;
        };
        $scope.select_day = function(day) {
            $scope.event_random = makeId();
            $scope.events = [];
            $scope.sets = [];
            $scope.media = [];
            $http.get("http://localhost:5000/years/" + $scope.selected_year + "/months/" + $scope.selected_month + '/days/' + day + '/events')
                .then(onEventsComplete, onHttpError);
            $scope.selected_day = day;
        };
        $scope.select_event = function(event_id) {
            $scope.sets = [];
            $scope.media = [];
            $http.get("http://localhost:5000/events/" + event_id + "/sets")
                .then(onSetsComplete, onHttpError);
            $scope.selected_event = event_id;
        };
        $scope.select_set = function(set_id) {
            $scope.media = [];
            $http.get("http://localhost:5000/sets/" + set_id + "/media")
                .then(onMediaComplete, onHttpError);
            $scope.selected_set = set_id;
        };
    };

    app.controller("PhotoController", PhotoController);
})();

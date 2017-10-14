angular.
  module('vackerApp').
  component('yearList', {
    template:
      '<div class="item" ng-repeat="year in $ctrl.years">' +
      '<img class="item-img" src="{{ year.thumbnails[0] }}">' +
      '<div class="item-title">{{ year }}</div>' +
      '</div>',
    controller: function PhoneListController() {
        this.years = 
    }
});
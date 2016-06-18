var ListController, app;

app = angular.module('ngApp', ['ngResource']);

ListController = (function() {
  ListController.$inject = ['$scope', '$http', '$timeout'];

  function ListController(scope, http, timeout) {
    this.scope = scope;
    this.http = http;
    this.timeout = timeout;
    this.scope.set_color = function(x) {
      return set_color(x);
    };
    this.poll_page();
    this.intervalFunction();
  }

  ListController.prototype.intervalFunction = function() {
    return this.timeout((function(_this) {
      return function() {
        _this.poll_page();
        return _this.intervalFunction();
      };
    })(this), 5000);
  };

  ListController.prototype.poll_page = function() {
    var request;
    request = this.http.get('/poll_backend', {
      params: {}
    });
    return request.then((function(_this) {
      return function(result) {
        return _this.scope.site_data = result.data;
      };
    })(this));
  };

  ListController.prototype.set_color = function(status_code) {
    if (status_code !== 200) {
      return {
        color: "red"
      };
    } else {
      return {
        color: "green"
      };
    }
  };

  return ListController;

})();

app.controller('ListController', ListController);

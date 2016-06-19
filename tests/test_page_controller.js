describe("ListController", function() {

  beforeEach(module("pollApp"));

  var controller, scope;

  beforeEach(inject(function (_$rootScope_, _$http_, _$timeout_, _$controller_) {
    scope = $rootScope.$new();
    controller = $controller("ListController", {
      $scope: scope,
      $http: _$http_,
      $timeout: _$timeout_
    });
  }));
  it('should be green', function () {
    expect(controller.set_color(200)).toEqual("color: green");
    expect(controller.set_color(201)).toEqual("color: red");
  });
});

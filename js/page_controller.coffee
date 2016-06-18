app = angular.module('ngApp', ['ngResource'])


class ListController

  @$inject: ['$scope', '$http', '$timeout']
  constructor: (@scope, @http, @timeout) ->
    @scope.set_color = (x) ->
      set_color(x)
    @poll_page()
    @intervalFunction()

  intervalFunction: ->
    @timeout =>
      @poll_page()
      @intervalFunction()
    , 5000

  poll_page: ->
    request = @http.get '/poll_backend', params: { }
    request.then (result) =>
      @scope.site_data = result.data

  set_color: (status_code) ->
    if status_code != 200
      return {color: "red"}
    else
      return {color: "green"}

app.controller 'ListController', ListController

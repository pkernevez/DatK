'use strict';

angular.module('myApp.manifest', [])

.factory('manifestFactory', ['$http', function($http) {

  return{
      getManifest : function() {
        return $http.get('env_status.json');
      }
  }
}]);
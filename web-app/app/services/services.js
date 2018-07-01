'use strict';

angular.module('angApp.services', ['ngResource', 'angApp.appConfig'])


  .factory('Search', function($resource, ENV){
    return { 
    	result: $resource(ENV + '/matches', {}, {
            searchResults: { method: 'POST', params: {}, isArray: false } 
    	}),
    }
  })

  .factory('Auth', function($resource, ENV){
    return { 
    	user: $resource(ENV + '/user/auth', {}, {
            authUser: { method: 'POST', params: {}, isArray: false } 
    	}),
    }
  })

 .value('version', '0.1');

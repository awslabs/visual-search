'use strict';


angular.module('angApp', [  'ngRoute', 'ngResource', 'ui.bootstrap',
                            'angApp.appConfig',
                            'angApp.filters', 
                            'angApp.services', 
                            'angApp.directives', 
                            'angApp.mainControllers',
                            'angApp.searchControllers' ] )
                            

  .config(['$routeProvider', '$httpProvider', function($routeProvider, $httpProvider) {
	
	// main page 
	$routeProvider.when('/', 
			{templateUrl: 'app/partials/main.html', controller: 'MainCtrl'});
	
    // search page
	$routeProvider.when('/search', 
			{templateUrl: 'app/partials/search.html', controller: 'SearchCtrl'});

	// settings
	$routeProvider.when('/settings', 
			{templateUrl: 'app/partials/settings.html', controller: 'MainCtrl'});
    
    $routeProvider.otherwise({redirectTo: '/'});
    
    // to enable CORS (next two lines)
    $httpProvider.defaults.useXDomain = true;
	delete $httpProvider.defaults.headers.common['X-Requested-With'];
    
    // to enable storing/setting cookies with XHR requests (by default this is not allowed in most browsers)
    //$httpProvider.defaults.withCredentials = true;
  }])
  
  .run( function($rootScope, $location, $window, $http) {
	  
	// global api error handler
	$rootScope.handleApiError = (e) => {
		alert(	"API ERROR \nError code: " + 
				e.data.apiError + "\nError message: " + 
				e.data.apiMessage + "\nRuntime exception: " +
				e.data.javaException);
		if (401 == e.data.apiError ) {
			$location.path('/settings');
		}
	};
	
	// keep user logged in after page refresh by re-setting the Authorization header,
	// which ordinarily would be lost after a refresh due to the browser somehow
	// clearing the $http object of its default properties such as headers
	var authToken = $window.sessionStorage.getItem("authToken");
	if ( authToken != null && authToken.length >  0 ) {
		$http.defaults.headers.common['Authorization'] = 'Bearer ' + authToken;
	}
	
  });


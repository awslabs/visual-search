'use strict';


/**
 * general purpose controllers for main page directory, managing login etc.
 * 
 */
angular.module('angApp.mainControllers', [])

 .controller('MainCtrl', ['$scope', '$rootScope', '$window', '$location', '$http', 'Auth',
   function($scope, $rootScope, $window, $location, $http, Auth) {

    $scope.mainData = {
    	loggedIn: true, // NOTE change to false to begin enabling login
    	user: {userName: '', password: '', authToken: ''},
    };
    
    $scope.isLoggedIn = () => {
    	
    	let authInfo = $window.sessionStorage.getItem("auth");
    	if ( null == authInfo || "false" === authInfo ) {
    		return false;
    	}
    	else {
            
    		$scope.mainData.loggedIn = true;
    		$scope.mainData.user.userName = $window.sessionStorage.getItem("userName");
    		$scope.mainData.user.authToken = $window.sessionStorage.getItem("authToken");
    		return true
    	}
    }
    
    $scope.setIsLoggedIn = (isTrue, securityLevel) => {
    	
    	let sIsTrue = isTrue ? "true" : "false";
    	$window.sessionStorage.setItem("auth", sIsTrue);
    	let curName = isTrue ? $scope.mainData.user.userName : "";
    	$window.sessionStorage.setItem("userName", curName);
       	let authToken = isTrue ? $scope.mainData.user.authToken : "";
    	$window.sessionStorage.setItem("authToken", authToken);
    	
    	// set security level
    	// set a common "Authorization" header for all HTTP requests
    	// (NOTE:  the app.js run function has a case to handle page refreshes, any changes
    	// made here should also be made to that function)
    	if ( isTrue ) {
    		$window.sessionStorage.setItem("securityLevel", securityLevel);
    		$http.defaults.headers.common['Authorization'] = 'Bearer ' + $scope.mainData.user.authToken;
    	}
    }
    
    // check for login every time this page is launched
    $scope.isLoggedIn();
	  
    // click handler for login button
    $scope.login = () => {
    	
    	// NOTE:  if there are any kind of username and password format limits, validate here.
    	if ( $scope.mainData.user.userName === '' || $scope.mainData.user.password === '' ) {
    		$scope.loginError = true;
    		return;
    	}
    	
		Auth.user.authUser($scope.mainData.user, function(data) {
			
			$scope.loginError = false;
			$scope.mainData.user.authToken = data.token;
			$scope.setIsLoggedIn(true, data.securityLevel);
	    	$scope.mainData.loggedIn = true;
			
		}, function(e) { 
			
			$scope.loginError = true;
			$scope.setIsLoggedIn(false, null);
	    	$scope.mainData.loggedIn = false; 
		} );
 
    };
    
    // click handler for directory selection table
    $scope.setToolType = (event) => {
    	
    	let typeValue = event.currentTarget.attributes.id.nodeValue;
  
        if ( typeValue === "search" ) {
    		$window.sessionStorage.setItem("toolType", "search");
            $location.path('/search');
    	}
     	else {
    		// expand for new pages
    	}
    }
    
    // click handler for logout button
	$scope.logOut = () => {
		
		$scope.setIsLoggedIn(false, null);
		$location.path('/');
	}
	
    $scope.hasSufficientSecurityLevel = (requiredLevel) => {
    	
    	let actualSecurityLevel = $window.sessionStorage.getItem("securityLevel");
    	if ( null == actualSecurityLevel || parseInt(actualSecurityLevel) < requiredLevel ) {
    		alert("You do not have sufficient security permissions to proceed.");
    		return false;
    	}
    	
    	return true;
    }
    

  }]);
  
